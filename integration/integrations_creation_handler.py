import json

from http_util import HttpUtil


class IntegrationsCreationHandler:

    token = 'Bearer eyJraWQiOiJsTWkzY1ktY1FxSkNoajROaFpkYjNNR3dmTmlWT2NOX1I4MU5GaUU1YWVzIiwiYWxnIjoiUlMyNTYifQ.eyJ2ZXIiOjEsImp0aSI6IkFULkR0THdDYTZjMzZJRnVJUjczVFFGbkFwel9lSTd4dVdqbzc4MU5Ua1hmSjgub2FyNXllNTEyRUJ4OWZ2c1IweDYiLCJpc3MiOiJodHRwczovL2xvZ2luLXN0YWdpbmcuemVvdGFwLmNvbS9vYXV0aDIvZGVmYXVsdCIsImF1ZCI6IjBvYTFqNDVtbGFnQ1g1Y1B6MHg3IiwiaWF0IjoxNjk2ODM3NDg1LCJleHAiOjE2OTY4NDEwODUsImNpZCI6IjBvYTFqNDVtbGFnQ1g1Y1B6MHg3IiwidWlkIjoiMDB1MWw1b2VsbzM4WTZNclgweDciLCJzY3AiOlsib2ZmbGluZV9hY2Nlc3MiLCJwcm9maWxlIiwiZW1haWwiLCJvcGVuaWQiXSwiYXV0aF90aW1lIjoxNjk1OTcxNTY3LCJzdWIiOiJzaHViaGFtLmhpcmVtYXRoQHplb3RhcC5jb20iLCJsYXN0TmFtZSI6IkhpcmVtYXRoIHwgTW9vbHlhIHwiLCJmaXJzdE5hbWUiOiJTaHViaGFtIiwiZW1haWwiOiJzaHViaGFtLmhpcmVtYXRoQHplb3RhcC5jb20ifQ.aY_RxZurxjqrZQDdxIcffOAucOJFiEg3AqjeUjdU_BX_6eQ-ADhO-uIt5JeAuServrdtmd4SQGM1BBx3bcdVIchDnABSLHRCcDiezEIL7Gl1RjfwHuNX0YgXUJv8tQO_fUDZTx2o3_M2ho7xD8mBDVfWRIbFQ0e01mII2xv9SJOCz4ZrGA-AlgF4dSBnoMUbvTLjRn52FZVDnjGJg6JlIDQc-HHHDS3FTrQ9eeNDeE7TYXuQeuLsO4lZuucsqoRml20uhA0Orkj5ix6CcHIHNr89_6f4GBgNRqrpo1dVhR_6p5MKGksdOoaPdJLIi08ZHDiDfewDluaWhaYEkPhPsQ'

    my_map = {"uploadChannelMetadata": "http://upload-configuration-qa.zeotap.net/ops-ui-integration/api/v1/uploadChannelMetadata", "addUploaderConfigs": "http://upload-configuration-qa.zeotap.net/ops-ui-integration/api/v1/addUploaderConfigs", "midmapping" : "http://destinations-qa.zeotap.net/channelSettings/api/internal/v1/mid", "actions":"https://unity-qa.zeotap.com/channelSettings/api/v2/actions", "uploadChannelConfig" : "http://upload-configuration-qa.zeotap.net/ops-ui-integration/api/v1/addUploaderConfigs"}

    @staticmethod
    def create_integration(type, data, ai_response):
        try:
            api_url = IntegrationsCreationHandler.my_map[type]
            headers = {'Content-Type' : 'application/json'}
            data_json = json.loads(data)
            response_data = HttpUtil.make_post_request(api_url, data, headers)

            if response_data:
                print("Response:", response_data)
                IntegrationsCreationHandler.add_mid_mapping(data, ai_response)
                IntegrationsCreationHandler.add_default_action(data, ai_response)
                IntegrationsCreationHandler.add_configs(data, ai_response)
            else:
                print("Integration creation request failed.")
                return "Hey, failed creating the integration, please retry..."


        except Exception as e:
            return "Hey, failed creating the integration, please retry..."
        return "Hey, integration named " + data_json.get("integrationPartnerMetadata").get("intPartnerName") + " created successfully"

    def add_mid_mapping(data, ai_response):
        headers = {'Content-Type' : 'application/json'}
        for k,v in ai_response.get("midmappings").items() :
            displayName = k
            idName = v
            mid_map_body = '{ "name": "$_ID_NAME", "displayName": "$_DISPLAY_NAME", "intPartnerId": $_INTEGRATION_PARTNER_ID, "envId": 3, "countryIds": [ 0 ], "monetizationId": "$_ID_NAME", "idGroup": "Offline" }'
            data_json = json.loads(data)
            mid_map_body = mid_map_body.replace("$_INTEGRATION_PARTNER_ID", data_json.get("integrationPartnerMetadata").get("intId"))
            mid_map_body = mid_map_body.replace("$_ID_NAME", idName)
            mid_map_body = mid_map_body.replace("$_DISPLAY_NAME", displayName)
            HttpUtil.make_post_request(IntegrationsCreationHandler.my_map["midmapping"],mid_map_body, headers)

    def add_default_action(data, ai_response):
        headers = {'Content-Type' : 'application/json','Authorization' : IntegrationsCreationHandler.token}
        data_json = json.loads(data)
        default_action = '{ "actionName": "Attributes & Identifiers Action for $_INTEGRATION_PARTNER_ID", "isDefault": true, "defaultMapping": {}, "intPartnerId": $_INTEGRATION_PARTNER_ID, "fileType": "json", "actionType": "marTech", "productType": [ "Connect", "Audience" ], "actionMetadata": { "description": "This action will support attributes and identifiers mapping." }, "mappingMetadata": { } }'
        default_action = default_action.replace("$_INTEGRATION_PARTNER_ID", data_json.get("integrationPartnerMetadata").get("intId"))
        HttpUtil.make_post_request(IntegrationsCreationHandler.my_map["actions"],default_action, headers)

    def add_configs(data, ai_response):
        headers = {'Content-Type' : 'application/json'}
        data_json = json.loads(data)
        configs = '{ "intId": $_INTEGRATION_PARTNER_ID, "configMap": { "Upload": { "uploadType": "API", "uploadFormat": { "apiDetails": { "uploadUrl": "$_URL", "apiType": "POST", "headers": { "Authorization": "${clientId}" } }, "requestBody": $_REQUEST_BODY, "requestBodyType": "JSON", "batchSizeType": "LIST", "batchSize": 10000 } } }, "steps": { "Upload": [ "Upload" ] } }'
        configs = configs.replace("$_INTEGRATION_PARTNER_ID", data_json.get("integrationPartnerMetadata").get("intId"))
        configs = configs.replace("$_URL", ai_response.get("uploadMetaData").get("url"))
        configs = configs.replace("$_REQUEST_BODY", json.dumps(ai_response.get("uploadMetaData").get("requestBody")))
        HttpUtil.make_post_request(IntegrationsCreationHandler.my_map["uploadChannelConfig"], configs, headers)