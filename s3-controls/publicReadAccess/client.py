# import csv
# import boto3
# import botocore

# def check_block_public_access(s3_client, bucket_name):
#     try:
#         response = s3_client.get_public_access_block(Bucket=bucket_name)
#         return (
#             response['PublicAccessBlockConfiguration']['BlockPublicAcls'] and
#             response['PublicAccessBlockConfiguration']['IgnorePublicAcls'] and
#             response['PublicAccessBlockConfiguration']['BlockPublicPolicy'] and
#             response['PublicAccessBlockConfiguration']['RestrictPublicBuckets']
#         )
#     except botocore.exceptions.ClientError as e:
#         if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
#             return False
#         else:
#             raise

# def get_bucket_policy(s3_client, bucket_name):
#     try:
#         return s3_client.get_bucket_policy(Bucket=bucket_name)
#     except botocore.exceptions.ClientError as e:
#         if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
#             return None
#         else:
#             raise

# def get_bucket_acl(s3_client, bucket_name):
#     return s3_client.get_bucket_acl(Bucket=bucket_name)

# def check_bucket_policy(bucket_policy):
#     if not bucket_policy:
#         return False
#     statements = bucket_policy.get('Statement', [])
#     for statement in statements:
#         if statement.get('Effect') == 'Allow':
#             actions = statement.get('Action', [])
#             if isinstance(actions, str) and actions.startswith('s3:GetObject') and \
#                'Principal' in statement and statement['Principal'] == '*':
#                 return True
#             if isinstance(actions, list) and 's3:GetObject' in actions and \
#                'Principal' in statement and statement['Principal'] == '*':
#                 return True
#     return False

# def check_bucket_acl(bucket_acl, permission='READ'):
#     grants = bucket_acl.get('Grants', [])
#     for grant in grants:
#         grantee = grant.get('Grantee', {})
#         if 'URI' in grantee and grantee['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
#             grant_permission = grant.get('Permission', '')
#             if grant_permission == permission:
#                 return True
#     return False

# def main():
#     # Initialize Boto3 S3 client
#     s3 = boto3.client('s3')

#     # Get list of all S3 bucket names
#     response = s3.list_buckets()
#     bucket_names = [bucket['Name'] for bucket in response['Buckets']]

#     # Create a list to store bucket info
#     bucket_info = []

#     # Check Block Public Access and public read/write access for each bucket
#     for bucket_name in bucket_names:
#         block_public_access_enabled = check_block_public_access(s3, bucket_name)
#         bucket_policy = get_bucket_policy(s3, bucket_name)
#         bucket_acl = get_bucket_acl(s3, bucket_name)

#         public_read_access = check_bucket_policy(bucket_policy) or check_bucket_acl(bucket_acl)
#         public_write_access = check_bucket_acl(bucket_acl, permission='WRITE')

#         status = 'Enabled' if block_public_access_enabled else 'Disabled'
#         read_access_status = 'Yes' if public_read_access else 'No'
#         write_access_status = 'Yes' if public_write_access else 'No'

#         bucket_info.append({'BucketName': bucket_name, 'BlockPublicAccess': status, 'PublicReadAccess': read_access_status, 'PublicWriteAccess': write_access_status})

#     # Write bucket info to CSV file
#     csv_file = 'bucket_access_status.csv'
#     with open(csv_file, mode='w', newline='') as csvfile:
#         fieldnames = ['BucketName', 'BlockPublicAccess', 'PublicReadAccess', 'PublicWriteAccess']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for info in bucket_info:
#             writer.writerow(info)

#     print(f"Bucket access status has been written to {csv_file}")

# if __name__ == "__main__":
#     main()


import csv
import boto3
import botocore

def check_block_public_access(s3_client, bucket_name):
    try:
        response = s3_client.get_public_access_block(Bucket=bucket_name)
        return (
            response['PublicAccessBlockConfiguration']['BlockPublicAcls'] and
            response['PublicAccessBlockConfiguration']['IgnorePublicAcls'] and
            response['PublicAccessBlockConfiguration']['BlockPublicPolicy'] and
            response['PublicAccessBlockConfiguration']['RestrictPublicBuckets']
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
            return False
        else:
            raise

def get_bucket_policy(s3_client, bucket_name):
    try:
        return s3_client.get_bucket_policy(Bucket=bucket_name)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
            return None
        else:
            raise

def get_bucket_acl(s3_client, bucket_name):
    return s3_client.get_bucket_acl(Bucket=bucket_name)

def check_bucket_policy(bucket_policy):
    if not bucket_policy:
        return False
    statements = bucket_policy.get('Statement', [])
    for statement in statements:
        if statement.get('Effect') == 'Allow':
            actions = statement.get('Action', [])
            if isinstance(actions, str) and actions.startswith('s3:GetObject') and \
               'Principal' in statement and statement['Principal'] == '*':
                return True
            if isinstance(actions, list) and 's3:GetObject' in actions and \
               'Principal' in statement and statement['Principal'] == '*':
                return True
    return False

def check_bucket_acl(bucket_acl, permission='READ'):
    grants = bucket_acl.get('Grants', [])
    for grant in grants:
        grantee = grant.get('Grantee', {})
        if 'URI' in grantee and grantee['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
            grant_permission = grant.get('Permission', '')
            if grant_permission == permission:
                return True
    return False

def main():
    # Initialize Boto3 S3 client
    s3 = boto3.client('s3')

    # Get list of all S3 bucket names
    response = s3.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response['Buckets']]

    # Create a list to store bucket info
    bucket_info = []

    # Check Block Public Access and public read/write access for each bucket
    for bucket_name in bucket_names:
        block_public_access_enabled = check_block_public_access(s3, bucket_name)
        bucket_policy = get_bucket_policy(s3, bucket_name)
        bucket_acl = get_bucket_acl(s3, bucket_name)

        public_read_access = check_bucket_policy(bucket_policy) or check_bucket_acl(bucket_acl)
        public_write_access = check_bucket_acl(bucket_acl, permission='WRITE')

        status = 'Enabled' if block_public_access_enabled else 'Disabled'
        read_access_status = 'Yes' if public_read_access else 'No'
        write_access_status = 'Yes' if public_write_access else 'No'

        bucket_info.append({'BucketName': bucket_name, 'BlockPublicAccess': status, 'PublicReadAccess': read_access_status, 'PublicWriteAccess': write_access_status})

    # Write bucket info to CSV file
    csv_file = 'bucket_access_status.csv'
    with open(csv_file, mode='w', newline='') as csvfile:
        fieldnames = ['BucketName', 'BlockPublicAccess', 'PublicReadAccess', 'PublicWriteAccess']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for info in bucket_info:
            writer.writerow(info)

    print(f"Bucket access status has been written to {csv_file}")

if __name__ == "__main__":
    main()

