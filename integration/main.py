import threading
import requests
from flask import Flask, request, jsonify
import test_connection
import destination
import integrAI

app = Flask(__name__)

# Define allowed and channels
allowed_users = ["shubham.hiremath"]
allowed_channels = ["hackathon-stdio", "hackathon2023-integr8"]


@app.route('/slack/command/destination', methods=['POST'])
def slack_command_destination():
    data = request.form
    response_url = data.get('response_url')
    text_value = data.get('text', '')
    channel_name = data.get('channel_name')
    user_name = data.get('user_name')

    # Check if user and channel are allowed
    if user_name not in allowed_users or channel_name not in allowed_channels:
        return jsonify(
            {'response_type': 'ephemeral', 'text': 'You are not authorized to use this bot in this channel.'})

    my_thread = threading.Thread(target=handle_request_destination, args=(text_value, response_url))

    my_thread.start()

    return jsonify({'response_type': 'in_channel', 'text': 'Your request is processing...'})


@app.route('/slack/command/test', methods=['POST'])
def slack_command_test_connection():
    data = request.form
    response_url = data.get('response_url')
    text_value = data.get('text', '')
    channel_name = data.get('channel_name')
    user_name = data.get('user_name')

    # Check if user and channel are allowed
    if user_name not in allowed_users or channel_name not in allowed_channels:
        return jsonify(
            {'response_type': 'ephemeral', 'text': 'You are not authorized to use this bot in this channel.'})

    my_thread = threading.Thread(target=handle_request_test_connection, args=(text_value, response_url))

    my_thread.start()

    return jsonify({'response_type': 'in_channel', 'text': 'Your request is processing...'})


@app.route('/slack/command', methods=['POST'])
def slack_command_integrAI():
    data = request.form
    response_url = data.get('response_url')
    text_value = data.get('text', '')
    print(data)
    channel_name = data.get('channel_name')
    user_name = data.get('user_name')

    # Check if user and channel are allowed
    if user_name not in allowed_users or channel_name not in allowed_channels:
        return jsonify(
            {'response_type': 'ephemeral', 'text': 'You are not authorized to use this bot in this channel.'})

    my_thread = threading.Thread(target=handle_request_integrAI, args=(text_value, response_url))

    my_thread.start()

    return jsonify({'response_type': 'in_channel', 'text': 'Your request is processing...'})


def handle_request_integrAI(text_value, url):
    try:
        # Generate the actual response for IntegrAI
        response_text = integrAI.chat_bot_create_integration(text_value)

        # Send the response message
        response = requests.post(url, json={'response_type': 'in_channel', 'text': response_text})

        print(response.status_code)
    except Exception as e:
        # Handle any errors that occur during processing
        print(e)


def handle_request_destination(text_value, url):
    try:
        # Generate the actual response for destination
        response_text = destination.destination(text_value)

        # Send the response message
        response = requests.post(url, json={'response_type': 'in_channel', "text": response_text})

        print(response.status_code)
    except Exception as e:
        # Handle any errors that occur during processing
        print(e)


def handle_request_test_connection(text_value, url):
    try:
        # Generate the actual response for test_connection
        response_text = test_connection.test_connection(text_value)

        # Send the response message
        response = requests.post(url, json={'response_type': 'in_channel', "text": response_text})

        print(response.status_code)
    except Exception as e:
        # Handle any errors that occur during processing
        print(e)


if __name__ == '__main__':
    app.run(debug=True)
