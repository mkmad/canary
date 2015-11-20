import json
import time

import falcon
from falcon.errors import HTTPBadRequest
from oslo_config import cfg

from canary.openstack.common import log
from canary.drivers.cassandra import cassandradriver
from canary.util import canonicalize
from kazoo.client import KazooClient

conf = cfg.CONF
conf(project='canary', prog='canary', args=[])

log.setup('canary')
LOG = log.getLogger(__name__)

_CANARY_OPTIONS = [
    cfg.StrOpt('hosts', default='localhost:2181',
               help='Hostname for the zookeeper backend'),
    cfg.StrOpt('conductor_path', default='/taskflow/jobs/.entities/conductor',
               help='The path name where the canary conductor registers itself')
]

CANARY_GROUP = cfg.OptGroup(
    name='canary_con',
    title='conductor options'
)

conf.register_opts(_CANARY_OPTIONS, group=CANARY_GROUP)


class ConductorResource(object):
    
    def on_get(self, req, resp):
        path = req.get_param('path')
        if not path:
            path = conf['canary_con']['conductor_path']
        resp.status = falcon.HTTP_200
        resp.body = self._get_conductor_information(path)

    def _get_conductor_information(self,path,hosts=conf['canary_con']['hosts']):
        k = KazooClient(hosts=hosts)
        try:
            k.start()
            conductor_count = len(k.get_children(path))
            conductors = k.get_children(path)
            return json.dumps({'conductor_count':conductor_count,'conductors':conductors})
            k.stop()
        except Exception as e:
            LOG.info('Failed to fetch conductor information: {0}'.format(e))
