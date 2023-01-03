import json
import urllib3
import os
import boto3

sqs_client = boto3.client('sqs')

def lambda_handler(event, context):
    queueUrl = os.environ['QUEUE_URL']
    queueArn = os.environ['QUEUE_ARN']
    try:
        print(f"SQS-This is what API Gateway passed to the Lambda receiver ")
        body = event.get('body')
        print(event)
        i = 0
        i = i + 1

        messageBody = "API Gateway message handler"
        response = sqs_client.send_message(
            QueueUrl=queueUrl,
            MessageBody=messageBody,
            DelaySeconds=123,
         )
        print(f"Sent SQS Message and received response {response}")

        return {
            'statusCode': 200,
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