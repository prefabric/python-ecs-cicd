from aws_cdk import (
    Stack,
    aws_ecs_patterns as ecs_patterns,
    aws_ecs as ecs,
    aws_ec2 as ec2,
)
from constructs import Construct

class StagingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        config = self.node.try_get_context("context")["scaffold_config"]["staging"]

        # Staging vpc creation
        staging_vpc = ec2.Vpc(
            self,
            "StagingVPC",
            cidr=f"{config['cidr']}/21",
            max_azs=config["max_azs"],
            nat_gateways=config["nat_gateways"],
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="Ingress",
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    cidr_mask=24,
                    name="Application",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                ),
            ]
        )

        # ECS cluster creation
        cluster = ecs.Cluster(self, "FargateClusterStaging", vpc=staging_vpc)

        # Fargate service creation
        self.load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "ServiceStaging",
            cluster=cluster,
            memory_limit_mib=1024,
            desired_count=config["desired_count"],
            cpu=512,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("nginx"),
                container_port=80,
            ),
            task_subnets=ec2.SubnetSelection(
                subnets=staging_vpc.private_subnets
            ),
        )
