# import boto3
# import csv
# import botocore

# def check_bucket_ssl_policy(bucket_name):
#     s3 = boto3.client('s3')
#     try:
#         bucket_policy = s3.get_bucket_policy(Bucket=bucket_name)
#         statements = bucket_policy.get('Statement', [])
#         for statement in statements:
#             if statement.get('Condition', {}).get('Bool', {}).get('aws:SecureTransport') == 'false':
#                 return False
#     except botocore.exceptions.ClientError as e:
#         if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
#             pass
#         else:
#             raise

#     return True

# def main():
#     # Initialize Boto3 S3 client
#     s3 = boto3.client('s3')

#     # Get list of all S3 bucket names
#     response = s3.list_buckets()
#     bucket_names = [bucket['Name'] for bucket in response['Buckets']]

#     # Create a list to store bucket info
#     bucket_info = []

#     # Check SSL policy for each bucket
#     for bucket_name in bucket_names:
#         bucket_compliant = check_bucket_ssl_policy(bucket_name)
#         status = 'Compliant' if bucket_compliant else 'Non-compliant'
#         bucket_info.append({'BucketName': bucket_name, 'SSLPolicy': status})

#     # Write bucket info to CSV file
#     csv_file = 'ssl_policy_status.csv'
#     with open(csv_file, mode='w', newline='') as csvfile:
#         fieldnames = ['BucketName', 'SSLPolicy']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for info in bucket_info:
#             writer.writerow(info)

#     print(f"SSL policy status has been written to {csv_file}")

# if __name__ == "__main__":
#     main()


import boto3
import csv

def check_bucket_ssl_policy(bucket_name):
    s3 = boto3.client('s3')
    try:
        bucket_policy = s3.get_bucket_policy(Bucket=bucket_name)
        statements = bucket_policy.get('Statement', [])
        for statement in statements:
            if statement.get('Effect') == 'Deny' and statement.get('Condition', {}).get('Bool', {}).get('aws:SecureTransport') == 'false':
                return 'Non-compliant'
        return 'Compliant'
    except s3.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
            return 'Non-compliant'
        else:
            raise

def attach_ssl_policy(bucket_name):
    s3 = boto3.client('s3')
    policy = {
        "Id": "ExamplePolicy",
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowSSLRequestsOnly",
                "Action": "s3:*",
                "Effect": "Deny",
                "Resource": [
                    f"arn:aws:s3:::{bucket_name}",
                    f"arn:aws:s3:::{bucket_name}/*"
                ],
                "Condition": {
                    "Bool": {
                        "aws:SecureTransport": "false"
                    }
                },
                "Principal": "*"
            }
        ]
    }
    s3.put_bucket_policy(Bucket=bucket_name, Policy=policy)

def main():
    # Initialize Boto3 S3 client
    s3 = boto3.client('s3')

    # Get list of all S3 bucket names
    response = s3.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response['Buckets']]

    # Create a list to store bucket info for SSL policy status
    bucket_ssl_info = []

    # Check SSL policy for each bucket and attach the policy for non-compliant buckets
    for bucket_name in bucket_names:
        ssl_policy_status = check_bucket_ssl_policy(bucket_name)
        if ssl_policy_status == 'Non-compliant':
            attach_ssl_policy(bucket_name)
        bucket_ssl_info.append({'BucketName': bucket_name, 'SSLPolicyStatus': ssl_policy_status})

    # Write bucket info to CSV file for SSL policy status
    csv_file_ssl = 'bucket_ssl_policy_status.csv'
    with open(csv_file_ssl, mode='w', newline='') as csvfile:
        fieldnames_ssl = ['BucketName', 'SSLPolicyStatus']
        writer_ssl = csv.DictWriter(csvfile, fieldnames=fieldnames_ssl)
        writer_ssl.writeheader()
        for info in bucket_ssl_info:
            writer_ssl.writerow(info)

    print(f"Bucket SSL policy status has been written to {csv_file_ssl}")

    # Create a list to store bucket info for SSL policy check
    bucket_ssl_check_info = []

    # Check SSL policy for each bucket
    for bucket_name in bucket_names:
        ssl_policy_status = check_bucket_ssl_policy(bucket_name)
        bucket_ssl_check_info.append({'BucketName': bucket_name, 'SSLPolicyStatus': ssl_policy_status})

    # Write bucket info to CSV file for SSL policy check
    csv_file_ssl_check = 'bucket_ssl_policy_check.csv'
    with open(csv_file_ssl_check, mode='w', newline='') as csvfile_check:
        fieldnames_ssl_check = ['BucketName', 'SSLPolicyStatus']
        writer_ssl_check = csv.DictWriter(csvfile_check, fieldnames=fieldnames_ssl_check)
        writer_ssl_check.writeheader()
        for info in bucket_ssl_check_info:
            writer_ssl_check.writerow(info)

    print(f"Bucket SSL policy check has been written to {csv_file_ssl_check}")

if __name__ == "__main__":
    main()
