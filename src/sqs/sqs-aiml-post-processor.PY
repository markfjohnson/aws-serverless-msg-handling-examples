import json
import urllib3
import os

def handler(event, context):


    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'Hello, SQS ai-ml post processor received {}'.format(event["body"])
    }

if __name__ == "__main__":
    handler(None, None)