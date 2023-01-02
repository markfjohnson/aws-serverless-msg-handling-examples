from aws_cdk import (
    # Duration,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_cognito as cognito,
    aws_logs as logs,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_lambda_destinations as destinations,
    aws_events as events,
    Stack, Duration
    # aws_sqs as sqs,
)
from constructs import Construct

class MddDetectApigwEventbridgeStack(Stack):

    def defineNetworkStuff(self, vpcName, projectTag):
        log_group = logs.LogGroup(self, f"{vpcName}VPCLogGroup", retention=logs.RetentionDays.THREE_DAYS)
        flowIAM = iam.Role(self, f"{vpcName}FlowRole", assumed_by=iam.ServicePrincipal("vpc-flow-logs.amazonaws.com"))

        # VPC
        pubSubnet = ec2.SubnetConfiguration(name=f"{vpcName}public1", subnet_type=ec2.SubnetType.PUBLIC)
        subnets = []
        subnets.append(pubSubnet)
        pubSubnet = ec2.SubnetConfiguration(name=f"{vpcName}public2", subnet_type=ec2.SubnetType.PUBLIC)
        subnets = []
        subnets.append(pubSubnet)
        privateSubnet1 = ec2.SubnetConfiguration(name=f"{vpcName}private1", subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT)
        subnets.append(privateSubnet1)
        privateSubnet2 = ec2.SubnetConfiguration(name=f"{vpcName}private2", subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT)
        subnets.append(privateSubnet2)
        vpc = ec2.Vpc(self, f"{vpcName}VPC", max_azs=3,
                      subnet_configuration=subnets)
        ec2.FlowLog(self, f"{vpcName}FlowLog",
                    resource_type=ec2.FlowLogResourceType.from_vpc(vpc),
                    destination=ec2.FlowLogDestination.to_cloud_watch_logs(log_group, flowIAM))

        vpcEndpoint = None
        # apigwService = ec2.IInterfaceVpcEndpointService(name="*.execute-api.us-east-1.amazonaws.com", port=443)
        #
        # vpcEndpoint = ec2.InterfaceVpcEndpoint(self, "API Gateway VPC Endpoint",
        #                                        vpc=vpc,
        #                                        service=apigwService,
        #                                        subnets=ec2.SubnetSelection(
        #                                            subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT
        #                                        ),
        #                                        private_dns_enabled=True
        #                                        )

        return (vpc, vpcEndpoint)

    def defineCognito(self, poolName, api):
        user_pool = cognito.UserPool(self, id=poolName, user_pool_name=f"{poolName}-cognito", self_sign_up_enabled=True)

        user_pool.add_client(f"{poolName}Web-App",
                             generate_secret=True,
                             o_auth=cognito.OAuthSettings(
                                 # flows=cognito.OAuthFlows(
                                 #     client_credentials=True
                                 # ),
                                 scopes=[cognito.OAuthScope.COGNITO_ADMIN, cognito.OAuthScope.EMAIL,
                                         cognito.OAuthScope.PHONE, cognito.OAuthScope.PROFILE],
                                 callback_urls=["https://example.com/callback"],
                                 logout_urls=["https://example.com/signout"]),
                             )

        region = "us-east-1"
        #       auth = apigateway.CognitoUserPoolsAuthorizer(self, f'{poolName}Authorizer', cognito_user_pools=[user_pool])

        print(api)
        return user_pool

    def defineFunction(self, functionName, vpc=None, env_vars=None, eventBridgeDest=False):
        if vpc is not None:
            lambda_func = self.definePrivateLambda(functionName, vpc, env_vars, eventBridgeDest)
        else:
            lambda_func = self.definePublicLambda(functionName, env_vars, eventBridgeDest)
        return (lambda_func)

    def definePublicLambda(self, functionName, env_vars=None, eventBridgeDest=False):
        lambda_role = iam.Role(self, f"{functionName}_lambda_role",
                               assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
                               role_name=f"{functionName}_lambda_role"
                               )
        iam.ManagedPolicy(self, f"{functionName}_managed_policy",
                          statements=[
                              iam.PolicyStatement(
                                  effect=iam.Effect.ALLOW,
                                  actions=["ec2:CreateNetworkInterface",
                                           "ec2:DescribeNetworkInterfaces",
                                           "ec2:DeleteNetworkInterface",
                                           "ec2:AssignPrivateIpAddresses",
                                           "ec2:UnassignPrivateIpAddresses"],
                                  resources=["*"]
                              ),
                              iam.PolicyStatement(
                                  effect=iam.Effect.ALLOW,
                                  actions=["ec2:CreateNetworkInterface",
                                           "ec2:DescribeNetworkInterfaces",
                                           "ec2:DeleteNetworkInterface",
                                           "ec2:AssignPrivateIpAddresses",
                                           "ec2:UnassignPrivateIpAddresses"],
                                  resources=["*"]
                              ),
                          ],
                          roles=[lambda_role]
                          )
        lambda_role.add_managed_policy(
                    iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEventBridgeFullAccess"))

        evtBrdgeDest=None
        if eventBridgeDest:
            evtBrdgeDest = destinations.EventBridgeDestination()
        lambda_func = _lambda.Function(
            self, functionName,
            runtime=_lambda.Runtime.PYTHON_3_9,
            function_name=functionName,
            code=_lambda.Code.from_asset('lambda'),
            timeout=Duration.seconds(5),
            environment=env_vars,
            handler=f"{functionName}.handler",
            role = lambda_role,
            on_success= evtBrdgeDest)

        return lambda_func

    def definePrivateLambda(self, functionName, vpc, env_vars=None, eventBridgeDest=False):
        lambda_role = iam.Role(self, f"{functionName}_lambda_role",
                               assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
                               role_name=f"{functionName}_lambda_role"
                               )
        iam.ManagedPolicy(self, f"{functionName}_managed_policy",
                          statements=[
                              iam.PolicyStatement(
                                  effect=iam.Effect.ALLOW,
                                  actions=["ec2:CreateNetworkInterface",
                                           "ec2:DescribeNetworkInterfaces",
                                           "ec2:DeleteNetworkInterface",
                                           "ec2:AssignPrivateIpAddresses",
                                           "ec2:UnassignPrivateIpAddresses"],
                                  resources=["*"]
                              ),
                              iam.PolicyStatement(
                                  effect=iam.Effect.ALLOW,
                                  actions=["ec2:CreateNetworkInterface",
                                           "ec2:DescribeNetworkInterfaces",
                                           "ec2:DeleteNetworkInterface",
                                           "ec2:AssignPrivateIpAddresses",
                                           "ec2:UnassignPrivateIpAddresses"],
                                  resources=["*"]
                              ),
                          ],
                          roles=[lambda_role]
                          )
        lambda_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonEventBridgeFullAccess"))
        evtBrdgeDest=None
        if eventBridgeDest:
            evtBrdgeDest = destinations.EventBridgeDestination()
        lambda_func = _lambda.Function(
            self, functionName,
            function_name=functionName,
            runtime=_lambda.Runtime.PYTHON_3_9,
            vpc=vpc,
            code=_lambda.Code.from_asset('lambda'),
            timeout=Duration.seconds(5),
            handler=f"{functionName}.handler",
            environment=env_vars,
            role=lambda_role,
            on_success=evtBrdgeDest
        )
        return lambda_func

    def defineApiGateway(self, apiName, description, myFunction=None, apikey_required=False, integrationType=None,
                         endpointType=None, policyDocuments=None, env=None):

        api = apigateway.RestApi(
            self, apiName,
            rest_api_name=apiName,
            description=description,
            default_integration=integrationType,
            endpoint_configuration=endpointType,
            policy=policyDocuments,
        )

        return api

    def ex_regional_apigw(self):
        endPointConfig = apigateway.EndpointConfiguration(
            types=[apigateway.EndpointType.REGIONAL]
        )
        api_gw = self.defineApiGateway("RegionalAPIGW", "This is a test API Gateway with EventBridge",
                                       endpointType=endPointConfig)
        env_vars = {
            "URL": api_gw.url,
        }
        regionalMethodFunction = self.defineFunction("RegionalMethodFunction", eventBridgeDest=True)
        cognitoLambdaMethod = self.defineFunction("EventBridgeSrc")
        edgeCaller = self.defineFunction("RegionalCaller", env_vars=env_vars)
        self.defineMethods(api_gw, methodType="PUT", integrationType=apigateway.LambdaIntegration(regionalMethodFunction),
                           apiKeyRequired=False)

    def defineMethods(self, api, integrationType, methodType="GET", apiKeyRequired=False, auth=None):
        v1 = api.root.add_resource("v1")
        echo = v1.add_resource("echo")
        echo_method = echo.add_method(methodType, integrationType, api_key_required=apiKeyRequired, authorizer=auth)

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.ex_regional_apigw()
