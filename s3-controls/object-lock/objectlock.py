import boto3
import csv
from botocore.exceptions import ClientError

def check_bucket_object_lock(bucket_name):
    s3 = boto3.client('s3')
    try:
        response = s3.get_object_lock_configuration(Bucket=bucket_name)
        object_lock_configuration = response.get('ObjectLockConfiguration', {})
        object_lock_enabled = object_lock_configuration.get('ObjectLockEnabled')
        
        if object_lock_enabled:
            return 'Object Lock is enabled'
        else:
            return 'Object Lock is not enabled'
    except ClientError as e:
        if e.response['Error']['Code'] == 'ObjectLockConfigurationNotFoundError':
            return 'Object Lock configuration does not exist'
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

    # Check Object Lock status for each bucket
    for bucket_name in bucket_names:
        object_lock_status = check_bucket_object_lock(bucket_name)
        bucket_info.append({'BucketName': bucket_name, 'ObjectLockStatus': object_lock_status})

    # Write bucket info to CSV file
    csv_file = 'bucket_object_lock_status.csv'
    with open(csv_file, mode='w', newline='') as csvfile:
        fieldnames = ['BucketName', 'ObjectLockStatus']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for info in bucket_info:
            writer.writerow(info)

    print(f"Bucket Object Lock status has been written to {csv_file}")

if __name__ == "__main__":
    main()
