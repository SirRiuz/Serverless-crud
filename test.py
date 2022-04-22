

import os
import boto3


client = boto3.client(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id='xxxxxxxxxxxxxxxx',
    aws_secret_access_key='xxxxxxxxxxxxxxxx'
)


# item = client.scan(TableName='usersTable')
# print(item)


