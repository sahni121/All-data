import boto3
import csv
import botocore
def check_bucket_policy(bucket_name):
    s3 = boto3.client('s3')
    try:
        bucket_policy = s3.get_bucket_policy(Bucket=bucket_name)
        statements = bucket_policy.get('Statement', [])
        deny_actions = set()
        for statement in statements:
            if 'Effect' in statement and statement['Effect'] == 'Allow':
                if 'Principal' in statement and statement['Principal'] == {'AWS': '*'}:
                    if 'Action' in statement:
                        actions = statement['Action']
                        deny_actions.update(action for action in ["s3:DeleteBucketPolicy", "s3:PutBucketAcl", "s3:PutBucketPolicy", "s3:PutEncryptionConfiguration", "s3:PutObjectAcl"] if action in actions)
            elif 'Effect' in statement and statement['Effect'] == 'Deny':
                if 'Principal' in statement and statement['Principal'] == {'AWS': '*'}:
                    if 'Action' in statement:
                        actions = statement['Action']
                        if any(action in actions for action in ["s3:DeleteBucketPolicy", "s3:PutBucketAcl", "s3:PutBucketPolicy", "s3:PutEncryptionConfiguration", "s3:PutObjectAcl"]):
                            return False
        return len(deny_actions) == 5
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
            return True
        raise

def main():
    # Initialize Boto3 S3 client
    s3 = boto3.client('s3')

    # Get list of all S3 bucket names
    response = s3.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response['Buckets']]

    # Create a list to store bucket info
    bucket_info = []

    # Check bucket policy for each bucket
    for bucket_name in bucket_names:
    # bucket_name='1set3'
        bucket_policy_compliant = check_bucket_policy(bucket_name)
        status = 'compliant' if bucket_policy_compliant else 'non-compliant'
        bucket_info.append({'BucketName': bucket_name, 'BucketPolicyStatus': status})

    # Write bucket info to CSV file
    csv_file = 'bucket_policy_status.csv'
    with open(csv_file, mode='w', newline='') as csvfile:
        fieldnames = ['BucketName', 'BucketPolicyStatus']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for info in bucket_info:
            writer.writerow(info)

    print(f"Bucket policy status has been written to {csv_file}")

if __name__ == "__main__":
    main()
