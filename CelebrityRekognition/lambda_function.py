import boto3
import os

table_name=os.environ['table_name']
s3=boto3.resource('s3')
dynamodb=boto3.resource('dynamodb')
rekognition=boto3.client('rekognition')
table=dynamodb.Table(table_name)

def lambda_handler(event,context):
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    object=s3.Object(bucket,key)
    response=rekognition.recognize_celebrities(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name' : key
                }
            }
        )
    name_list=""
    
    for i in response['CelebrityFaces']:
        print('Celebrity Name is {}'.format(i['Name']))
        print("Acccuracy of detection is {}".format(i['MatchConfidence']))
        name_list+=i['Name']+","
    
    response= table.put_item(
        Item={
            'key':key,
            'names':name_list
        }
        )
    print(response)