import boto3,csv
import pprint
def check_server_side_encryption(bucket_name):
    s3 = boto3.client('s3')
    
    # Check if server-side encryption is enabled on the bucket
    response = s3.get_bucket_encryption(Bucket=bucket_name)
    # pprint.pprint(response)
    rules = response['ServerSideEncryptionConfiguration']['Rules']
    if len(rules) > 0:
        for rule in rules:
            if 'ApplyServerSideEncryptionByDefault' in rule:
                sse_algorithm = rule['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']
                if sse_algorithm in ['AES256', 'aws:kms','aws:kms:dsse']:
                    return True
   
    # If server-side encryption is not enabled, check if the bucket policy denies PutObject requests without encryption
    try:
        
        bucket_policy = s3.get_bucket_policy(Bucket=bucket_name)
        statements = bucket_policy.get('Statement', [])
        for statement in statements:
            if statement.get('Effect') == 'Deny' and statement.get('Action') == 's3:PutObject' and \
               'Condition' in statement and 'StringNotEqualsIfExists' in statement['Condition']:
                condition = statement['Condition']
                if condition.get('aws:SecureTransport') == 'false':
                    return True
    except s3.exceptions.NoSuchBucketPolicy:
        pass

    return False

def main():
    # Initialize Boto3 S3 client
    s3 = boto3.client('s3')

    # Get list of all S3 bucket names
    response = s3.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response['Buckets']]

    # Create a list to store bucket info
    bucket_info = []

    # Check server-side encryption for each bucket
    for bucket_name in bucket_names:
        server_side_encryption_enabled = check_server_side_encryption(bucket_name)
        status = 'Enabled' if server_side_encryption_enabled else 'Not Enabled'
        bucket_info.append({'BucketName': bucket_name, 'ServerSideEncryption': status})

    # Write bucket info to CSV file
    csv_file = 'server_side_encryption_status.csv'
    with open(csv_file, mode='w', newline='') as csvfile:
        fieldnames = ['BucketName', 'ServerSideEncryption']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for info in bucket_info:
            writer.writerow(info)

    print(f"Server-side encryption status has been written to {csv_file}")


if __name__ == "__main__":
    main()


# import boto3,csv

# def enable_server_side_encryption(bucket_name):
#     s3 = boto3.client('s3')
    
#     # Check if server-side encryption is enabled on the bucket
#     response = s3.get_bucket_encryption(Bucket=bucket_name)
#     rules = response['ServerSideEncryptionConfiguration']['Rules']
#     if len(rules) > 0:
#         for rule in rules:
#             sse_algorithm = rule['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']
#             if sse_algorithm in ['AES256', 'aws:kms']:
#                 return True

#     # If server-side encryption is not enabled, enable it with AES256
#     else:
#      s3.put_bucket_encryption(
#         Bucket=bucket_name,
#         ServerSideEncryptionConfiguration={
#             'Rules': [
#                 {
#                     'ApplyServerSideEncryptionByDefault': {
#                         'SSEAlgorithm': 'AES256'
#                     }
#                 }
#             ]
#         }
#     )
#     return True

# def main():
#     # Initialize Boto3 S3 client
#     s3 = boto3.client('s3')

#     # Get list of all S3 bucket names
#     response = s3.list_buckets()
#     bucket_names = [bucket['Name'] for bucket in response['Buckets']]

#     # Create a list to store bucket info
#     bucket_info = []

#     # Check server-side encryption for each bucket
#     for bucket_name in bucket_names:
    
#         server_side_encryption_enabled = enable_server_side_encryption(bucket_name)
#         status = 'Enabled' if server_side_encryption_enabled else 'Not Enabled'
#         bucket_info.append({'BucketName': bucket_name, 'ServerSideEncryption': status})

#     # Write bucket info to CSV file
#     csv_file = 'server_side_encryption_status.csv'
#     with open(csv_file, mode='w', newline='') as csvfile:
#         fieldnames = ['BucketName', 'ServerSideEncryption']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for info in bucket_info:
#             writer.writerow(info)

#     print(f"Server-side encryption status has been written to {csv_file}")

