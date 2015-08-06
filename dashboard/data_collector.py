import json
import time
import requests


def run():

    tipboard_api_key = "b721f623a67441d68237eb1724f8a3cb"
    tipboard_api_version = "v0.1"
    tipboard_host = "http://localhost:7272"
    tipboard_url = "{0}/api/{1}/{2}/push".format(
        tipboard_host, tipboard_api_version, tipboard_api_key)

    canary_api_host = "http://localhost:8889"
    canary_jobs_path = "/taskflow/jobs/poppy_service_jobs"
    canary_api_url = "{0}/v1.0/jobs?path={1}".format(
        canary_api_host, canary_jobs_path)

    print("Starting Canary Dashboard Data Collector")

    while True:
        # request data from the Canary API
        unclaimed = "0"
        claimed = "0"
        completed = "0"
        running = "0"

        response = requests.get(canary_api_url)

        jobs = json.loads(response.text)
        jobs_list = []

        if jobs != []:
            jobs_list = jobs[0].get('jobs', [])

            unclaimed = len([
                x for x in jobs_list if x.get('status') == "UNCLAIMED"])
            claimed = len([
                x for x in jobs_list if x.get('status') == "CLAIMED"])
            completed = len([
                x for x in jobs_list if x.get('status') == "COMPLETED"])
            running = len([x for x in jobs_list])

        print "Unclaimed ({0}), Claimed ({1}), Completed ({2}), Running ({3})".format(
            unclaimed, claimed, completed, running)

        # parse the data for the various supported tiles
        unclaimed_jobs = {
            "title": "Unclaimed Jobs",
            "description": "",
            "just-value": unclaimed
        }

        claimed_jobs = {
            "title": "Claimed Jobs",
            "description": "",
            "just-value": claimed
        }

        completed_jobs = {
            "title": "Completed Jobs",
            "description": "",
            "just-value": completed
        }

        running_jobs = [
            {
                "label": x.get("status"),
                "text": x.get("_name"),
                "description": x.get("_uuid")
            }
            for x in jobs_list]
        # post the data to the tipboard api

        # UNCLAIMED JOBS
        data_to_push = {
            'tile': 'just_value',
            'key': "unclaimed_jobs",
            'data': json.dumps(unclaimed_jobs),
        }
        requests.post(tipboard_url, data=data_to_push)

        # CLAIMED JOBS
        data_to_push = {
            'tile': 'just_value',
            'key': "claimed_jobs",
            'data': json.dumps(claimed_jobs),
        }
        requests.post(tipboard_url, data=data_to_push)

        # COMPLETED JOBS
        data_to_push = {
            'tile': 'just_value',
            'key': "completed_jobs",
            'data': json.dumps(completed_jobs),
        }
        requests.post(tipboard_url, data=data_to_push)

        # RUNNING JOBS
        data_to_push = {
            'tile': 'fancy_listing',
            'key': "running_jobs",
            'data': json.dumps(running_jobs),
        }
        requests.post(tipboard_url, data=data_to_push)

        # sleep for interval
        print "Posted Data.  Now Sleep."
        time.sleep(1)

        # loop


if __name__ == '__main__':
    run()
