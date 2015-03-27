from oslo.config import cfg

from canary.openstack.common import log
from canary.transport.wsgi.driver import Driver

app_container = Driver()

conf = cfg.CONF
conf(project='canary', prog='canary', args=[])

log.setup('canary')
app = app_container.app