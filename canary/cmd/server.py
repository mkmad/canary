from canary.common import cli
from canary.transport.wsgi.driver import Driver


@cli.runnable
def run():
    app_container = Driver()
    app_container.listen()