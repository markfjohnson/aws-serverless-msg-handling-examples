
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

### SQS

XXXXX

```
sam deploy -t sqs-template.yaml --stack-name sqs-message-example 
```
