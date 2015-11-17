import json
import time

import falcon
from falcon.errors import HTTPBadRequest
from oslo_config import cfg

from canary.openstack.common import log
from canary.drivers.cassandra import cassandradriver
from canary.util import canonicalize

conf = cfg.CONF
conf(project='canary', prog='canary', args=[])

log.setup('canary')
LOG = log.getLogger(__name__)

_CANARY_OPTIONS = [
    cfg.IntOpt('interval', default='120',
               help='Retrieve activities for the last x seconds'),

]

CANARY_GROUP = cfg.OptGroup(
    name='canary',
    title='canary options'
)


conf.register_opts(_CANARY_OPTIONS, group=CANARY_GROUP)


class ItemResource(object):

    def on_get(self, req, resp):
        path = req.get_param('path')
        if not path:
            description = "Specify a valid `path` querystring"
            raise HTTPBadRequest(title="Bad Request",
                                 description=description)

        cassandra_driver = cassandradriver.CassandraStorageDriver(conf)
        cassandra_driver.connect()

        current_time = time.time()
        query_time = current_time - conf['canary']['interval']
        job_details = \
            cassandra_driver.get_job_details(date=canonicalize(query_time),
                                             path=path)

        cassandra_driver.close_connection()
        resp.status = falcon.HTTP_200

        for i in range(len(job_details)):
            flow_status = []
            for val in json.loads(job_details[i]['jobs']):
                stat = {}
                #flow_id = val['flow_status'].keys()[0]
                #flow_status[flow_id] = []
                sub_tasks = val['flow_status'].values()[0]['tasks']
                for sub_val in sub_tasks:
                    if sub_val:
                        #import ipdb;ipdb.set_trace()
                        for task_name, task_values in sub_val.items():
                            stat[task_name] = task_values['state']        
                        flow_status.append(stat)

            job_details[i]['jobs'] = json.loads(job_details[i]['jobs'])
            job_details[i]['flow_status'] = flow_status
        resp.body = json.dumps(job_details)
