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

from oslo.config import cfg
from taskflow.jobs import backends as job_backends
from taskflow.persistence import backends as persistence_backends

from canary.tasks import base
from canary.openstack.common import log

LOG = log.getLogger(__name__)

TASKFLOW_OPTIONS = [
    cfg.StrOpt('jobboard_backend_type', default='zookeeper',
               help='Default jobboard backend type'),
    cfg.StrOpt('persistent_backend_type', default='zookeeper',
               help='Default jobboard persistent backend type'),
    cfg.ListOpt('jobboard_backend_host', default=['localhost'],
                help='Default jobboard backend server host'),
    cfg.IntOpt('jobboard_backend_port', default=2181,
               help='Default jobboard backend server port (e.g: ampq)'),
    cfg.ListOpt('persistent_backend_host', default=['localhost'],
                help='Default persistent backend server host'),
    cfg.IntOpt('persistent_backend_port', default=2181,
               help='Default persistent backend server port (e.g: ampq)'),
    cfg.StrOpt('canary_worker_path',
               default='/taskflow/jobs/canary_jobs',
               help='Default Zookeeper path for canary jobs'),
    cfg.StrOpt('canary_worker_jobboard',
               default='canary_jobs',
               help='Default jobboard name associated with canary worker jobs'),
]

TASKFLOW_GROUP = 'tasks:taskflow'


class TaskFlowDistributedTaskDriver(base.Driver):
    """TaskFlow distributed task Driver."""

    def __init__(self, conf):
        super(TaskFlowDistributedTaskDriver, self).__init__(conf)
        conf.register_opts(TASKFLOW_OPTIONS, group=TASKFLOW_GROUP)
        self.distributed_task_conf = conf[TASKFLOW_GROUP]

        job_backends_hosts = ','.join(['%s:%s' % (
            host, self.distributed_task_conf.jobboard_backend_port)
            for host in
            self.distributed_task_conf.jobboard_backend_host])

        self.jobboard_backend_conf_worker = {
            # This topic could become more complicated
            "board": self.distributed_task_conf.jobboard_backend_type,
            "hosts": job_backends_hosts,
            "path": self.distributed_task_conf.canary_worker_path,
        }

        persistence_backends_hosts = ','.join(['%s:%s' % (
            host, self.distributed_task_conf.jobboard_backend_port)
            for host in
            self.distributed_task_conf.jobboard_backend_host])

        self.persistence_backend_conf = {
            # This topic could become more complicated
            "connection": self.distributed_task_conf.persistent_backend_type,
            "hosts": persistence_backends_hosts,
        }

    def is_alive(self):
        """Health check for TaskFlow worker."""
        return True

    def persistence(self):
        return persistence_backends.backend(
            self.persistence_backend_conf.copy())

    def job_board(self, conf, persistence, **kwargs):
        return job_backends.backend(
            self.distributed_task_conf.canary_worker_jobboard,
            conf.copy(), persistence=persistence)


    @property
    def vendor_name(self):
        """storage name.

        :returns 'TaskFlow'
        """
        return 'TaskFlow'
