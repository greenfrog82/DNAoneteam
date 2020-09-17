import json
import logging
import os
from datetime import datetime

import boto3
from chalice import Chalice


app = Chalice(app_name='dna')
app.log.setLevel(logging.DEBUG)


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/ping', methods=['POST'], cors=True)
def ping():
    return f'This reponse is from aws lambda - {app.current_request.json_body["msg"]}'


@app.route('/warehouse', methods=['POST'])
def warehouse():
    """
    app.current_request.json_body 형식
    {
        "eventtime" : "2020-09-10 13:45:29",
        "country": "KR",
        "source_ip" : "222.105.146.133",
        "location": {
            "lat": 37.2979833,
            "lon": 127.071765
        },
        "product": "2020 가을 신상"
    }

    ex) curl -H 'Content-Type: application/json' -d '{"country": "KR", "location": {"lat": 37.29279833, "lon": 127.071765}, "product": "iphone 12"}' -X POST https://l155m9dcql.execute-api.ap-northeast-2.amazonaws.com/api/warehouse | jq .
    """
    stream_name = os.getenv('STREAM_NAME')
    kinesis_client = boto3.client('kinesis')

    data = app.current_request.json_body
    data['eventtime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['source_ip'] = app.current_request.context['identity']['sourceIp']

    res = kinesis_client.put_record(StreamName=stream_name, PartitionKey='1', Data=json.dumps(data))
    app.log.debug(f'Response of Kinesis Client : {res}')

    return {
        "statusCode": res['ResponseMetadata']['HTTPStatusCode'],
    }

