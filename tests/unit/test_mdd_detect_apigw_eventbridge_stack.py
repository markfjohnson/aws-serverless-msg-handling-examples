import aws_cdk as core
import aws_cdk.assertions as assertions

from mdd_detect_apigw_eventbridge.mdd_detect_apigw_eventbridge_stack import MddDetectApigwEventbridgeStack

# example tests. To run these tests, uncomment this file along with the example
# resource in mdd_detect_apigw_eventbridge/mdd_detect_apigw_eventbridge_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MddDetectApigwEventbridgeStack(app, "mdd-detect-apigw-eventbridge")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
