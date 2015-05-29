import importlib
import json

from oslo.config import cfg
from taskflow.patterns import linear_flow
from taskflow import task

from canary.openstack.common import log
from canary.model import JobBoard


log.setup('canary')
LOG = log.getLogger(__name__)


def memoize(f):
    memo = {}

    def helper(*args, **kwargs):
        x = str(args) + str(kwargs)
        if x not in memo:
            memo[x] = f(*args, **kwargs)
        return memo[x]

    return helper

@memoize
def load_database_driver():

    conf = cfg.CONF
    conf(project='canary', prog='canary', args=[])

    _CANARY_OPTIONS = [
        cfg.StrOpt('driver', default='mongo',
                   help='Driver to be loaded')

    ]

    CANARY_GROUP = cfg.OptGroup(
            name='canary',
            title='canary options'
        )

    conf.register_opts(_CANARY_OPTIONS, group=CANARY_GROUP)
    return _load_driver(conf.canary.driver)


@memoize
def _load_driver(classname):
    """Creates of the instance of the specified
    class given the fully-qualified name. The module
    is dynamically imported.
    """
    pos = classname.rfind('.')
    module_name = classname[:pos]
    class_name = classname[pos + 1:]

    mod = importlib.import_module(module_name)
    return getattr(mod, class_name)()

def canary_monitoring_service():
    flow = linear_flow.Flow('Canary Monitoring Service').add(
            GenerateTaskflowInformation(),
            InsertJobData(rebind=['job_details_tuple'])
    )
    return flow

class GenerateTaskflowInformation(task.Task):

    default_provides = 'job_details_tuple'

    def execute(self, name, path, conf, persistence, logbook_path):
        jb = JobBoard(name=name,
                      conf=conf,
                      persistence=persistence,
                      logbook_path=logbook_path)
        job_details = jb.get_all_jobs(serializable=True)
        job_count = jb.board.job_count
        job_details_tuple = (job_details, path, job_count)
        jb.close()
        return job_details_tuple

class InsertJobData(task.Task):

    def execute(self, job_details_tuple, **kwargs):
        job_details, path, job_count = job_details_tuple
        driver = load_database_driver()
        driver.insert_job_details(path=path,
                                  job_count=job_count,
                                  job_details=json.loads(job_details))