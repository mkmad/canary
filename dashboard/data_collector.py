import datetime
import json
import time
import requests


def run():

    tipboard_api_key = "b721f623a67441d68237eb1724f8a3cb"
    tipboard_api_version = "v0.1"
    tipboard_host = "http://localhost:7272"
    tipboard_url = "{0}/api/{1}/{2}/push".format(
        tipboard_host, tipboard_api_version, tipboard_api_key)

    print("Starting Canary Dashboard Data Collector")

    while True:
        print "Posting Data..."

        # request data from the Canary API

        # parse the data for the various supported tiles
        unclaimed_jobs = {
            "title": "Unclaimed Jobs",
            "description": "",
            "just-value": datetime.datetime.now().strftime('%S')
        }

        claimed_jobs = {
            "title": "Claimed Jobs",
            "description": "",
            "just-value": "44"
        }

        completed_jobs = {
            "title": "Completed Jobs",
            "description": "",
            "just-value": "2"
        }

        # post the data to the tipboard api
        data_to_push = {
            'tile': 'just_value',
            'key': "claimed_jobs",
            'data': json.dumps(unclaimed_jobs),
        }
        requests.post(tipboard_url, data=data_to_push)

        data_to_push = {
            'tile': 'just_value',
            'key': "unclaimed_jobs",
            'data': json.dumps(claimed_jobs),
        }
        requests.post(tipboard_url, data=data_to_push)

        data_to_push = {
            'tile': 'just_value',
            'key': "completed_jobs",
            'data': json.dumps(completed_jobs),
        }
        requests.post(tipboard_url, data=data_to_push)

        # sleep for interval
        print "Posted Data.  Now Sleep."
        time.sleep(1)

        # loop


if __name__ == '__main__':
    run()
