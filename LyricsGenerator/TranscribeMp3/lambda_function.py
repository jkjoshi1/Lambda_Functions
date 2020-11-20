import boto3

s3 = boto3.client('s3')
transcribe = boto3.client('transcribe')


def lambda_handler(event, context):

    for record in event['Records']:
        source_bucket = record['s3']['bucket']['name']
        object_key = record['s3']['object']['object_key']
        object_url = "https://s3.amazonaws.com/{0}/{1}".format(source_bucket, object_key)
        response = transcribe.start_transcription_job(
            TranscriptionJobName='MyTranscriptionJob',
            Media={'MediaFileUri': object_url},
            MediaFormat='mp3',
            LanguageCode='en-US'
        )
        print(response)
