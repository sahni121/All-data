import boto3
import csv
from botocore.exceptions import ClientError

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

def check_bucket_acl(bucket_acl):
    grants = bucket_acl.get('Grants', [])
    for grant in grants:
        grantee = grant.get('Grantee', {})
        if 'URI' in grantee and grantee['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
            permission = grant.get('Permission', '')
            if permission in ['READ', 'FULL_CONTROL']:
                return True
    return False

def check_block_public_access(s3_client, bucket_name):
    try:
        response = s3_client.get_public_access_block(Bucket=bucket_name)
        return (
            response['PublicAccessBlockConfiguration']['BlockPublicAcls'] and
            response['PublicAccessBlockConfiguration']['IgnorePublicAcls'] and
            response['PublicAccessBlockConfiguration']['BlockPublicPolicy'] and
            response['PublicAccessBlockConfiguration']['RestrictPublicBuckets']
        )
    except s3_client.exceptions.NoSuchPublicAccessBlockConfiguration:
        return False
def main():
    # Initialize Boto3 S3 client
    s3 = boto3.client('s3')

    # Get list of all S3 bucket names
    response = s3.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response['Buckets']]

    # Create a list to store bucket info
    bucket_info = []

    # Check public read access for each bucket
    for bucket_name in bucket_names:
        public_access_blocked = check_block_public_access(s3, bucket_name)
        try:
            bucket_policy = s3.get_bucket_policy(Bucket=bucket_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
                bucket_policy = None
            else:
                raise
        bucket_acl = s3.get_bucket_acl(Bucket=bucket_name)
        public_read_access = check_bucket_policy(bucket_policy) or check_bucket_acl(bucket_acl)
        status = 'No'
        if not public_access_blocked and public_read_access:
            status = 'Yes'
        bucket_info.append({'BucketName': bucket_name, 'PublicReadAccess': status})

    # Write bucket info to CSV file
    csv_file = 'buckets_public_read_access.csv'
    with open(csv_file, mode='w', newline='') as csvfile:
        fieldnames = ['BucketName', 'PublicReadAccess']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for info in bucket_info:
            writer.writerow(info)

    print(f"Bucket public read access status has been written to {csv_file}")

if __name__ == "__main__":
    main()
