import datetime


def canonicalize(timestamp):
    """Returns a timestamp compatible with Cassandra.
    :param timestamp: UNIX timestamp
    :type timestamp: int
    :return: YYYY-mm-ddTHH:MM:SSZ
    :rtype: six.text_type
    """
    now = datetime.datetime.utcfromtimestamp(int(timestamp))
    return now.isoformat()