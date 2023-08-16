import boto3
from botocore.exceptions import ClientError
import json
import os,csv


def convert_json_to_csv(json_file_path, csv_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    
    with open(csv_file_path, 'w', newline='') as csv_file:
        fieldnames = ['PermissionSetName', 'InlinePolicy', 'CustomerManagedPolicies', 'ManagedPolicies', 'AWSManagedPolicies']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for permission_set_data in data['PermissionSets']:
            writer.writerow(permission_set_data)


def get_all_permission_sets():
    # Create an AWS SSO Admin client
    sso_admin_client = boto3.client('sso-admin')

    # List all AWS SSO instances
    response_instances = sso_admin_client.list_instances()

    # Get the first AWS SSO instance (You can modify this logic to choose a specific instance if you have multiple instances)
    instance_arn = response_instances['Instances'][0]['InstanceArn']

    # Create a paginator for listing all permission sets
    paginator = sso_admin_client.get_paginator('list_permission_sets')
    permission_sets = []
    try:
        for page in paginator.paginate(InstanceArn=instance_arn):
            permission_sets.extend(page['PermissionSets'])
    except ClientError as e:
        print(f"Error listing permission sets: {e}")
        return None

    return instance_arn, permission_sets

def get_inline_policy_for_permission_set(instance_arn, permission_set_arn):
    # Create an AWS SSO Admin client
    sso_admin_client = boto3.client('sso-admin')

    # Get the inline policy for the permission set
    response_policy = sso_admin_client.get_inline_policy_for_permission_set(
        InstanceArn=instance_arn,
        PermissionSetArn=permission_set_arn
    )

    return response_policy.get('InlinePolicy')

def list_managed_policies_in_permission_set(instance_arn, permission_set_arn):
    # Create an AWS SSO Admin client
    sso_admin_client = boto3.client('sso-admin')

    # List managed policies for the permission set
    response_policies = sso_admin_client.list_managed_policies_in_permission_set(
        InstanceArn=instance_arn,
        PermissionSetArn=permission_set_arn
    )

    return response_policies['AttachedManagedPolicies']

def list_customer_managed_policies_in_permission_set(instance_arn, permission_set_arn):
    # Create an AWS SSO Admin client
    sso_admin_client = boto3.client('sso-admin')

    # List customer managed policies for the permission set
    response_policies = sso_admin_client.list_customer_managed_policy_references_in_permission_set(
        InstanceArn=instance_arn,
        PermissionSetArn=permission_set_arn
    )

    return response_policies.get('CustomerManagedPolicyReferences', [])

def get_permission_set_details(instance_arn, permission_set_arn):
    # Create an AWS SSO Admin client
    sso_admin_client = boto3.client('sso-admin')

    try:
        # Describe the permission set to get detailed information, including attached policies
        response_permission_set = sso_admin_client.describe_permission_set(InstanceArn=instance_arn, PermissionSetArn=permission_set_arn)
        permission_set_details = response_permission_set['PermissionSet']
        return permission_set_details
    except ClientError as e:
        print(f"Error describing permission set: {e}")
        return None

def save_inline_policy_to_file(inline_policy, permission_set_name):
    # Create a directory to store the policy files if it doesn't exist
    if not os.path.exists("inline_policies"):
        os.makedirs("inline_policies")

    file_name = f"inline_policies/{permission_set_name}.json"
    with open(file_name, 'w') as f:
        f.write(inline_policy)
    
    return file_name

def run_sso_permissions():
    instance_arn, all_permission_sets = get_all_permission_sets()

    if all_permission_sets:
        output_data = {}
        permission_sets_data = []

        # Print the detailed information of each permission set
        for permission_set_arn in all_permission_sets:
            permission_set_details = get_permission_set_details(instance_arn, permission_set_arn)
            if permission_set_details:
                permission_set_data = {
                    "PermissionSetName": permission_set_details['Name']
                }

                # Fetch the policies attached to the permission set
                inline_policy = get_inline_policy_for_permission_set(instance_arn, permission_set_arn)
                customer_managed_policies = list_customer_managed_policies_in_permission_set(instance_arn, permission_set_arn)
                managed_policies = list_managed_policies_in_permission_set(instance_arn, permission_set_arn)

                if inline_policy:
                    permission_set_data["InlinePolicy"] = json.loads(inline_policy)

                    # Create the 'policies' folder if it doesn't exist inside 'output'
                    policies_folder = os.path.join("output", "policies")
                    if not os.path.exists(policies_folder):
                        os.makedirs(policies_folder)

                    file_name = os.path.join(policies_folder, f"{permission_set_details['Name'].replace(' ', '_').lower()}_inline_policy.json")
                    with open(file_name, 'w') as f:
                        json.dump(permission_set_data["InlinePolicy"], f, indent=4)

                elif customer_managed_policies:
                    permission_set_data["CustomerManagedPolicies"] = [policy['Name'] for policy in customer_managed_policies]

                elif managed_policies:
                    permission_set_data["ManagedPolicies"] = [policy['Name'] for policy in managed_policies]

                # Check for AWS Managed Policies
                aws_managed_policies = [policy['PolicyName'] for policy in permission_set_details.get('ManagedPolicies', []) if policy['Status'] == 'ACTIVE']
                if aws_managed_policies:
                    permission_set_data["AWSManagedPolicies"] = aws_managed_policies

                permission_sets_data.append(permission_set_data)

        # Store all permission set data in a single JSON file inside 'output/permissionSet'
        permission_set_folder = os.path.join("output", "permissionSet")
        if not os.path.exists(permission_set_folder):
            os.makedirs(permission_set_folder)

        with open(os.path.join(permission_set_folder, "permission_sets_output.json"), 'w') as f:
            json.dump({"PermissionSets": permission_sets_data}, f, indent=4)
        


         # Store all permission set data in a single JSON file inside 'output/permissionSet'
    permission_set_folder = os.path.join("output", "permissionSet")
    if not os.path.exists(permission_set_folder):
        os.makedirs(permission_set_folder)

    json_file_path = os.path.join(permission_set_folder, "permission_sets_output.json")
    with open(json_file_path, 'w') as f:
        json.dump({"PermissionSets": permission_sets_data}, f, indent=4)

    # Convert the JSON file to CSV
    csv_file_path = os.path.join(permission_set_folder, "permission_sets_output.csv")
    convert_json_to_csv(json_file_path, csv_file_path)