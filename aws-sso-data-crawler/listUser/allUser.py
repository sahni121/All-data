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

def list_users():
    # Get the Identity Store ID dynamically
    identity_store_id = get_identity_store_id()

    # Create an AWS Identity Store client
    client = boto3.client('identitystore')

    # Use the paginator to handle pagination of results
    paginator = client.get_paginator('list_users')
    page_iterator = paginator.paginate(IdentityStoreId=identity_store_id)

    try:
        # Prepare the list of users with their details
        users_data = []
        
        # Iterate through the pages of results
        for page in page_iterator:
            # Extract the list of users from the current page
            users = page['Users']

            # Append user details to the users_data list
            for user in users:
                user_id = user['UserId']
                user_name = user['UserName']
                user_email = user['Emails'][0]['Value'] if 'Emails' in user and user['Emails'] else 'N/A'
                user_displayname = user.get('DisplayName', 'N/A')

                user_data = {
                    "User ID": user_id,
                    "Username": user_name,
                    "User Email": user_email,
                    "User Display Name": user_displayname
                }
                users_data.append(user_data)

        # Prepare the final output data with the "All-Users" key
        all_users_data = {
            "All-Users": users_data
        }

        # Prepare the JSON file path
        output_directory = 'output/listUsers'
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        output_file_path_json = os.path.join(output_directory, 'user_list.json')

        # Write the all_users_data to the JSON file
        with open(output_file_path_json, 'w') as json_file:
            json.dump(all_users_data, json_file, indent=2)

        # Convert JSON to CSV and store it in the same location
        output_file_path_csv = os.path.join(output_directory, 'user_list.csv')
        with open(output_file_path_json, 'r') as json_file, open(output_file_path_csv, 'w', newline='') as csv_file:
            data = json.load(json_file)
            users_data = data['All-Users']

            # Create a CSV writer and write the header
            csv_writer = csv.DictWriter(csv_file, fieldnames=users_data[0].keys())
            csv_writer.writeheader()

            # Write the data to the CSV file
            csv_writer.writerows(users_data)

    except ClientError as e:
        print(f"An error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

