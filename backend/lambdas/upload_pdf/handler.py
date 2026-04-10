import json
import boto3
import os

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Get the uploaded file details from the event
        bucket_name = os.environ['S3_BUCKET']
        file_key = event['Records'][0]['s3']['object']['key']
        
        # Log the file upload
        print(f"File uploaded: {file_key} to bucket: {bucket_name}")

        return {
            'statusCode': 200,
            'body': json.dumps('File uploaded successfully!')
        }
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error uploading file.')
        }