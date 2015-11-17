# Copyright (c) 2015 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from oslo_config import cfg
from oslo_utils import uuidutils
from taskflow.conductors import single_threaded
from taskflow import engines
from taskflow.persistence import logbook

from canary.tasks import base
from canary.tasks.taskflow.driver import TaskFlowDistributedTaskDriver
from canary.openstack.common import log


LOG = log.getLogger(__name__)


conf = cfg.CONF
conf(project='canary', prog='canary', args=[])

class TaskflowDistributedTaskServices(base.DistributedTaskServices):

    def __init__(self):
        super(TaskflowDistributedTaskServices, self).__init__()

        self.driver = TaskFlowDistributedTaskDriver(conf)
        self.jobboard_backend_conf_worker = \
            self.driver.jobboard_backend_conf_worker

    @property
    def persistence(self):
        return self.driver.persistence()

    def submit_task(self, flow_factory, **kwargs):
        """submit a task.

        """
        with self.persistence as persistence:

            with self.driver.job_board(
                    self.jobboard_backend_conf_worker.copy(),
                    persistence=persistence) as board:

                job_id = uuidutils.generate_uuid()
                job_name = '-'.join([flow_factory.__name__, job_id])
                job_logbook = logbook.LogBook(job_name)
                flow_detail = logbook.FlowDetail(job_name,
                                                 uuidutils.generate_uuid())
                factory_args = ()
                factory_kwargs = {}
                engines.save_factory_details(flow_detail, flow_factory,
                                             factory_args, factory_kwargs)
                job_logbook.add(flow_detail)
                persistence.get_connection().save_logbook(job_logbook)
                job_details = {
                    'store': kwargs
                }
                job = board.post(job_name,
                                 book=job_logbook,
                                 details=job_details)
                LOG.info("Posted: {0}".format(job))


    def run_task_worker(self):
        """Run a task flow worker (conductor).

        """
        with self.persistence as persistence:

            with self.driver.job_board(
                    self.jobboard_backend_conf_worker.copy(),
                    persistence=persistence) as board:
                conductor = single_threaded.SingleThreadedConductor(
                    "Canary worker conductor", board, persistence,
                    engine='serial')

                conductor.run()
