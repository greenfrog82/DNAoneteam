import json
import os
import sys
# import requests
import boto3
import datetime
import decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return float(o)
        return super(DecimalEncoder, self).default(o)
        
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
    client = boto3.resource("dynamodb", "ap-northeast-2")
    table = client.Table('dna_seller')
    key = {}
    key['id'] = 1
    print(key)
    response = table.get_item(Key=key)
    print(response['Item'])
    response['Item']["eventtime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    data = {}
    data['eventtime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['source_ip'] = response['Item']['source_ip']
    data['country'] = response['Item']['country']

    stream_name = os.getenv("StreamName")
    kinesis_client = boto3.client('kinesis',"ap-northeast-2")
    print(json.dumps(response['Item'], cls=DecimalEncoder))
    res = kinesis_client.put_record(StreamName=stream_name, PartitionKey='1', Data= json.dumps(response['Item'], cls=DecimalEncoder))

    return {
        "statusCode": 200,
        "body": response,
    }
