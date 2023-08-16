import boto3
import json
from botocore.exceptions import ClientError

def remove_denied_actions_from_policy(bucket_name):
    s3 = boto3.client('s3')
    
    try:
        # Get the existing bucket policy
        response = s3.get_bucket_policy(Bucket=bucket_name)
        bucket_policy = json.loads(response['Policy'])

        # Extract the statements from the bucket policy
        statements = bucket_policy['Statement']

        # Filter statements that contain denied actions for other AWS accounts
        filtered_statements = [statement for statement in statements if 'Deny' in statement['Effect']
                               and 'Principal' in statement and statement['Principal'] == '*'
                               and any(action in statement['Action'] for action in
                                       ['s3:DeleteBucketPolicy', 's3:PutBucketAcl', 's3:PutBucketPolicy',
                                        's3:PutEncryptionConfiguration', 's3:PutObjectAcl'])]

        # Remove the filtered statements from the bucket policy
        for statement in filtered_statements:
            statements.remove(statement)

        # Save the modified bucket policy
        updated_policy = json.dumps(bucket_policy)
        s3.put_bucket_policy(Bucket=bucket_name, Policy=updated_policy)
        
        print(f"Bucket policy for '{bucket_name}' has been updated to remove denied actions for other AWS accounts.")
    
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
            print(f"No bucket policy found for '{bucket_name}'. No remediation needed.")
        else:
            print(f"An error occurred: {e}")

def main():
    # Replace 'your_bucket_name' with the actual name of your S3 bucket
    bucket_name = 'your_bucket_name'

    # Call the function to remove denied actions from the bucket policy
    remove_denied_actions_from_policy(bucket_name)

if __name__ == "__main__":
    main()
