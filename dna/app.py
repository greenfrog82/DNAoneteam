import json
import logging
import os
from datetime import datetime

import boto3
from chalice import Chalice


app = Chalice(app_name='dna')
app.log.setLevel(logging.DEBUG)

store_repo = {
    'jongno': {
        "country": "KR",
        "source_ip": "223.105.146.133",
        "location": {
            "lat": 37.57171827707595,
            "lon": 126.99214406051956,
        },
    },
    'gangnam': {
        "country": "KR",
        "source_ip": "221.105.146.133",
        "location": {
            "lat": 37.49832874224437,
            "lon": 127.02785335269097,
        },
    },
    'pangyo': {
        "country": "KR",
        "source_ip": "222.105.146.133",
        "location": {
            "lat": 37.394654177759406,
            "lon": 127.1111016559017,
        },
    },
}


@app.route('/warehouse', methods=['POST'], cors=True)
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

    ex) curl -H 'Content-Type: application/json' -d '{"store":"gangnam", "product": "iphone 12"}' -X POST https://l155m9dcql.execute-api.ap-northeast-2.amazonaws.com/api/warehouse | jq .
    """
    stream_name = os.getenv('STREAM_NAME')
    kinesis_client = boto3.client('kinesis')

    request_data = app.current_request.json_body

    store = store_repo[request_data['store']]
    store['eventtime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    store['product'] = request_data['product']
    # data['source_ip'] = app.current_request.context['identity']['sourceIp']

    res = kinesis_client.put_record(StreamName=stream_name, PartitionKey='1', Data=json.dumps(store))
    app.log.debug(f'Response of Kinesis Client : {res}')

    return {
        "statusCode": res['ResponseMetadata']['HTTPStatusCode'],
    }


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/ping', methods=['POST'], cors=True)
def ping():
    return f'This reponse is from aws lambda - {app.current_request.json_body["msg"]}'
