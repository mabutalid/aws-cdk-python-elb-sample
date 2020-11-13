#!/usr/bin/env python3

from aws_cdk import core

from stacks.elb_stacks import ElbStack

env_singapore = core.Environment(account="************", region="us-east-1")

app = core.App()
ElbStack(app, "elb-stack", env=env_singapore)

app.synth()
