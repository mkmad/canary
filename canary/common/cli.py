import functools
import sys


from oslo_config import cfg

from canary.openstack.common import log
from canary.transport.wsgi.driver import Driver

app_container = Driver()

conf = cfg.CONF
conf(project='canary', prog='canary', args=[])

log.setup('canary')


LOG = log.getLogger(__name__)


def _fail(returncode, ex):
    """Handles terminal errors.

    :param returncode: process return code to pass to sys.exit
    :param ex: the error that occurred
    """

    LOG.exception(ex)
    sys.exit(returncode)


def runnable(func):
    """Entry point wrapper.

    Note: This call blocks until the process is killed
          or interrupted.
    """

    @functools.wraps(func)
    def _wrapper():
        try:
            log.setup('canary')
            func()
        except KeyboardInterrupt:
            LOG.info(u'Terminating')
        except Exception as ex:
            _fail(1, ex)

    return _wrapper