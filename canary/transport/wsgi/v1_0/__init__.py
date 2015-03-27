from canary.transport.wsgi.v1_0 import jobs


def public_endpoints():

    return [
        # Return list of jobs from taskflow for a given path
        ('/jobs',
        jobs.ItemResource()),
    ]