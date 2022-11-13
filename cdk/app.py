#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk.pipeline_stack import PipelineStack
from cdk.common_infra_stack import CommonInfraStack
from cdk.staging_stack import StagingStack
from cdk.prod_stack import ProdStack


app = cdk.App()

env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))

common_infra_stack = CommonInfraStack(app, "CommonInfraStack", env=env)
staging_stack = StagingStack(app, "StagingStack", env=env)

config = app.node.try_get_context("context")

prod_stack = None
if config["scaffold_config"]["prod_enabled"]:
    prod_stack = ProdStack(app, "ProdStack", env=env)
    prod_stack.add_dependency(staging_stack)

pipeline_stack = PipelineStack(
    app,
    "PipelineStack",
    common_infra_stack=common_infra_stack,
    staging_stack=staging_stack,
    prod_stack=prod_stack,
    env=env,
)
pipeline_stack.add_dependency(common_infra_stack)
pipeline_stack.add_dependency(staging_stack)

if config["scaffold_config"]["prod_enabled"]:
    pipeline_stack.add_dependency(prod_stack)

app.synth()
