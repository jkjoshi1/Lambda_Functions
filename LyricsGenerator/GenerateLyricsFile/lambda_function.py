import json
import os
import urllib.request

import boto3


MY_S3_BUCKET = os.environ['MY_S3_BUCKET']

s3 = boto3.resource('s3')
transcribe = boto3.client('transcribe')


def lambda_handler(event, context):
    current_job_name = event['detail']['TranscriptionJobName']
    current_job_output = transcribe.get_transcription_job(TranscriptionJobName=current_job_name)
    uri = current_job_output['TranscriptionJob']['Transcript']['TranscriptFileUri']
    print(uri)

    content = urllib.request.urlopen(uri).read().decode('UTF-8')

    print(json.dumps(content))

    data = json.loads(content)

    lyrics_text = data['results']['transcripts'][0]['transcript']

    object = s3.Object(MY_S3_BUCKET, current_job_name + '-lyrics.txt')
    object.put(Body=lyrics_text)
