
# SQS vs SNS vs Event Bridge Examples

## Overview

| Requirement              | SNS | SQS | EventBridge |
|--------------------------|-----|-----|-------------|
| Replay messages          | No | No  | Yes |
| Tracing                  | Yes | Yes | Yes |
| Push message to consumer | Yes | No  | Yes |
| Consumer Pulls Message | No | Yes | No |
| Catch Duplicates | No | Yes | No |

## Examples

Pre-requisites:
* Create a S3 bucket to hold the artifacts.  This will be used with the S3-bucket parameter option when deploying the example using SAM.
### SQS


#### Setup Enviornment
``` 
sam deploy -t sqs-template.yaml --stack-name sqs-message-example --s3-bucket mfj-sam-artifacts --capabilities CAPABILITY_IAM
```

#### Run Example

```python

```



