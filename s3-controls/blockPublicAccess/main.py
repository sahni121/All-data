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
    # after_info = []

    # Check Block Public Access for each bucket and enable if disabled
    for bucket_name in bucket_names:
        block_public_access_enabled = logic.check_block_public_access(s3_client, bucket_name)
        status = 'Enabled' if block_public_access_enabled else 'Disabled'

        # Store before status
        before_info.append({'BucketName': bucket_name, 'Status': status})
        
        # if not block_public_access_enabled:
        #     logic.enable_block_public_access(s3_client, bucket_name)

        # # Store after status
        # after_status = 'Enabled' if logic.check_block_public_access(s3_client, bucket_name) else 'Disabled'
        # after_info.append({'BucketName': bucket_name, 'Status': after_status})

    # Write "before" bucket info to CSV file
    before_csv_file = 'block_public_access_status_before.csv'
    with open(before_csv_file, mode='w', newline='') as csvfile:
        fieldnames = ['BucketName', 'Status','PublicReadAccess']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for info in before_info:
            writer.writerow(info)

    print(f"Block Public Access status before enabling for S3 buckets has been written to {before_csv_file}")

    # # Write "after" bucket info to CSV file
    # after_csv_file = 'block_public_access_status_after.csv'
    # with open(after_csv_file, mode='w', newline='') as csvfile:
    #     fieldnames = ['BucketName', 'Status']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     writer.writeheader()
    #     for info in after_info:
    #         writer.writerow(info)

    # print(f"Block Public Access status after enabling for S3 buckets has been written to {after_csv_file}")

if __name__ == "__main__":
    main()
