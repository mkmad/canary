from oslo.config import cfg

from canary.openstack.common import log as logging
from canary.tasks.taskflow import ServicesDriver

conf = cfg.CONF
conf(project='canary', prog='canary', args=[])
logging.setup('canary')

LOG = logging.getLogger(__name__)


def run():
    LOG.info("Starting Canary Conductor")
    ServicesDriver().run_task_worker()
