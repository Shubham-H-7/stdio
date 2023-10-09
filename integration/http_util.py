# http_util.py
import json

import requests

class HttpUtil:
    @staticmethod
    def make_post_request(url, data, headers=None):
        try:
            response = requests.post(url, data=data, headers=headers)

            if response.status_code == 200:
                return response.json()  # Assuming the response is in JSON format
            else:
                # Handle non-200 status codes here
                return None

        except requests.exceptions.RequestException as e:
            # Handle request exceptions here
            print("Error:", e)
            return None

    @staticmethod
    def make_get_request(url, params=None, headers=None):
        try:
            response = requests.get(url, params=params, headers=headers)

            if response.status_code == 200:
                return response.json()  # Assuming the response is in JSON format
            else:
                # Handle non-200 status codes here
                return None

        except requests.exceptions.RequestException as e:
            # Handle request exceptions here
            print("Error:", e)
            return None

    @staticmethod
    def make_slack_response(url, text):
        slack_message2 = {
            "response_type": "in_channel",
            "text": text
        }

        headers = {'Content-Type': 'application/json'}
        HttpUtil.make_post_request(url, data=json.dumps(slack_message2), headers = headers)