# if __name__ == "__main__":
#     main()



# import boto3
# import csv

# def check_server_side_encryption(bucket_name):
#     s3 = boto3.client('s3')
    
#     # Check if server-side encryption is enabled on the bucket
#     response = s3.get_bucket_encryption(Bucket=bucket_name)
#     rules = response['ServerSideEncryptionConfiguration']['Rules']
#     if len(rules) > 0:
#         for rule in rules:
#             sse_algorithm = rule['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']
#             if sse_algorithm in ['AES256', 'aws:kms']:
#                 return True

#     # If server-side encryption is not enabled, check if the bucket policy denies PutObject requests without encryption
#     try:
#         bucket_policy = s3.get_bucket_policy(Bucket=bucket_name)
#         statements = bucket_policy.get('Statement', [])
#         for statement in statements:
#             if statement.get('Effect') == 'Deny' and statement.get('Action') == 's3:PutObject' and \
#                'Condition' in statement and 'StringNotEqualsIfExists' in statement['Condition']:
#                 condition = statement['Condition']
#                 if condition.get('s3:x-amz-server-side-encryption') == 'AWSKMS':
#                     return True
#     except s3.exceptions.NoSuchBucketPolicy:
#         pass

#     return False

# def enable_server_side_encryption(bucket_name, encryption_type):
#     s3 = boto3.client('s3')
    
#     # Check if server-side encryption is enabled on the bucket
#     response = s3.get_bucket_encryption(Bucket=bucket_name)
#     rules = response['ServerSideEncryptionConfiguration']['Rules']
#     if len(rules) > 0:
#         for rule in rules:
#             sse_algorithm = rule['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']
#             if sse_algorithm in ['AES256', 'aws:kms']:
#                 return True

#     # If server-side encryption is not enabled, enable it based on user choice
#     if encryption_type == 'AES256':
#         s3.put_bucket_encryption(
#             Bucket=bucket_name,
#             ServerSideEncryptionConfiguration={
#                 'Rules': [
#                     {
#                         'ApplyServerSideEncryptionByDefault': {
#                             'SSEAlgorithm': 'AES256'
#                         }
#                     }
#                 ]
#             }
#         )
#         return True
#     elif encryption_type == 'AWS-KMS':
#         kms_key_id = input("Enter the AWS KMS Key ID: ")
#         s3.put_bucket_encryption(
#             Bucket=bucket_name,
#             ServerSideEncryptionConfiguration={
#                 'Rules': [
#                     {
#                         'ApplyServerSideEncryptionByDefault': {
#                             'SSEAlgorithm': 'aws:kms',
#                             'KMSMasterKeyID': kms_key_id
#                         }
#                     }
#                 ]
#             }
#         )
#         return True
#     else:
#         print("Invalid encryption type specified.")
#         return False

# def main():
#     # Initialize Boto3 S3 client
#     s3 = boto3.client('s3')

#     # Get list of all S3 bucket names
#     response = s3.list_buckets()
#     bucket_names = [bucket['Name'] for bucket in response['Buckets']]

#     # Create a list to store bucket info before enabling server-side encryption
#     before_bucket_info = []

#     # Check server-side encryption for each bucket before enabling
#     # for bucket_name in bucket_names:
#     bucket_name='1set2'
#     server_side_encryption_enabled = check_server_side_encryption(bucket_name)
#     status = 'Enabled' if server_side_encryption_enabled else 'Not Enabled'
#     before_bucket_info.append({'BucketName': bucket_name, 'ServerSideEncryption': status})

#     # Write bucket info before enabling to CSV file
#     csv_file_before = 'server_side_encryption_status_before.csv'
#     with open(csv_file_before, mode='w', newline='') as csvfile:
#         fieldnames = ['BucketName', 'ServerSideEncryption']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for info in before_bucket_info:
#             writer.writerow(info)

#     print(f"Server-side encryption status before enabling has been written to {csv_file_before}")

#     # Create a list to store bucket info after enabling server-side encryption
#     after_bucket_info = []

