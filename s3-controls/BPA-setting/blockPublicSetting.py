import boto3
import csv

def check_bucket_public_access_blocks(bucket_name):
    s3 = boto3.client('s3')
    try:
        response = s3.get_public_access_block(Bucket=bucket_name)
        
        # Check if any of the public access blocks settings are set to false
        if not response['PublicAccessBlockConfiguration']['IgnorePublicAcls'] or \
           not response['PublicAccessBlockConfiguration']['BlockPublicPolicy'] or \
           not response['PublicAccessBlockConfiguration']['BlockPublicAcls'] or \
           not response['PublicAccessBlockConfiguration']['RestrictPublicBuckets']:
            return False
        else:
            return True
    except s3.exceptions.NoSuchPublicAccessBlockConfiguration:
        return False

def main():
    # Initialize Boto3 S3 client
    s3 = boto3.client('s3')

    # Get list of all S3 bucket names
    response = s3.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response['Buckets']]

    # Create a list to store bucket info
    bucket_info = []

    # Check bucket public access blocks for each bucket
    for bucket_name in bucket_names:
        bucket_public_access_blocks_applied = check_bucket_public_access_blocks(bucket_name)
        status = 'Applied' if bucket_public_access_blocks_applied else 'Not Applied'
        bucket_info.append({'BucketName': bucket_name, 'PublicAccessBlocksStatus': status})

    # Write bucket info to CSV file
    csv_file = 'bucket_public_access_blocks_status.csv'
    with open(csv_file, mode='w', newline='') as csvfile:
        fieldnames = ['BucketName', 'PublicAccessBlocksStatus']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for info in bucket_info:
            writer.writerow(info)

    print(f"Bucket public access blocks status has been written to {csv_file}")

if __name__ == "__main__":
    main()
