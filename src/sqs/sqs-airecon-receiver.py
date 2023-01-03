import json
import urllib3
import os
import boto3

def lambda_handler(event, context):
    try:
        queueUrl = os.environ['QUEUE_URL']
        sqs_client = boto3.client('sqs')
        print(f"This is what API Gateway passed to the Lambda receiver ")
        body = event.get('body')
        print(body)
        i = 0
        i = i + 1

        response = sqs_client.send_message(
            QueueUrl=queueUrl,
            MessageBody= body

        )
        print(f"Sent message")
        return {
            'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
            "isBase64Encoded": False,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': body,
        }
    except Exception as ex:
        return {
            "statusCode": 502,
            "error": ex
        }

if __name__ == "__main__":
    lambda_handler(None, None)