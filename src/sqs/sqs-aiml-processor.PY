import json
import urllib3
import os

def lambda_handler(event, context):
    print(f"sqs-aiml-processor: {event['body']}")

    return {
        'statusCode': 200,
        "isBase64Encoded": False,
        'headers': {
            'Content-Type': 'text/plain'
        },
        "Status": "Processed",
        "processorBody": event['body'],
        "receivedbody": event['receivedbody'],
        'body': 'Hello, AIML Processor! You have hit {}'.format(event["body"])
    }

if __name__ == "__main__":
    lambda_handler(None, None)