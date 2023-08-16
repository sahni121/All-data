import boto3
import csv
import botocore
import os

def get_destination_bucket_arn():
    # Replace 'your-destination-bucket' with your actual destination bucket name
    destination_bucket_name = 'your-destination-bucket'
    
    s3 = boto3.client('s3')
    try:
        response = s3.get_bucket_location(Bucket=destination_bucket_name)
        region = response['LocationConstraint']
        if not region:
            region = 'us-east-1'  # Default to 'us-east-1' if region is not specified
        return f"arn:aws:s3:::{destination_bucket_name}/*"
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucket':
            raise Exception(f"Destination bucket '{destination_bucket_name}' not found.")
        else:
            raise

def get_iam_role_arn():
    # Replace 'your-iam-role' with your actual IAM role name
    iam_role_name = 'your-iam-role'
    
    iam = boto3.client('iam')
    try:
        response = iam.get_role(RoleName=iam_role_name)
        return response['Role']['Arn']
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            raise Exception(f"IAM role '{iam_role_name}' not found.")
        else:
            raise

def enable_bucket_replication(bucket_name, destination_bucket_arn, iam_role_arn):
    s3 = boto3.client('s3')
    try:
        replication_config = {
            "Role": iam_role_arn,
            "Rules": [
                {
                    "Status": "Enabled",
                    "DeleteMarkerReplication": {"Status": "Disabled"},
                    "Priority": 1,
                    "Filter": {},
                    "Destination": {
                        "Bucket": destination_bucket_arn,
                        "StorageClass": "STANDARD"
                    },
                    "SourceSelectionCriteria": {"SseKmsEncryptedObjects": {"Status": "Enabled"}},
                    "Id": "EntireBucket"
                }
            ]
        }
        
        s3.put_bucket_replication(Bucket=bucket_name, ReplicationConfiguration=replication_config)
        print(f"Enabled replication for bucket {bucket_name}")
    except Exception as e:
        print(f"Error enabling replication for bucket {bucket_name}: {e}")

def check_bucket_cross_region_replication(bucket_name):
    s3 = boto3.client('s3')
    try:
        replication_config = s3.get_bucket_replication(Bucket=bucket_name)
        if 'ReplicationConfiguration' in replication_config:
            rules = replication_config['ReplicationConfiguration'].get('Rules', [])
            return any(rule.get('Status') == 'Enabled' for rule in rules)
        else:
            return False
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ReplicationConfigurationNotFoundError':
            return False
        elif e.response['Error']['Code'] == 'NoSuchBucket':
            return False
        else:
            raise

def main():
    # Read destination bucket ARN and IAM role ARN from environment variables
    destination_bucket_arn = os.environ.get('DESTINATION_BUCKET_ARN')
    iam_role_arn = os.environ.get('IAM_ROLE_ARN')

    if not destination_bucket_arn or not iam_role_arn:
        print("Error: Destination bucket ARN or IAM role ARN not provided.")
        return

    # Initialize Boto3 S3 client
    s3 = boto3.client('s3')

    # Get list of all S3 bucket names
    response = s3.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response['Buckets']]

    # Enable cross-region replication for each bucket that doesn't have it enabled
    # for bucket_name in bucket_names:
    bucket_name='1set4'
    replication_enabled = check_bucket_cross_region_replication(bucket_name)
    if not replication_enabled:
        enable_bucket_replication(bucket_name, destination_bucket_arn, iam_role_arn)

if __name__ == "__main__":
    main()
