import json
import urllib3
import os

def lambda_handler(event, context):
    try:
        print(f"Post Processor: {event.get('body')}")

        return {
            'statusCode': 200,
            "isBase64Encoded": False,
            'headers': {
                'Content-Type': 'application/json'
            },
            "processorBody": event['body'],
            "receivedbody": event['receivedbody'],
            'body': 'Hello, SQS ai-ml post processor received '
        }
    except Exception as ex:
        return ex

if __name__ == "__main__":
    lambda_handler(None, None)