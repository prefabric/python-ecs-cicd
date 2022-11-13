
from aws_cdk import (
    Stack,
    aws_ecr as ecr,
)
from constructs import Construct

class CommonInfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.ecr_repository = ecr.Repository(self, "app_image_repository")
