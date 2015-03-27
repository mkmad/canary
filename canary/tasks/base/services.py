import abc
import six


@six.add_metaclass(abc.ABCMeta)
class DistributedTaskServicesBase(object):

    """Services Controller Base class."""

    def __init__(self):
        super(DistributedTaskServicesBase, self).__init__()

    def submit_task(self):
        """submit a task .

        :raises NotImplementedError
        """
        raise NotImplementedError

    def run_task_worker(self):
        """worker that deals with hourly updates

        :raises NotImplementedError
        """
        raise NotImplementedError