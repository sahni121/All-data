import boto3,csv
from botocore.exceptions import ClientError

def check_bucket_event_notifications(bucket_name):
    s3 = boto3.client('s3')
    try:
        response = s3.get_bucket_notification_configuration(Bucket=bucket_name)
        if 'TopicConfigurations' in response or 'QueueConfigurations' in response or 'LambdaFunctionConfigurations' in response:
            return True
        else:
            return False
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchConfiguration':
            return False
        else:
            raise
def put_bucket_event_notification(bucket_name):
    s3 =boto3.client('s3')
    response=s3.put_bucket_notification_configuration(bucket_name)
    if(check_bucket_event_notifications == False):
        response.get([])
def main():
    # Initialize Boto3 S3 client
    s3 = boto3.client('s3')

    # Get list of all S3 bucket names
    response = s3.list_buckets()
    bucket_names = [bucket['Name'] for bucket in response['Buckets']]

    # Create a list to store bucket info
    bucket_info = []

    # Check event notifications for each bucket
    # for bucket_name in bucket_names:
    bucket_name='1set7'
    has_event_notifications = check_bucket_event_notifications(bucket_name)
    if(has_event_notifications == True):
        status='enabled'
    else:
        status='Disabled'
        
    bucket_info.append({'BucketName': bucket_name, 'EventNotificationsEnabled': status})

    # Write bucket info to CSV file
    csv_file = 'bucket_event_notifications_status.csv'
    with open(csv_file, mode='w', newline='') as csvfile:
        fieldnames = ['BucketName', 'EventNotificationsEnabled']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for info in bucket_info:
            writer.writerow(info)

    print(f"Bucket event notifications status has been written to {csv_file}")

if __name__ == "__main__":
    main()
