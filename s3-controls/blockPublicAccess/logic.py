

import boto3
import botocore

def check_block_public_access(s3_client, bucket_name):
    try:
        response = s3_client.get_public_access_block(Bucket=bucket_name)
        return response['PublicAccessBlockConfiguration']['BlockPublicAcls'] and \
               response['PublicAccessBlockConfiguration']['IgnorePublicAcls'] and \
               response['PublicAccessBlockConfiguration']['BlockPublicPolicy'] and \
               response['PublicAccessBlockConfiguration']['RestrictPublicBuckets']
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
            return False
        else:
            raise






# def enable_block_public_access(s3_client, bucket_name):
#     s3_client.put_public_access_block(
#         Bucket=bucket_name,
#         PublicAccessBlockConfiguration={
#             'BlockPublicAcls': True,
#             'IgnorePublicAcls': True,
#             'BlockPublicPolicy': True,
#             'RestrictPublicBuckets': True
#         }
#     )
#     print(f"Block Public Access enabled for bucket: {bucket_name}")
