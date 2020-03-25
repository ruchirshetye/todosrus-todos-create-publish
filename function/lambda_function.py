import boto3
from os import getenv

sns = boto3.resource('sns')
topic = sns.Topic(getenv('APP_TOPIC_ARN'))

def lambda_handler(event, context):
    for event_record in event["Records"]:
        if event_record["eventName"] != "INSERT":
            return { 'statusCode': 200 }
        identity_id = event_record["dynamodb"]["Keys"]["IdentityId"]["S"]
        name = event_record["dynamodb"]["NewImage"]["Name"]["S"]
        topic.publish(
            Message=name,
            Subject='Todo Created For You New Again',
            MessageAttributes={
                'IdentityId': {
                    'DataType': 'String',
                    'StringValue': identity_id,
                }
            }
        )