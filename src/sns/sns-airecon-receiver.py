import json
import urllib3
import os

i = 0
def lambda_handler(event, context):

    body = event['body']

    i = i + 1

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': body,
        "iteration": i,
        'processedBy': f"SNS Method receiver processing received {event['body']}"
    }

if __name__ == "__main__":
    lambda_handler(None, None)