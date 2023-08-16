import boto3
import csv
import botocore

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
    # Initialize Boto3 S3 client
    s3 = boto3.client('s3')

    # Get list of all S3 bucket names
    response = s3.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response['Buckets']]

    # Create a list to store bucket info
    bucket_info = []

    # Check cross-region replication for each bucket
    for bucket_name in bucket_names:
        bucket_replication_enabled = check_bucket_cross_region_replication(bucket_name)
        status = 'Enabled' if bucket_replication_enabled else 'Disabled'
        bucket_info.append({'BucketName': bucket_name, 'CrossRegionReplicationStatus': status})

    # Write bucket info to CSV file
    csv_file = 'bucket_replication_status.csv'
    with open(csv_file, mode='w', newline='') as csvfile:
        fieldnames = ['BucketName', 'CrossRegionReplicationStatus']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for info in bucket_info:
            writer.writerow(info)

    print(f"Bucket replication status has been written to {csv_file}")

if __name__ == "__main__":
    main()



# import boto3

# def enable_bucket_replication(bucket_name, destination_bucket_arn, iam_role_arn):
#     s3 = boto3.client('s3')
#     try:
#         replication_config = {
#             "Role": iam_role_arn,
#             "Rules": [
#                 {
#                     "Status": "Enabled",
#                     "DeleteMarkerReplication": {"Status": "Disabled"},
#                     "Priority": 1,
#                     "Filter": {},
#                     "Destination": {
#                         "Bucket": destination_bucket_arn,
#                         "StorageClass": "STANDARD"
#                     },
#                     "SourceSelectionCriteria": {"SseKmsEncryptedObjects": {"Status": "Enabled"}},
#                     "Id": "EntireBucket"
#                 }
#             ]
#         }
        
#         s3.put_bucket_replication(Bucket=bucket_name, ReplicationConfiguration=replication_config)
#         print(f"Enabled replication for bucket {bucket_name}")
#     except Exception as e:
#         print(f"Error enabling replication for bucket {bucket_name}: {e}")

# # def main():
# #     # Initialize Boto3 S3 client
# #     s3 = boto3.client('s3')

# #     # Get list of all S3 bucket names
# #     response = s3.list_buckets()
# #     bucket_names = [bucket['Name'] for bucket in response['Buckets']]

# #     # Enter the destination bucket ARN and IAM role ARN
# #     destination_bucket_arn = 'arn:aws:s3:::your-destination-bucket'
# #     iam_role_arn = 'arn:aws:iam::your-account-id:role/your-iam-role'

# #     # Enable cross-region replication for each bucket that doesn't have it enabled
# #     for bucket_name in bucket_names:
# #         replication_enabled = check_bucket_cross_region_replication(bucket_name)
# #         if not replication_enabled:
# #             enable_bucket_replication(bucket_name, destination_bucket_arn, iam_role_arn)

# # if __name__ == "__main__":
# #     main()

# def main():
#     # Initialize Boto3 S3 client
#     s3 = boto3.client('s3')

#     # Get list of all S3 bucket names
#     response = s3.list_buckets()
#     bucket_names = [bucket['Name'] for bucket in response['Buckets']]

#     # Read destination bucket ARN and IAM role ARN from environment variables
#     destination_bucket_arn = os.environ.get('DESTINATION_BUCKET_ARN')
#     iam_role_arn = os.environ.get('IAM_ROLE_ARN')

#     if not destination_bucket_arn or not iam_role_arn:
#         print("Error: Destination bucket ARN or IAM role ARN not provided.")
#         return

#     # Enable cross-region replication for each bucket that doesn't have it enabled
#     # for bucket_name in bucket_names:
#     bucket_name='1set2'
#     replication_enabled = check_bucket_cross_region_replication(bucket_name)
#     if not replication_enabled:
#         enable_bucket_replication(bucket_name, destination_bucket_arn, iam_role_arn)

# if __name__ == "__main__":
#     main()