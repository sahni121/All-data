import boto3,pprint
import csv

def check_bucket_acl(bucket_name):
    s3 = boto3.client('s3')
    try:
        acl = s3.get_bucket_acl(Bucket=bucket_name)
        # pprint.pprint(acl)
        if 'Grants' in acl:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking ACL for bucket {bucket_name}: {e}")
        return False

def main():
    # Initialize Boto3 S3 client
    s3 = boto3.client('s3')

    # Get list of all S3 bucket names
    response = s3.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response['Buckets']]

    # Create a list to store bucket info
    bucket_info = []

    # Check ACL for each bucket
    for bucket_name in bucket_names:
        has_acl = check_bucket_acl(bucket_name)
        bucket_info.append({'BucketName': bucket_name, 'ACLConfigured': has_acl})

    # Write bucket info to CSV file
    csv_file = 'bucket_acl_status.csv'
    with open(csv_file, mode='w', newline='') as csvfile:
        fieldnames = ['BucketName', 'ACLConfigured']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for info in bucket_info:
            writer.writerow(info)

    print(f"Bucket ACL status has been written to {csv_file}")

if __name__ == "__main__":
    main()
