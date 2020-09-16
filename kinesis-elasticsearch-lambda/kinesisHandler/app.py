import json
import os
import sys
# import requests
import boto3
import base64
import socket

from datetime import datetime

from elasticsearch import Elasticsearch
from elasticsearch import RequestsHttpConnection

import requests
def lambda_handler(event, context):

    ES_HOST = os.getenv('esEndpoint')  
    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
    es_client = Elasticsearch(
        hosts = [{'host': ES_HOST, 'port': 443}],
        # http_auth=('interpark', 'Interpark1!'),
        use_ssl=True,
        # verify_certs=True,
        #connection_class=RequestsHttpConnection
    )
    # mapper = {
    #             "mappings": {
    #                 "properties": {
    #                 "loc":    { "type": "geo_point" }
    #                 }
    #             }   
    #         }
    # es_client.indices.create(index='loc', body =mapper, ignore=400)
 
    print(event)
    #es_client.index(index="loca",  body=json.dumps(loc))
    for record in event['Records']:
        id = record['eventID']
        timestamp = record['kinesis']['approximateArrivalTimestamp']
        
        # Kinesis data is base64-encoded, so decode here
        message = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        #ret = requests.get(f"http://api.ipstack.com/{message}?access_key=fe3488be900ea0c9a6d46704acaa77b5")
        
        print(message)
        try:
            es_client.index(index="dna", body=message)
        except Exception as e:
            print(e)



        # Create the JSON document
        #document = { "id": id, "timestamp": timestamp, "message": message }
        # Index the document


        # r = requests.put(url + id, auth=awsauth, json=document, headers=headers)
        # count += 1

    # doc = {
    # 'author': 'kimchy',
    # 'text': 'Elasticsearch: cool. bonsai cool.',
    # 'timestamp': datetime.now(),
    # }      
    print('[INFO] ElasticSearch Service', json.dumps(es_client.info(), indent=2), file=sys.stderr)

    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
