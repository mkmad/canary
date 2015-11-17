from wsgiref import simple_server

import falcon
from oslo_config import cfg

from canary.openstack.common import log
from canary.transport.wsgi import v1_0
from canary.drivers.cassandra import cassandradriver
import canary

conf = cfg.CONF
conf(project='canary', prog='canary', args=[])

log.setup('canary')
LOG = log.getLogger(__name__)

_CANARY_OPTIONS = [
    cfg.StrOpt('host', default='127.0.0.1',
               help='host to serve app on'),
    cfg.IntOpt('port', default='8888',
               help='port to serve app on'),
]

CANARY_GROUP = cfg.OptGroup(
    name='canary',
    title='canary options'
)

conf.register_opts(_CANARY_OPTIONS, group=CANARY_GROUP)

canary.database = None


class Driver(object):

    def __init__(self):

        self.app = None
        self.conf = conf
        self._init_routes()
        self._init_database_connections()

    def _init_database_connections(self):
        db_driver = cassandradriver.CassandraStorageDriver(self.conf)
        db_driver.connect()
        canary.database = db_driver

    def _init_routes(self):
        """Initialize hooks and URI routes to resources."""

        endpoints = [
            ('/v1.0', v1_0.public_endpoints()),

        ]

        self.app = falcon.API()

        for version_path, endpoints in endpoints:
            for route, resource in endpoints:
                self.app.add_route(version_path + route, resource)

    def listen(self):
        """Self-host using 'bind' and 'port' from canary conf"""
        msgtmpl = (u'Serving on host %(bind)s:%(port)s')
        host = conf['canary']['host']
        port = conf['canary']['port']
        LOG.info(msgtmpl,
                 {'bind': host,
                     'port': port})

        httpd = simple_server.make_server(host,
                                          port,
                                          self.app)
        httpd.serve_forever()
