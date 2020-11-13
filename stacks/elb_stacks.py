from aws_cdk import (
    aws_elasticloadbalancing as elb,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    core,
)


class ElbStack(core.Stack):
    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # creating a machine image
        ami = ec2.MachineImage.latest_amazon_linux(
            cpu_type=ec2.AmazonLinuxCpuType.X86_64,
            edition=ec2.AmazonLinuxEdition.STANDARD,
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX,
            storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
        )

        # creating vpc
        vpc = ec2.Vpc.from_lookup(self, "vpc", is_default=True)

        # creating security group
        skull_sg = ec2.SecurityGroup(
            self,
            "myec2sg",
            vpc=vpc,
            security_group_name="skull-sg",
            description="sg for ec2 cdk example",
            allow_all_outbound=True,
        )

        # creating autoscaling group
        asg = autoscaling.AutoScalingGroup(
            self,
            "autoscaling",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ami,
            vpc=vpc,
            security_group=skull_sg,
        )

        # creating load balancer
        load_balancer = elb.LoadBalancer(
            self, "loadbalancer", internet_facing=True, vpc=vpc
        )

        # adding listeners to load balancer
        listener = load_balancer.add_listener(
            external_port=80, external_protocol=elb.LoadBalancingProtocol.HTTP
        )

        # add targets for load balancer such as the autoscaling group created above
        load_balancer.add_target(asg)
