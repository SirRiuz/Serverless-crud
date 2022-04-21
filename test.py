

import os
import boto3


client = boto3.client(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id='AKIARJCBZXL7GZM22FGQ',
    aws_secret_access_key='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'
)


# item = client.scan(TableName='usersTable')
# print(item)


