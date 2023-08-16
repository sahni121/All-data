import boto3
import csv
from botocore.exceptions import ClientError
import pprint

def check_bucket_lifecycle(bucket_name):
    s3 = boto3.client('s3')
    try:
        response = s3.get_bucket_lifecycle_configuration(Bucket=bucket_name)
        # pprint.pprint(response)
        rules = response.get('Rules', [])
        return len(rules) > 0
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
            return False
        else:
            raise

def main():
    # Initialize Boto3 S3 client
    s3 = boto3.client('s3')

    # Get list of all S3 bucket names
    response = s3.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response['Buckets']]

    # Create a list to store bucket info
    bucket_info = []

    # Check lifecycle policy for each bucket
    for bucket_name in bucket_names:
        bucket_versioning = s3.get_bucket_versioning(Bucket=bucket_name)
        if bucket_versioning.get('Status') == 'Enabled':
            has_lifecycle_policy = check_bucket_lifecycle(bucket_name)
            bucket_info.append({'BucketName': bucket_name, 'VersioningStatus': 'Enabled', 'LifecyclePolicyConfigured': has_lifecycle_policy})
        else:
            bucket_info.append({'BucketName': bucket_name, 'VersioningStatus': 'Not Enabled', 'LifecyclePolicyConfigured': False})

    # Write bucket info to CSV file
    csv_file = 'bucket_lifecycle_status.csv'
    with open(csv_file, mode='w', newline='\n') as csvfile:
        fieldnames = ['BucketName', 'VersioningStatus', 'LifecyclePolicyConfigured']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for info in bucket_info:
            writer.writerow(info)

    print(f"Bucket lifecycle status has been written to {csv_file}")

if __name__ == "__main__":
    main()

