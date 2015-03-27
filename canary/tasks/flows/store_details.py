from oslo.config import cfg
from taskflow.patterns import linear_flow
from taskflow import task

from canary.openstack.common import log
from canary.model import JobBoard
from canary.drivers.cassandradriver import CassandraStorageDriver

conf = cfg.CONF
conf(project='canary', prog='canary', args=[])

log.setup('canary')
LOG = log.getLogger(__name__)

_CASSANDRA_OPTIONS = [
    cfg.StrOpt('keyspace', default='canary',
               help='Keyspace for all queries made in session'),

]

CASSANDRA_GROUP = cfg.OptGroup(
        name='cassandra',
        title='cassandra options'
    )

conf.register_opts(_CASSANDRA_OPTIONS, group=CASSANDRA_GROUP)

def canary_monitoring_service():
    flow = linear_flow.Flow('Canary Monitoring Service').add(
            GenerateTaskflowInformation(),
            InsertJobData(rebind=['job_details_tuple'])
    )
    return flow

class GenerateTaskflowInformation(task.Task):

    default_provides = 'job_details_tuple'

    def execute(self, name, path, conf, persistence):
        jb = JobBoard(name=name,conf=conf,persistence=persistence)
        job_details = jb.get_all_jobs(serializable=True)
        job_count = jb.board.job_count
        job_details_tuple = (job_details, path, job_count)
        return job_details_tuple

class InsertJobData(task.Task):

    def execute(self, job_details_tuple, **kwargs):
        job_details, path, job_count = job_details_tuple
        cassandra_driver = CassandraStorageDriver()
        cassandra_driver.connect(conf['cassandra']['keyspace'])
        cassandra_driver.insert_job_details(path=path,
                                            job_count=job_count,
                                            job_details=job_details)
        cassandra_driver.close_connection()