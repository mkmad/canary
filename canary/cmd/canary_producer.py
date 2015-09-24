from oslo_config import cfg


from canary.openstack.common import log as logging
from canary.tasks.taskflow import ServicesDriver
from canary.tasks.flows.store_details import canary_monitoring_service
from time import sleep

conf = cfg.CONF
conf(project='canary', prog='canary', args=[])

logging.setup('canary')
LOG = logging.getLogger(__name__)


def run():

    _CANARY_OPTIONS = [
        cfg.StrOpt('name',
                   default='jobboard',
                   help='name of the jobboard to track'),
        cfg.StrOpt('path',
                   default='/taskflow/jobs',
                   help='taskflow path to track'),
        cfg.StrOpt('logbook_path',
                   default='/taskflow',
                   help='logbook path to track'),
        cfg.StrOpt('persistence',
                   default='zookeeper',
                   help='persistence backend driver'),
        cfg.StrOpt('zookeeper_host',
                   default='localhost:2181',
                   help='zookeeper host that canary needs to query'),
        cfg.StrOpt('interval',
                   default=5,
                   help='interval (seconds) to check for new jobboard tasks'),
    ]

    CANARY_GROUP = cfg.OptGroup(
        name='canary',
        title='canary options'
    )
    conf.register_group(CANARY_GROUP)
    conf.register_opts(_CANARY_OPTIONS, group=CANARY_GROUP)

    kwargs = {
        'name': conf['canary'].name,
        'path': conf['canary'].path,
        'persistence': {
            'connection': conf['canary'].persistence,
        },
        'conf': {
            'path': conf['canary'].path,
            'hosts': conf['canary'].zookeeper_host
        },
        'logbook_path': conf['canary'].logbook_path,
    }

    # interval = conf['canary'].interval

    while True:
        LOG.info("Posting job to Zookeeper Jobboard")
        ServicesDriver().submit_task(canary_monitoring_service, **kwargs)
        sleep(5)
