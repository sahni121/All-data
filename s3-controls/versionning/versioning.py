import boto3
import csv
from botocore.exceptions import ClientError

def check_bucket_versioning(bucket_name):
    s3 = boto3.client('s3')
    try:
        response = s3.get_bucket_versioning(Bucket=bucket_name)
        versioning_status = response.get('Status')
        return versioning_status == 'Enabled'
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucket':
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

    # Check versioning status for each bucket
    for bucket_name in bucket_names:
        versioning_enabled = check_bucket_versioning(bucket_name)
        bucket_info.append({'BucketName': bucket_name, 'VersioningStatus': 'Enabled' if versioning_enabled else 'Not Enabled'})

    # Write bucket info to CSV file
    csv_file = 'bucket_versioning_status.csv'
    with open(csv_file, mode='w', newline='') as csvfile:
        fieldnames = ['BucketName', 'VersioningStatus']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for info in bucket_info:
            writer.writerow(info)

    print(f"Bucket versioning status has been written to {csv_file}")

if __name__ == "__main__":
    main()
