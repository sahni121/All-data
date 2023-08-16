import boto3
import csv

def check_bucket_encryption(bucket_name):
    s3 = boto3.client('s3')
    response = s3.get_bucket_encryption(Bucket=bucket_name)
    rules = response.get('ServerSideEncryptionConfiguration', {}).get('Rules', [])
    
    for rule in rules:
        encryption_algorithm = rule.get('ApplyServerSideEncryptionByDefault', {}).get('SSEAlgorithm')
        if encryption_algorithm == 'AES256':
            return 'Default encryption (SSE-S3) found'
        elif encryption_algorithm == 'aws:kms' or encryption_algorithm == 'aws:kms:aws_managed':
            return 'Encrypted with AWS KMS or DSSE-KMS'

    return 'Not encrypted'

def main():
    # Initialize Boto3 S3 client
    s3 = boto3.client('s3')

    # Get list of all S3 bucket names
    response = s3.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response['Buckets']]

    # Create a list to store bucket info
    bucket_info = []

    # Check encryption status for each bucket
    for bucket_name in bucket_names:
        encryption_status = check_bucket_encryption(bucket_name)
        bucket_info.append({'BucketName': bucket_name, 'EncryptionStatus': encryption_status})

    # Write bucket info to CSV file
    csv_file = 'bucket_encryption_status.csv'
    with open(csv_file, mode='w', newline='') as csvfile:
        fieldnames = ['BucketName', 'EncryptionStatus']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for info in bucket_info:
            writer.writerow(info)

    print(f"Bucket encryption status has been written to {csv_file}")

if __name__ == "__main__":
    main()
