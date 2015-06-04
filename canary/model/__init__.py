import json

from taskflow.persistence.backends.impl_zookeeper import ZkBackend
from taskflow.jobs.backends.impl_zookeeper import ZookeeperJobBoard


class JobBoard(object):

    def __init__(self, name, conf, persistence, logbook_path):
        self.name = name
        self.conf = conf
        self.persistence = persistence
        self.logbook_path = logbook_path

        self.board = ZookeeperJobBoard(name=self.name,
                                       conf=self.conf,
                                       persistence=self.persistence)
        self.board.connect()


    def get_flow_status(self, book_uuid):

        log_book_conf = self.conf.copy()
        log_book_conf['path'] = self.logbook_path
        backend = ZkBackend(log_book_conf)
        connection = backend.get_connection()
        log_book = connection.get_logbook(book_uuid)
        current_flow_status = {}
        complete_task_status = []
        current_task_status = {}
        for (uuid, flow) in log_book._flowdetails_by_id.items():

            flow_details = flow.to_dict()
            del flow_details['name']
            current_flow_status[flow.name] = flow_details
            for (uuid, task) in flow._atomdetails_by_id.items():
                task_details = task.to_dict()
                del task_details['name']
                current_task_status[task.name.replace('.','-')] = \
                    task_details
            complete_task_status.append(current_task_status)

            current_flow_status[flow.name]['tasks'] = complete_task_status

        backend.close()
        return current_flow_status

    def get_all_jobs(self, serializable=False):

        jobs_iter = self.board.iterjobs(ensure_fresh=True)

        if not serializable:
            return [job for job in jobs_iter]
        else:

            json_list = []
            for job in jobs_iter:
                board = job.board
                current_flow_status = self.get_flow_status(job._book_data['uuid'])
                owner = board.find_owner(job)
                status = job.state
                job_dict = job.__dict__
                job_dict['_created_on'] = job_dict['_created_on'].isoformat()
                job_dict['status'] = status
                job_dict['owner'] = owner
                job_dict['flow_status'] = current_flow_status
                del job_dict['_client']
                del job_dict['_board']
                json_list.append(job_dict)

            return json.dumps(json_list)

    def close(self):
        self.board.close()
