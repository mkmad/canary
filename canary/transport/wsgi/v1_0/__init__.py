from canary.transport.wsgi.v1_0 import jobs
from canary.transport.wsgi.v1_0 import conductors

def public_endpoints():

    return [
        # Return list of jobs from taskflow for a given path
        ('/jobs',
        jobs.ItemResource()),
        ('/conductor',
        conductors.ConductorResource()),
    ]
