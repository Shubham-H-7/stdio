import json
import random
import sys
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from integrations_creation_handler import IntegrationsCreationHandler


def generate_int_id():
    return str(random.randint(3000, 3999))


class IntegrAI:
    private_key = "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"
    chat = None
    chat_prompt = None
    loaded_data = None
    mid_mappings = None

    def __init__(self):
        IntegrAI.chat = ChatOpenAI(temperature=0, openai_api_key=IntegrAI.private_key,
                                   model="gpt-3.5-turbo")
        template = (
            "Act as a integration platform, convert the message with info to json with the format {JSONFORMAT}. While filling the json populate mid ids based on {MIDMAPPINGFORMAT} as it is in {MIDMAPPINGFORMAT} and populate only mid ids which user asks. Under destinationMetaData if you receive only one field name it's key as clientId by default. Only respond back in json format provided. Also ensure user to have token, url and request body. If not please ask user to provide the details")
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)
        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
        IntegrAI.chat_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )
        with open("venv/bin/file2.json", "r") as json_file:
            IntegrAI.loaded_data = json.load(json_file)
        with open("venv/bin/file4.json", "r") as json_file:
            IntegrAI.mid_mappings = json.load(json_file)

    def chat_bot_create_integration(self, user_input):
        v = IntegrAI.chat(
            IntegrAI.chat_prompt.format_prompt(
                JSONFORMAT=IntegrAI.loaded_data, MIDMAPPINGFORMAT=IntegrAI.mid_mappings, text=user_input
            ).to_messages()
        )
        try:
            parsed_json = json.loads(v.content)
            _static_access_token_d_metadata = '{ "$_CLIENT_ID": { "secret": true, "type": "text", "name": "$_STATIC_ACCESS_TOKEN" } }'
            for k, v in parsed_json.get("destinationMetaData").items():
                _static_access_token_d_metadata = _static_access_token_d_metadata.replace("$_CLIENT_ID", k)
                _static_access_token_d_metadata = _static_access_token_d_metadata.replace("$_STATIC_ACCESS_TOKEN", v)
            intId = generate_int_id()
            data = '{ "channelTemplate": {}, "integrationType": "Batch", "integrationPartnerMetadata": { "intId": "$_INTEGRATION_ID", "channelId": "108", "intPartnerName": "$_INTEGRATION_NAME", "destinationMetaData": $_DESTINATION_METADATA, "channelType": 1, "destinationType": "Creation" } }'
            data = data.replace("$_INTEGRATION_NAME", parsed_json.get("name"))
            data = data.replace("$_DESTINATION_METADATA", _static_access_token_d_metadata)
            data = data.replace("$_INTEGRATION_ID", intId)
            return IntegrationsCreationHandler.create_integration("uploadChannelMetadata", data, parsed_json)
        except Exception as e:
            return v.content
