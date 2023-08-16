import boto3
import csv

def get_management_event_types(trail_name):
    cloudtrail = boto3.client('cloudtrail')
    try:
        response = cloudtrail.get_event_selectors(TrailName=trail_name)
        event_selectors = response.get('EventSelectors', [])
        if not event_selectors:
            print(f"No event selectors configured for CloudTrail '{trail_name}'.")
        else:
            management_event_types = set()
            for selector in event_selectors:
                if selector.get('IncludeManagementEvents'):
                    if selector.get('ReadWriteType') == 'All':
                        management_event_types.add('Read and Write')
                    elif selector.get('ReadWriteType') == 'ReadOnly':
                        management_event_types.add('Read')
                    elif selector.get('ReadWriteType') == 'WriteOnly':
                        management_event_types.add('Write')
            return list(management_event_types)
    except cloudtrail.exceptions.TrailNotFoundException:
        print(f"CloudTrail '{trail_name}' not found.")
    except Exception as e:
        print(f"Error: {e}")
# def main():
#     cloudtrail = boto3.client('cloudtrail')
#     response = cloudtrail.describe_trails()
#     trails = response['trailList']

#     read_and_write_trails = []
#     write_only_trails = []

#     for trail in trails:
#         trail_name = trail['Name']
#         print(f"Getting management event types for CloudTrail '{trail_name}':")
#         management_event_types = get_management_event_types(trail_name)
#         if 'Read and Write' in management_event_types:
#             read_and_write_trails.append({'Trail Name': trail_name, 'ManagementEventTypes': ', '.join(management_event_types)})
#         if 'Write' in management_event_types and 'Read' not in management_event_types:
#             write_only_trails.append({'Trail Name': trail_name, 'ManagementEventTypes': ', '.join(management_event_types)})

#     # Write read and write trails to a CSV file
#     with open('read_and_write_trails.csv', mode='w', newline='') as csvfile:
#         fieldnames = ['Trail Name', 'ManagementEventTypes']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for trail in read_and_write_trails:
#             writer.writerow(trail)

#     # Write write-only trails to a CSV file
#     with open('write_only_trails.csv', mode='w', newline='') as csvfile:
#         fieldnames = ['Trail Name', 'ManagementEventTypes']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for trail in write_only_trails:
#             writer.writerow(trail)

#     print("CloudTrail trails with both Read and Write permissions written to read_and_write_trails.csv")
#     print("CloudTrail trails with Write-only permissions written to write_only_trails.csv")

# if __name__ == "__main__":
#     main()



def main():
    cloudtrail = boto3.client('cloudtrail')
    response = cloudtrail.describe_trails()
    trails = response['trailList']

    common_trails = []

    for trail in trails:
        trail_name = trail['Name']
        print(f"Getting management event types for CloudTrail '{trail_name}':")
        management_event_types = get_management_event_types(trail_name)
        if 'Read and Write' in management_event_types and 'Write' in management_event_types:
            common_trails.append({'Trail Name': trail_name, 'ManagementEventTypes': ', '.join(management_event_types)})

    # Write common trails to a CSV file
    with open('common_trails.csv', mode='w', newline='') as csvfile:
        fieldnames = ['Trail Name', 'ManagementEventTypes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for trail in common_trails:
            writer.writerow(trail)

    print("CloudTrail trails with both Read and Write permissions and Write permissions written to common_trails.csv")

if __name__ == "__main__":
    main()