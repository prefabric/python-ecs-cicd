import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk.common_infra_stack import CommonInfraStack

def test_sqs_queue_created():
    app = core.App()
    stack = CommonInfraStack(app, "CommonInfraStack")
    template = assertions.Template.from_stack(stack)

    template.has_resource(
        "AWS::ECR::Repository",
        {
            "DeletionPolicy": "Retain"
        },
    )
