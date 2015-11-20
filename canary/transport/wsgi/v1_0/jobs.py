import json
import falcon
import base64
from falcon.errors import HTTPBadRequest
from oslo_config import cfg
from canary.openstack.common import log
from canary.drivers.redis import redisdriver


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

        redis_driver = redisdriver.RedisStorageDriver()
        job_details = redis_driver.get_job_details()
        resp.status = falcon.HTTP_200

        for i in range(len(job_details)):
            flow_status = []
            job_details[i] = json.loads(base64.b64decode(job_details[i]))
            for val in job_details[i]['jobs']:
                stat = {}
                sub_tasks = val['flow_status'].values()[0]['tasks']
                for sub_val in sub_tasks:
                    if sub_val:
                        for task_name, task_values in sub_val.items():
                            stat[task_name] = task_values['state']        
                        flow_status.append(stat)

            job_details[i]['flow_status'] = flow_status
        resp.body = json.dumps(job_details)
