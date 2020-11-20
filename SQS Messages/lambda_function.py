import os
import boto3
import json
from datetime import datetime

sqs=boto3.resource('sqs')
dynamodb=boto3.resource('dynamodb')
TABLE_NAME=os.environ['TABLE_NAME']
QUEUE_URL=os.environ['QUEUE_URL']
table=dynamodb.Table(TABLE_NAME)

def lambda_handler(event,context):
    
    for message in sqs.Queue(QUEUE_URL).receive_messages(MaxNumberOfMessages=10):
        response=table.put_item(Item={
            'MessageId':message.message_id,
            'body':message.body,
            'timestamp':datetime.now().isoformat()
            }
        )
        print('Wrote message:',json.dumps(response))
        message.delete()
        print('deleted message:',messagemessage_id)