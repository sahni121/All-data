# import boto3
# import csv

# def check_bucket_logging(bucket_name):
#     s3 = boto3.client('s3')
#     try:
#         response = s3.get_bucket_logging(Bucket=bucket_name)
#         logging_enabled = 'LoggingEnabled' in response
#         return logging_enabled
#     except s3.exceptions.NoSuchBucketLogging:
#         return False

# def main():
#     # Initialize Boto3 S3 client
#     s3 = boto3.client('s3')

#     # Get list of all S3 bucket names
#     response = s3.list_buckets()
#     bucket_names = [bucket['Name'] for bucket in response['Buckets']]

#     # Create a list to store bucket info
#     bucket_info = []

#     # Check bucket logging for each bucket
#     for bucket_name in bucket_names:
#         bucket_logging_enabled = check_bucket_logging(bucket_name)
#         status = 'Enabled' if bucket_logging_enabled else 'Not Enabled'
#         bucket_info.append({'BucketName': bucket_name, 'ServerAccessLoggingStatus': status})

#     # Write bucket info to CSV file
#     csv_file = 'bucket_logging_status.csv'
#     with open(csv_file, mode='w', newline='') as csvfile:
#         fieldnames = ['BucketName', 'ServerAccessLoggingStatus']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for info in bucket_info:
#             writer.writerow(info)

#     print(f"Bucket logging status has been written to {csv_file}")

# if __name__ == "__main__":
#     main()




# import boto3
# import csv

# def check_bucket_logging(bucket_name):
#     s3 = boto3.client('s3')
#     try:
#         response = s3.get_bucket_logging(Bucket=bucket_name)
#         logging_enabled = 'LoggingEnabled' in response
#         return logging_enabled
#     except s3.exceptions.NoSuchBucketLogging:
#         return False
# def enable_bucket_logging(bucket_name):
#     s3 = boto3.client('s3')
#     try:
#         logging_config = {
#             'LoggingEnabled': {
#                 'TargetBucket': bucket_name,
#                 'TargetPrefix': 'logs/',
#                 'TargetGrants': [
#                     {
#                         'Grantee': {
#                             'Type': 'Group',
#                             'URI': 'http://acs.amazonaws.com/groups/s3/LogDelivery'
#                         },
#                         'Permission': 'WRITE'
#                     }
#                 ]
#             }
#         }
#         s3.put_bucket_logging(Bucket=bucket_name, BucketLoggingStatus=logging_config)
#         print(f"Enabled logging for bucket: {bucket_name}")
#     except Exception as e:
#         print(f"Error enabling logging for bucket {bucket_name}: {e}")

# def main():
#     # Initialize Boto3 S3 client
#     s3 = boto3.client('s3')

#     # Get list of all S3 bucket names
#     response = s3.list_buckets()
#     bucket_names = [bucket['Name'] for bucket in response['Buckets']]

#     # Create a list to store bucket info
#     bucket_info = []

#     # Check bucket logging for each bucket
#     # for bucket_name in bucket_names:
#     bucket_name='1set4'
#     bucket_logging_enabled = check_bucket_logging(bucket_name)
#     status = 'Enabled' if bucket_logging_enabled else 'Not Enabled'
#     bucket_info.append({'BucketName': bucket_name, 'ServerAccessLoggingStatus': status})

#     if not bucket_logging_enabled:
#             enable_bucket_logging(bucket_name)

#     # Write bucket info to CSV file
#     csv_file = 'bucket_logging_status.csv'
#     with open(csv_file, mode='w', newline='') as csvfile:
#         fieldnames = ['BucketName', 'ServerAccessLoggingStatus']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for info in bucket_info:
#             writer.writerow(info)

#     print(f"Bucket logging status has been written to {csv_file}")

# if __name__ == "__main__":
#     main()

import boto3
import csv

def check_bucket_logging(bucket_name):
    s3 = boto3.client('s3')
    try:
        response = s3.get_bucket_logging(Bucket=bucket_name)
        logging_enabled = 'LoggingEnabled' in response
        return logging_enabled
    except s3.exceptions.NoSuchBucketLogging:
        return False

def enable_bucket_logging(bucket_name):
    s3 = boto3.client('s3')
    try:
        logging_config = {
            'LoggingEnabled': {
                'TargetBucket': '1set3',
                'TargetPrefix': 'logs/',
            }
        }
        s3.put_bucket_logging(Bucket=bucket_name, BucketLoggingStatus=logging_config)
        print(f"Enabled logging for bucket: {bucket_name}")
    except Exception as e:
        print(f"Error enabling logging for bucket {bucket_name}: {e}")

def main():
    # Initialize Boto3 S3 client
    s3 = boto3.client('s3')

    # Get list of all S3 bucket names
    response = s3.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response['Buckets']]

    # Create lists to store bucket info
    initial_bucket_info = []
    updated_bucket_info = []

    # Check bucket logging for each bucket
    # for bucket_name in bucket_names:
    bucket_name='1set4'
    bucket_logging_enabled = check_bucket_logging(bucket_name)
    initial_status = 'Enabled' if bucket_logging_enabled else 'Not Enabled'
    initial_bucket_info.append({'BucketName': bucket_name, 'Status': initial_status})

    if not bucket_logging_enabled:
            enable_bucket_logging(bucket_name)
            updated_status = 'Enabled'
            updated_bucket_info.append({'BucketName': bucket_name, 'Status': updated_status})
    else:
            updated_status = initial_status

    # Write initial bucket info to CSV file
    initial_csv_file = 'initial_bucket_logging_status.csv'
    with open(initial_csv_file, mode='w', newline='') as csvfile:
        fieldnames = ['BucketName', 'Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for info in initial_bucket_info:
            writer.writerow(info)

    print(f"Initial bucket logging status has been written to {initial_csv_file}")

    # Write updated bucket info to CSV file
    updated_csv_file = 'updated_bucket_logging_status.csv'
    with open(updated_csv_file, mode='w', newline='') as csvfile:
        fieldnames = ['BucketName', 'Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for info in updated_bucket_info:
            writer.writerow(info)

    print(f"Updated bucket logging status has been written to {updated_csv_file}")

if __name__ == "__main__":
    main()
