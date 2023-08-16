import csv
import boto3
import logic
import client

def main():
    s3_client = client.get_s3_client()

    # Get list of all S3 bucket names
    bucket_names = client.get_bucket_names(s3_client)

    # Create lists to store bucket info before and after enabling Block Public Access
    before_info = []

    # Check Block Public Access for each bucket and enable if disabled
    for bucket_name in bucket_names:
        block_public_access_enabled = logic.check_block_public_access(s3_client, bucket_name)
        public_read_access = logic.check_bucket_policy(s3_client )
        public_write_access = logic.check_bucket_acl(s3_client, bucket_name)

        status = 'Enabled' if block_public_access_enabled else 'Disabled'

        # Store before status
        before_info.append({
            'BucketName': bucket_name,
            'Status': status,
            'PublicReadAccess': 'Yes' if public_read_access else 'No',
            'PublicWriteAccess': 'Yes' if public_write_access else 'No'
        })

    before_csv_file = 'block_public_access_status_before.csv'
    with open(before_csv_file, mode='w', newline='') as csvfile:
        fieldnames = ['BucketName', 'Status', 'PublicReadAccess', 'PublicWriteAccess']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for info in before_info:
            writer.writerow(info)

    print(f"Block Public Access status and access permissions for S3 buckets have been written to {before_csv_file}")

if __name__ == "__main__":
    main()
