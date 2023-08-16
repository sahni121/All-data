import boto3
import csv
from botocore.exceptions import ClientError

def check_bucket_lifecycle(bucket_name):
    s3 = boto3.client('s3')
    try:
        response = s3.get_bucket_lifecycle_configuration(Bucket=bucket_name)
        rules = response.get('Rules', [])
        return len(rules) > 0
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucket':
            return False
        elif e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
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
        has_lifecycle_policy = check_bucket_lifecycle(bucket_name)
        bucket_info.append({'BucketName': bucket_name, 'LifecyclePolicyConfigured': has_lifecycle_policy})

    # Write bucket info to CSV file
    csv_file = 'bucket_lifecycle_status.csv'
    with open(csv_file, mode='w', newline='') as csvfile:
        fieldnames = ['BucketName', 'LifecyclePolicyConfigured']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for info in bucket_info:
            writer.writerow(info)

    print(f"Bucket lifecycle policy status has been written to {csv_file}")

if __name__ == "__main__":
    main()
