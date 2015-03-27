import abc
import six


@six.add_metaclass(abc.ABCMeta)
class DistributedTaskDriverBase(object):
    """Interface definition for distributed task queue driver.
    :param conf: Configuration containing options for this driver.
    :type conf: `oslo.config.ConfigOpts`
    """
    def __init__(self, conf):
        self._conf = conf

    @property
    def conf(self):
        """conf
        :returns conf
        """
        return self._conf