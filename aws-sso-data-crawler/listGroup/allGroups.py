import boto3
import os
import json
import csv
from botocore.exceptions import ClientError

def get_identity_store_id():
    # Create an AWS SSO Admin client
    sso_admin_client = boto3.client('sso-admin')

    # List all AWS SSO instances
    response_instances = sso_admin_client.list_instances()

    # Get the first AWS SSO instance (You can modify this logic to choose a specific instance if you have multiple instances)
    instance = response_instances['Instances'][0]

    # Extract the Identity Store ID from the AWS SSO instance
    identity_store_id = instance['IdentityStoreId']

    return identity_store_id

def list_groups():
    # Get the Identity Store ID dynamically
    identity_store_id = get_identity_store_id()

    # Create an AWS Identity Store client
    client = boto3.client('identitystore')

    # Fetch the list of all groups from the AWS SSO Identity Store
    response_groups = client.list_groups(IdentityStoreId=identity_store_id)

    # Extract the list of groups
    groups = response_groups['Groups']

    # Prepare the list of groups with their members
    groups_data = []

    # Create an AWS Identity Store paginator for listing group memberships
    paginator = client.get_paginator('list_group_memberships')

    # Iterate through the list of groups
    for group in groups:
        group_id = group['GroupId']
        group_name = group['DisplayName']

        # Create an iterator to get all group memberships for the current group
        memberships_iterator = paginator.paginate(
            IdentityStoreId=identity_store_id,
            GroupId=group_id
        )

        # Prepare the list of group members with their names
        group_members_data = []
        for page in memberships_iterator:
            memberships = page['GroupMemberships']
            for membership in memberships:
                user_id_dict = membership['MemberId']
                user_id = user_id_dict['UserId']  # Access the 'UserId' key to get the user ID as a string

                # Fetch the user details using describe_user API to get the user name
                response_user = client.describe_user(
                    IdentityStoreId=identity_store_id,
                    UserId=user_id
                )

                # Extract the user name from the response
                user_name = response_user['UserName']

                user_data = {
                    "UserId": user_id,
                    "UserName": user_name
                }
                group_members_data.append(user_data)

        group_data = {
            "Group ID": group_id,
            "Group Name": group_name,
            "Group Members": group_members_data
        }
        groups_data.append(group_data)

    # Prepare the final output data with the "All-Groups" key
    all_groups_data = {
        "All-Groups": groups_data
    }

    # Prepare the JSON file path
    output_directory = 'output/listGroups'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # JSON file path
    json_file_path = os.path.join(output_directory, 'group_list.json')

    # Write the all_groups_data to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(all_groups_data, json_file, indent=2)

    # CSV file path
    csv_file_path = os.path.join(output_directory, 'group_list.csv')

    # Convert JSON to CSV and write to the CSV file
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Group ID", "Group Name", "User ID", "User Name"])
        for group_data in groups_data:
            group_id = group_data["Group ID"]
            group_name = group_data["Group Name"]
            for user_data in group_data["Group Members"]:
                user_id = user_data["UserId"]
                user_name = user_data["UserName"]
                csv_writer.writerow([group_id, group_name, user_id, user_name])


