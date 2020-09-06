import json
import os
import sys
# import requests
import boto3

from datetime import datetime

from elasticsearch import Elasticsearch
from elasticsearch import RequestsHttpConnection
from requests_aws4auth import AWS4Auth
def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    ES_HOST = os.getenv('esEndpoint')  
    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
    session = boto3.Session(region_name='ap-northeast-2')
    credentials = session.get_credentials()
    credentials = credentials.get_frozen_credentials()
    access_key = credentials.access_key
    secret_key = credentials.secret_key
    token = credentials.token

    aws_auth = AWS4Auth(
        access_key,
        secret_key,
        'ap-northeast-2',
        'es',
        session_token=token
    )
    es_client = Elasticsearch(
        hosts = [{'host': ES_HOST, 'port': 443}],
        http_auth=aws_auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
    }      
    print('[INFO] ElasticSearch Service', json.dumps(es_client.info(), indent=2), file=sys.stderr)

    es_client.index(index="product_list", doc_type="_doc", body=doc)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
