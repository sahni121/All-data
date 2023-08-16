import boto3

def get_s3_client():
    return boto3.client('s3')

def get_bucket_names(s3_client):
    response = s3_client.list_buckets()
    return [bucket['Name'] for bucket in response['Buckets']]
