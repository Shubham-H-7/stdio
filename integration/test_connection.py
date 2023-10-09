import json

import test_api
import test_sftp

from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

chat = ChatOpenAI(temperature=0, openai_api_key="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",
                  model="gpt-3.5-turbo")


def test_connection(input_text):
    template = (
        "Act as a testing tool for connections after converting the message with info to json with the format {JSONFORMAT} if the connection type is SFTP then host, username, password and port should be present in json. If not please ask user to provide the missing details. "
        "If the connection type is API then url, httpmethod (only POST or GET), statictoken and requestbody should be present in json. If not please ask user to provide the details.")
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    v = chat(
        chat_prompt.format_prompt(
            JSONFORMAT={'name': '', 'connectiontype': '', 'username': '', 'password': '', 'host': '', 'url': '',
                        'statictoken': '', 'httpMethod': '', 'requestbody': '', 'port': ''}, text=input_text
        ).to_messages()
    )
    try:
        v = json.loads(v.content)

        if v['connectiontype'].upper() == 'SFTP':
            return test_sftp.testSftpConnection(v['host'], v['port'], v['username'], v['password'], None)
        if v['connectiontype'].upper() == 'API':
            if type(v['requestbody']) is dict:
                request_body = v['requestbody']
            else:
                request_body = json.loads(v['requestbody'])
            return test_api.test_api_connection(v['url'], v['httpMethod'], v['statictoken'], request_body)
    except Exception as e:
        print(e)
        if type(v) is dict:
            return 'Connection failed please check your inputs'
        else:
            return v.content



