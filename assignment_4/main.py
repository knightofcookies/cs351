import os
from dotenv import load_dotenv
import boto3

load_dotenv()

ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
REGION_NAME = os.getenv("REGION_NAME")

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name=REGION_NAME,
)

ec2 = session.resource("ec2")

USER_DATA_SCRIPT = """#!/bin/bash
sudo yum update -y
sudo yum install -y httpd
sudo systemctl start httpd
sudo systemctl enable httpd
sudo chmod -R 755 /var/www/html/
sudo curl -o /var/www/html/index.html https://raw.githubusercontent.com/knightofcookies/knightofcookies.github.io/main/index.html
"""

amazon_linux_instance = ec2.create_instances(
    ImageId="ami-0e53db6fd757e38c7",
    InstanceType="t2.micro",
    MinCount=1,
    MaxCount=1,
    UserData=USER_DATA_SCRIPT,
    KeyName="bazinga",
    SecurityGroupIds=["sg-0e7e357d262c268b3"],
)

amazon_linux_instance[0].wait_until_running()

amazon_linux_instance[0].reload()

print(f"HTTP server hosted at http://{amazon_linux_instance[0].public_ip_address}")

ubuntu_instances = ec2.create_instances(
    ImageId="ami-0522ab6e1ddcc7055",
    InstanceType="t2.micro",
    MinCount=2,
    MaxCount=2,
    KeyName="bazinga",
    SecurityGroupIds=["sg-07c4f01ac3b5e84a3"],
)

for instance in ubuntu_instances:
    instance.wait_until_running()

for instance in ec2.instances.filter(
    Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
):
    print(
        f'Instance ID: {instance.id}, State: {instance.state["Name"]}, Public IP: {instance.public_ip_address}'
    )

for instance in ec2.instances.filter(
    Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
):
    status = ec2.meta.client.describe_instance_status(InstanceIds=[instance.id])
    print(
        f'Instance ID: {instance.id}, Status: {status["InstanceStatuses"][0]["InstanceStatus"]["Status"]}'
    )


for instance in ec2.instances.filter(
    Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
):
    instance.stop()
    instance.wait_until_stopped()

for instance in ec2.instances.filter(
    Filters=[{"Name": "instance-state-name", "Values": ["stopped"]}]
):
    instance.terminate()
    instance.wait_until_terminated()

print("All instances have been terminated.")
