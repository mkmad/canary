import json

from taskflow.jobs.backends.impl_zookeeper import ZookeeperJobBoard

class JobBoard(object):

    def __init__(self, name, conf, persistence):
        self.name = name
        self.conf = conf
        self.persistence = persistence

        self.board = ZookeeperJobBoard(name=self.name,
                                       conf=self.conf,
                                       persistence=self.persistence)
        self.board.connect()

    def get_all_jobs(self, serializable=False):

        jobs_iter = self.board.iterjobs(ensure_fresh=True)

        if not serializable:
            return [job for job in jobs_iter]
        else:

            json_list = []
            for job in jobs_iter:
                board = job.board
                owner = board.find_owner(job)
                status = job.state
                job_dict = job.__dict__
                job_dict['_created_on'] = job_dict['_created_on'].isoformat()
                job_dict['status'] = status
                job_dict['owner'] = owner
                del job_dict['_client']
                del job_dict['_board']
                json_list.append(job_dict)

            return json.dumps(json_list)

    def close(self):
        self.board.close()
