
# import boto3
# import csv
# from botocore.exceptions import ClientError

# def check_bucket_lifecycle(bucket_name):
#     s3 = boto3.client('s3')
#     try:
#         response = s3.get_bucket_lifecycle_configuration(Bucket=bucket_name)
#         rules = response.get('Rules', [])
#         return len(rules) > 0
#     except ClientError as e:
#         if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
#             return False
#         else:
#             raise

# def configure_bucket_lifecycle(bucket_name):
#     s3 = boto3.client('s3')
#     try:
#         lifecycle_config = {
#             'Rules': [
#                 {
#                     'ID': 'SampleRule',
#                     'Status': 'Enabled',
#                     'Prefix': '',
#                     'Expiration': {
#                         'Days': 30
#                     }
#                 }
#             ]
#         }
#         s3.put_bucket_lifecycle_configuration(Bucket=bucket_name, LifecycleConfiguration=lifecycle_config)
#         print(f"Configured lifecycle policy for bucket: {bucket_name}")
#     except Exception as e:
#         print(f"Error configuring lifecycle policy for bucket {bucket_name}: {e}")

# def enable_bucket_versioning(bucket_name):
#     s3 = boto3.client('s3')
#     try:
#         s3.put_bucket_versioning(Bucket=bucket_name, VersioningConfiguration={'Status': 'Enabled'})
#         print(f"Enabled versioning for bucket: {bucket_name}")
#     except Exception as e:
#         print(f"Error enabling versioning for bucket {bucket_name}: {e}")

# def main():
#     # Initialize Boto3 S3 client
#     s3 = boto3.client('s3')

#     # Get list of all S3 bucket names
#     response = s3.list_buckets()
#     bucket_names = [bucket['Name'] for bucket in response['Buckets']]

#     # Create a list to store bucket info
#     bucket_info = []

#     # Check and remediate lifecycle policy for each bucket
#     # for bucket_name in bucket_names:
#     bucket_name='1set6'
#     bucket_versioning = s3.get_bucket_versioning(Bucket=bucket_name)
#     if bucket_versioning.get('Status') != 'Enabled':
#         enable_bucket_versioning(bucket_name)
#     has_lifecycle_policy = check_bucket_lifecycle(bucket_name)
#     if bucket_versioning.get('Status') == 'Enabled' and not has_lifecycle_policy:
#         configure_bucket_lifecycle(bucket_name)
#         has_lifecycle_policy = True
#     bucket_info.append({'BucketName': bucket_name, 'VersioningStatus': 'Enabled', 'LifecyclePolicyConfigured': has_lifecycle_policy})

#     # Write bucket info to CSV file
#     csv_file = 'bucket_lifecycle_status.csv'
#     with open(csv_file, mode='w', newline='') as csvfile:
#         fieldnames = ['BucketName', 'VersioningStatus', 'LifecyclePolicyConfigured']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for info in bucket_info:
#             writer.writerow(info)

#     print(f"Bucket lifecycle status has been written to {csv_file}")

# if __name__ == "__main__":
#     main()






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
        if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
            return False
        else:
            raise

def configure_bucket_lifecycle(bucket_name):
    s3 = boto3.client('s3')
    try:
        lifecycle_config = {
            'Rules': [
                {
                    'ID': 'SampleRule',
                    'Status': 'Enabled',
                    'Prefix': '',
                    'Expiration': {
                        'Days': 30
                    }
                }
            ]
        }
        s3.put_bucket_lifecycle_configuration(Bucket=bucket_name, LifecycleConfiguration=lifecycle_config)
        print(f"Configured lifecycle policy for bucket: {bucket_name}")
    except Exception as e:
        print(f"Error configuring lifecycle policy for bucket {bucket_name}: {e}")

def enable_versioning_and_configure_lifecycle(bucket_name):
    s3 = boto3.client('s3')
    try:
        # Enable versioning
        s3.put_bucket_versioning(Bucket=bucket_name, VersioningConfiguration={'Status': 'Enabled'})
        print(f"Enabled versioning for bucket: {bucket_name}")
        
        # Configure lifecycle policy
        configure_bucket_lifecycle(bucket_name)
        
        print(f"Versioning enabled and lifecycle policy configured for bucket: {bucket_name}")
    except Exception as e:
        print(f"Error enabling versioning and configuring lifecycle policy for bucket {bucket_name}: {e}")

def main():
    # Initialize Boto3 S3 client
    s3 = boto3.client('s3')

    # Get list of all S3 bucket names
    response = s3.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response['Buckets']]

    # Create a list to store bucket info
    bucket_info = []

    # Check and remediate versioning and lifecycle policy for each bucket
    # for bucket_name in bucket_names:
    bucket_name='1set7'
    enable_versioning_and_configure_lifecycle(bucket_name)
    has_lifecycle_policy = check_bucket_lifecycle(bucket_name)
    bucket_info.append({'BucketName': bucket_name, 'VersioningStatus': 'Enabled', 'LifecyclePolicyConfigured': has_lifecycle_policy})

    # Write bucket info to CSV file
    csv_file = 'bucket_lifecycle_status.csv'
    with open(csv_file, mode='w', newline='') as csvfile:
        fieldnames = ['BucketName', 'VersioningStatus', 'LifecyclePolicyConfigured']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for info in bucket_info:
            writer.writerow(info)

    print(f"Bucket lifecycle status has been written to {csv_file}")

if __name__ == "__main__":
    main()
