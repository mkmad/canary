from oslo_config import cfg

from canary.common import cli
from canary.openstack.common import log as logging
from canary.transport.wsgi.driver import Driver

conf = cfg.CONF
conf(project='canary', prog='canary', args=[])
logging.setup('canary')

LOG = logging.getLogger(__name__)


@cli.runnable
def run():
    app_container = Driver()
    app_container.listen()
