import json
import urllib3
import os

def lambda_handler(event, context):

    print('request: {}'.format(json.dumps(event)))
    url = os.environ['API_URL']
    max_count = 5
    url_modified = f"{url}/airecon/"
    print(f"API Request: {url_modified}")

    http = urllib3.PoolManager()
    for n in range(0,max_count):
        x = http.request('PUT', url_modified, body=json.dumps(event))

    return {
        'statusCode': 200,
        "isBase64Encoded": False,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'Hello, SQS Bulk Message Caller! You have received {}\n '.format(x.data)
    }

#
# if __name__ == "__main__":
#     handler( {"key1": "value1", "key2": "value2", "key3": "value3"}, None)