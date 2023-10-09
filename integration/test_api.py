import requests


def test_api_connection(api_url, http_method, bearer_token, json_body=None):
    try:
        headers = {
            'Authorization': f'Bearer {bearer_token}',
            'Content-Type': 'application/json'
        }

        if http_method.upper() == 'GET':
            response = requests.get(api_url, headers=headers)
        elif http_method.upper() == 'POST':
            if json_body is None:
                raise ValueError("JSON request body is required for POST requests.")
            response = requests.post(api_url, headers=headers, json=json_body)
        if response.status_code == 200:
            return "API Connection Successful"
        else:
            return f"API Connection Failed. Status Code: {response.status_code}"
    except Exception as e:
        return f"API Connection Failed. Error: {str(e)}"
