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

"""Mongo storage driver implementation."""


import time

from pymongo import MongoClient

from oslo_config import cfg

from canary.openstack.common import log as logging
from canary.util import canonicalize

conf = cfg.CONF
conf(project='canary', prog='canary', args=[])
logging.setup('canary')

LOG = logging.getLogger(__name__)

_MONGO_OPTIONS = [
    cfg.ListOpt('cluster', default=['127.0.0.1'],
                help='Mongo cluster contact points'),
    cfg.StrOpt('uri', default='mongodb://localhost:27017/',
               help='mongo uri'),
    cfg.IntOpt('port', default=9042, help='Mongo cluster port'),
    cfg.BoolOpt('ssl_enabled', default=False,
                help='Communicate with Mongo over SSL?'),
    cfg.StrOpt('ssl_ca_certs', default='',
               help='Absolute path to the appropriate .crt file'),
    cfg.BoolOpt('auth_enabled', default=False,
                help='Does Mongo have authentication enabled?'),
    cfg.StrOpt('username', default='', help='Mongo username'),
    cfg.StrOpt('password', default='', help='Mongo password'),
    cfg.StrOpt('ssl_version', default='TLSv1.1', help='TLS version'),
    cfg.StrOpt('database', default='canary', help='database name'),
    cfg.StrOpt('collection', default='jobs', help='collection name')
]

MONGO_GROUP = cfg.OptGroup(
        name='mongo',
        title='mongo options'
    )

conf.register_opts(_MONGO_OPTIONS, group=MONGO_GROUP)

def _connection(database):
    client = MongoClient(conf.mongo.uri)
    return client[database]


class MongoStorageDriver(object):

    def __init__(self,conf):
        super(MongoStorageDriver, self).__init__()
        self.session = _connection(database=conf.mongo.database)

    def insert_job_details(self, path, job_details, job_count):
        collection = self.session[conf.mongo.collection]

        date = canonicalize(time.time())
        args = dict(
            date=date,
            path=path,
            job_count=job_count,
            jobs=job_details
        )
        collection.insert_one(args)
