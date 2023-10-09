import requests
import json

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

chat = ChatOpenAI(temperature=0, openai_api_key="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",
                  model="gpt-3.5-turbo")

template = (
    "If asked for inputs, get channel from user input, identify channel in the {EXISTING_DATA} and return back the values."
    "If asked for destination creation, identify the channel and convert the input to a json after mapping them to values for that channel in {EXISTING_DATA} including channel and destination name")
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)


def create_destination(user_inputs):
    try:
        api_url = 'https://unity-qa.zeotap.com/channelSettings/api/v1/destinations'
        bearer_token = 'eyJraWQiOiJsTWkzY1ktY1FxSkNoajROaFpkYjNNR3dmTmlWT2NOX1I4MU5GaUU1YWVzIiwiYWxnIjoiUlMyNTYifQ.eyJ2ZXIiOjEsImp0aSI6IkFULkR0THdDYTZjMzZJRnVJUjczVFFGbkFwel9lSTd4dVdqbzc4MU5Ua1hmSjgub2FyNXllNTEyRUJ4OWZ2c1IweDYiLCJpc3MiOiJodHRwczovL2xvZ2luLXN0YWdpbmcuemVvdGFwLmNvbS9vYXV0aDIvZGVmYXVsdCIsImF1ZCI6IjBvYTFqNDVtbGFnQ1g1Y1B6MHg3IiwiaWF0IjoxNjk2ODM3NDg1LCJleHAiOjE2OTY4NDEwODUsImNpZCI6IjBvYTFqNDVtbGFnQ1g1Y1B6MHg3IiwidWlkIjoiMDB1MWw1b2VsbzM4WTZNclgweDciLCJzY3AiOlsib2ZmbGluZV9hY2Nlc3MiLCJwcm9maWxlIiwiZW1haWwiLCJvcGVuaWQiXSwiYXV0aF90aW1lIjoxNjk1OTcxNTY3LCJzdWIiOiJzaHViaGFtLmhpcmVtYXRoQHplb3RhcC5jb20iLCJsYXN0TmFtZSI6IkhpcmVtYXRoIHwgTW9vbHlhIHwiLCJmaXJzdE5hbWUiOiJTaHViaGFtIiwiZW1haWwiOiJzaHViaGFtLmhpcmVtYXRoQHplb3RhcC5jb20ifQ.aY_RxZurxjqrZQDdxIcffOAucOJFiEg3AqjeUjdU_BX_6eQ-ADhO-uIt5JeAuServrdtmd4SQGM1BBx3bcdVIchDnABSLHRCcDiezEIL7Gl1RjfwHuNX0YgXUJv8tQO_fUDZTx2o3_M2ho7xD8mBDVfWRIbFQ0e01mII2xv9SJOCz4ZrGA-AlgF4dSBnoMUbvTLjRn52FZVDnjGJg6JlIDQc-HHHDS3FTrQ9eeNDeE7TYXuQeuLsO4lZuucsqoRml20uhA0Orkj5ix6CcHIHNr89_6f4GBgNRqrpo1dVhR_6p5MKGksdOoaPdJLIi08ZHDiDfewDluaWhaYEkPhPsQ'
        headers = {
            'Authorization': f'Bearer {bearer_token}',
            'Content-Type': 'application/json'
        }

        response = requests.post(api_url, headers=headers, json=user_inputs)
        if response.status_code == 201:
            return ("Destination created successfully")
        else:
            return (f"Destination creation failed. Status Code: {response.status_code}, message: {response.content}")
    except Exception as e:
        return (f"Destination created failed with error. Error: {str(e)}")


def get_channel_metadata():
    response_body = json.loads(requests.get(
        'http://destinations-qa.zeotap.net/channelSettings/api/internal/v1/integrationPartners/details').content)

    channel_inputs = {}
    channel_ids = {}
    channel_display_name_mappings = {}
    for channel in response_body:
        channel_name = channel['intPartnerName']
        channel_id = channel['intId']
        channel_ids[channel_name] = channel_id
        display_names = []
        display_name_mappings = {}
        if channel.get('destinationMetaData') is not None:
            for key, value in channel['destinationMetaData'].items():
                if type(value) is dict and key != 'creationMetaDataDetails':
                    display_names.append(value['name'])
                    display_name_mappings[value['name']] = key
            channel_inputs[channel_name] = display_names
            channel_display_name_mappings[channel_name] = display_name_mappings
    return {
        'channel_inputs': channel_inputs,
        'channel_ids': channel_ids,
        'channel_display_name_mappings': channel_display_name_mappings
    }


def destination(user_input):
    all_channel_metadata = get_channel_metadata()

    v = chat(
        chat_prompt.format_prompt(
            EXISTING_DATA=all_channel_metadata['channel_inputs'], text=user_input
        ).to_messages()).content
    try:
        try:
            v = json.loads(v)
        except Exception as e:
            print(str(e))
            return v

        channel = v['channel']
        int_partner_id = all_channel_metadata['channel_ids'][channel]
        mappings = all_channel_metadata['channel_display_name_mappings'][channel]
        metadata = {'integrationPartnerName': channel,
                    'intId': int_partner_id,
                    'orgId': '5406ca19-e570-480a-9415-d3abec72f8c3',
                    'productType': 'channel-platform',
                    'destinationName': v['destination_name']}

        integrationPartnerDestinationDetails = {}
        for key, value in v.items():
            if mappings.get(key) is not None:
                integrationPartnerDestinationDetails[mappings[key]] = value
        metadata['integrationPartnerDestinationDetails'] = integrationPartnerDestinationDetails
        return create_destination(metadata)
    except Exception as e:
        print(str(e))
        return ("Unexpected exception. Please try again")