import json
import urllib3
import os


def lambda_handler(event, context):
    try:
        print(f"This is what API Gateway passed to the Lambda receiver ")
        body = event.get('body')
        print(body)
        i = 0
        i = i + 1

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