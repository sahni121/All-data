

import requests
import json
import boto3
import os



def get_role_and_external(account_id):
    api_url = "https://be.cloudonomic.com/billdesk//ck-auto/anonymous/customer-with-payer"
 
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_data = response.json()

        if 'data' in response_data:
            for data_entry in response_data['data']:
                if data_entry['payerAccountId'] == int(account_id):
                    role_arn = data_entry['iamRole']
                    external_id = data_entry['externalId']
                    if role_arn and external_id:
                        return role_arn, external_id
                    break

        print(f"ARN and ExternalId not found for Customer ID: {account_id}")
        return None, None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the API request: {e}")
        return None, None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None, None


def validate_assume_role(role_arn, external_id):
    try:
        sts_client = boto3.client('sts')
        response = sts_client.assume_role(
            RoleArn=role_arn,
            ExternalId=external_id,
            RoleSessionName='Ck-Auto'
        )
        
        credentials = response['Credentials']
        return credentials  # Return the assumed credentials

    except Exception as e:
        print(f"Error assuming the role: {e}")
        return None

def save_credentials_to_file(credentials):
    with open('aws_credentials.sh', 'w') as file:
        file.write(f"export AWS_ACCESS_KEY_ID='{credentials['AccessKeyId']}'\n")
        file.write(f"export AWS_SECRET_ACCESS_KEY='{credentials['SecretAccessKey']}'\n")
        file.write(f"export AWS_SESSION_TOKEN='{credentials['SessionToken']}'\n")


def main():
    account_id= input("Enter the Account ID: ")

    role_arn, external_id = get_role_and_external(account_id)
    if role_arn and external_id:
        print(f"Role ARN: {role_arn}")
        print(f"External ID: {external_id}")


    if role_arn and external_id:
        credentials = validate_assume_role(role_arn, external_id)
        if credentials:
            # Export the assumed credentials as environment variables
            os.environ['AWS_ACCESS_KEY_ID'] = credentials['AccessKeyId']
            os.environ['AWS_SECRET_ACCESS_KEY'] = credentials['SecretAccessKey']
            os.environ['AWS_SESSION_TOKEN'] = credentials['SessionToken']

            print("Credentials exported to environment variables.")

            # Save credentials to a file
            save_credentials_to_file(credentials)

            print("Assumed Role successfully and credentials exported to file.")

            # Read and print the credentials file
          
        else:
            print("Error while assuming the role.")
    else:
        print("Unable to retrieve RoleArn and ExternalId.")

if __name__ == "__main__":
    main()
