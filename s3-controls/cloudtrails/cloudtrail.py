# # import boto3,pprint

# # def get_cloudtrail_event_types(trail_name):
# #     cloudtrail = boto3.client('cloudtrail')
# #     try:
# #         response = cloudtrail.get_event_selectors(TrailName=trail_name)
# #         pprint.pprint(response)
# #         event_selectors = response.get('EventSelectors', [])
# #         if not event_selectors:
# #             print(f"No event selectors configured for CloudTrail '{trail_name}'.")
# #         else:
# #             event_types = []
# #             for selector in event_selectors:
# #                 event_types.extend(selector['DataResources'])
# #             return event_types
# #     except cloudtrail.exceptions.TrailNotFoundException:
# #         print(f"CloudTrail '{trail_name}' not found.")
# #     except Exception as e:
# #         print(f"Error: {e}")


# # def main():
# #     cloudtrail = boto3.client('cloudtrail')
# #     response = cloudtrail.describe_trails()
# #     trails = response['trailList']
    
# #     for trail in trails:
# #         trail_name = trail['Name']
# #         print(f"Getting event types for CloudTrail '{trail_name}':")
# #         event_types = get_cloudtrail_event_types(trail_name)
# #         if event_types:
# #             for event_type in event_types:
# #                 print(event_type)

# # if __name__ == "__main__":
# #     main()






# import boto3
# import pprint
# import csv

# def get_cloudtrail_event_types(trail_name):
#     cloudtrail = boto3.client('cloudtrail')
#     try:
#         response = cloudtrail.get_event_selectors(TrailName=trail_name)
#         event_selectors = response.get('EventSelectors', [])
#         if not event_selectors:
#             print(f"No event selectors configured for CloudTrail '{trail_name}'.")
#         else:
#             event_types = set()
#             for selector in event_selectors:
#                 read_write_type = selector.get('ReadWriteType')
#                 if read_write_type == 'All':
#                     event_types.add('Read')
#                     event_types.add('Write')
#                 elif read_write_type == 'ReadOnly':
#                     event_types.add('Read')
#                 elif read_write_type == 'WriteOnly':
#                     event_types.add('Write')
#             return list(event_types)
#     except cloudtrail.exceptions.TrailNotFoundException:
#         print(f"CloudTrail '{trail_name}' not found.")
#     except Exception as e:
#         print(f"Error: {e}")


# import boto3
# import pprint
# import csv

# def get_cloudtrail_event_types(trail_name):
#     cloudtrail = boto3.client('cloudtrail')
#     try:
#         response = cloudtrail.get_event_selectors(TrailName=trail_name)
#         event_selectors = response.get('EventSelectors', [])
#         if not event_selectors:
#             print(f"No event selectors configured for CloudTrail '{trail_name}'.")
#         else:
#             event_types = set()
#             for selector in event_selectors:
#                 read_write_type = selector.get('ReadWriteType')
#                 if read_write_type == 'All':
#                     event_types.add('Read')
#                     event_types.add('Write')
#                 elif read_write_type == 'ReadOnly':
#                     event_types.add('Read')
#                 elif read_write_type == 'WriteOnly':
#                     event_types.add('Write')
#             return list(event_types)
#     except cloudtrail.exceptions.TrailNotFoundException:
#         print(f"CloudTrail '{trail_name}' not found.")
#     except Exception as e:
#         print(f"Error: {e}")

# def main():
#     cloudtrail = boto3.client('cloudtrail')
#     response = cloudtrail.describe_trails()
#     trails = response['trailList']

#     with open('cloudtrail_event_types.csv', mode='w', newline='') as csvfile:
#         fieldnames = ['CloudTrailName', 'EventTypes']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()

#         for trail in trails:
#             trail_name = trail['Name']
#             print(f"Getting event types for CloudTrail '{trail_name}':")
#             event_types = get_cloudtrail_event_types(trail_name)
#             if event_types:
#                 event_types_str = ', '.join(event_types)
#             else:
#                 event_types_str = 'No event selectors configured'
#             writer.writerow({'CloudTrailName': trail_name, 'EventTypes': event_types_str})

# if __name__ == "__main__":
#     main()


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

def main():
    cloudtrail = boto3.client('cloudtrail')
    response = cloudtrail.describe_trails()
    trails = response['trailList']

    with open('cloudtrail_event_types.csv', mode='w', newline='') as csvfile:
        fieldnames = ['CloudTrailName', 'ManagementEventTypes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for trail in trails:
            trail_name = trail['Name']
            print(f"Getting management event types for CloudTrail '{trail_name}':")
            management_event_types = get_management_event_types(trail_name)
            if management_event_types:
                management_event_types_str = ', '.join(management_event_types)
            else:
                management_event_types_str = 'No management events configured'
            writer.writerow({'CloudTrailName': trail_name, 'ManagementEventTypes': management_event_types_str})

if __name__ == "__main__":
    main()