#     # Enable server-side encryption for each bucket
#     for bucket_name in bucket_names:
#         print(f"Checking server-side encryption status for bucket: {bucket_name}")
#         encryption_type = input("Choose the encryption type (AES256 or AWS-KMS): ")
#         server_side_encryption_enabled = enable_server_side_encryption(bucket_name, encryption_type)
#         status = 'Enabled' if server_side_encryption_enabled else 'Not Enabled'
#         after_bucket_info.append({'BucketName': bucket_name, 'ServerSideEncryption': status})

#     # Write bucket info after enabling to CSV file
#     csv_file_after = 'server_side_encryption_status_after.csv'
#     with open(csv_file_after, mode='w', newline='') as csvfile:
#         fieldnames = ['BucketName', 'ServerSideEncryption']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for info in after_bucket_info:
#             writer.writerow(info)

#     print(f"Server-side encryption status after enabling")
# if __name__ == "__main__":
#     main()




# import boto3
# import csv

# def check_server_side_encryption(bucket_name):
#     s3 = boto3.client('s3')
#     response = s3.get_bucket_encryption(Bucket=bucket_name)
#     rules = response.get('ServerSideEncryptionConfiguration', {}).get('Rules', [])
#     if rules:
#         for rule in rules:
#             sse_algorithm = rule.get('ApplyServerSideEncryptionByDefault', {}).get('SSEAlgorithm')
#             if sse_algorithm in ['AES256', 'aws:kms']:
#                 return True
#     return False

# def enable_server_side_encryption(bucket_name, encryption_algorithm='AES256'):
#     s3 = boto3.client('s3')
#     s3.put_bucket_encryption(
#         Bucket=bucket_name,
#         ServerSideEncryptionConfiguration={
#             'Rules': [
#                 {
#                     'ApplyServerSideEncryptionByDefault': {
#                         'SSEAlgorithm': encryption_algorithm
#                     }
#                 }
#             ]
#         }
#     )

# def main():
#     # Initialize Boto3 S3 client
#     s3 = boto3.client('s3')

#     # Get list of all S3 bucket names
#     response = s3.list_buckets()
#     bucket_names = [bucket['Name'] for bucket in response['Buckets']]

#     # Create a list to store bucket info before enabling server-side encryption
#     before_bucket_info = []

#     # Check server-side encryption for each bucket before enabling
#     for bucket_name in bucket_names:
#     # bucket_name='1set2'
#         server_side_encryption_enabled = check_server_side_encryption(bucket_name)
#         status = 'Enabled' if server_side_encryption_enabled else 'Not Enabled'
#         before_bucket_info.append({'BucketName': bucket_name, 'ServerSideEncryption': status})

#     # Write bucket info to CSV file before enabling
#     csv_file_before = 'server_side_encryption_status_before.csv'
#     with open(csv_file_before, mode='w', newline='') as csvfile:
#         fieldnames = ['BucketName', 'ServerSideEncryption']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for info in before_bucket_info:
#             writer.writerow(info)

#     print(f"Server-side encryption status before enabling has been written to {csv_file_before}")

#     # Enable server-side encryption for each bucket
#     for bucket_name in bucket_names:
#         enable_server_side_encryption(bucket_name, encryption_algorithm='AES256')

#     # Create a list to store bucket info after enabling server-side encryption
#     after_bucket_info = []

#     # Check server-side encryption for each bucket after enabling
#     for bucket_name in bucket_names:
#         server_side_encryption_enabled = check_server_side_encryption(bucket_name)
#         status = 'Enabled' if server_side_encryption_enabled else 'Not Enabled'
#         after_bucket_info.append({'BucketName': bucket_name, 'ServerSideEncryption': status})

#     # Write bucket info to CSV file after enabling
#     csv_file_after = 'server_side_encryption_status_after.csv'
#     with open(csv_file_after, mode='w', newline='') as csvfile:
#         fieldnames = ['BucketName', 'ServerSideEncryption']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for info in after_bucket_info:
#             writer.writerow(info)

#     print(f"Server-side encryption status after enabling has been written to {csv_file_after}")

# if __name__ == "__main__":
#     main()
