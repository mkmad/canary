import json
import time

import falcon
from falcon.errors import HTTPBadRequest
from oslo.config import cfg

from canary.openstack.common import log
from canary.drivers.cassandradriver import CassandraStorageDriver
from canary.util import canonicalize

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

_CANARY_OPTIONS = [
    cfg.IntOpt('interval', default='120',
               help='Retrieve activities for the last x seconds'),

]

CANARY_GROUP = cfg.OptGroup(
        name='canary',
        title='canary options'
    )


conf.register_opts(_CASSANDRA_OPTIONS, group=CASSANDRA_GROUP)
conf.register_opts(_CANARY_OPTIONS, group=CANARY_GROUP)

class ItemResource(object):

    def on_get(self, req, resp):
        path = req.get_param('path')
        if not path:
            description = "Specify a valid `path` querystring"
            raise HTTPBadRequest(title="Bad Request",
                                 description=description)
        cassandra_driver = CassandraStorageDriver()
        cassandra_driver.connect(conf['cassandra']['keyspace'])
        current_time = time.time()
        query_time = current_time - conf['canary']['interval']
        job_details = \
            cassandra_driver.get_job_details(date=canonicalize(query_time),
                                             path=path)
        cassandra_driver.close_connection()
        resp.status = falcon.HTTP_200

        for i in range(len(job_details)):
            job_details[i]['jobs'] = json.loads(json.loads(job_details[i]['jobs']))
        resp.body = json.dumps(job_details)