#!/bin/bash

# Unset existing AWS credentials
unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY
unset AWS_SESSION_TOKEN
# echo "unset the credentials "

# Run the Python script to get new credentials
python3 getCredentials.py

# Check if the Python script has saved new credentials
if [ -f "aws_credentials.sh" ]; then
    # Load the new credentials into the current shell session
    source aws_credentials.sh
    echo "New credentials loaded into environment variables."
else
    echo "No new credentials were obtained."
fi
