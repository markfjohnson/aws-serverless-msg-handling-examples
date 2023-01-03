import boto3
import os

def lambda_handler(event, context):
    print(f"sqs-aiml-processor: {event['body']}")
    sqs_client = boto3.client('sqs')
    queueUrl = os.environ['QUEUE_URL']

    response = sqs_client.send_message(
        QueueUrl=queueUrl,
        MessageBody='This is my second test SQS message',

    )

    result = {
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
