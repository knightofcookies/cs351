import base64
import boto3


ec2_client = boto3.client("ec2")
autoscaling_client = boto3.client("autoscaling")
cloudwatch_client = boto3.client("cloudwatch")

USER_DATA_SCRIPT = """#!/bin/bash
sudo yum update -y
sudo yum install -y httpd
sudo systemctl start httpd
sudo systemctl enable httpd
sudo chmod -R 755 /var/www/html/
sudo curl -o /var/www/html/index.html https://raw.githubusercontent.com/knightofcookies/knightofcookies.github.io/main/index.html
"""

encoded_script = base64.b64encode(USER_DATA_SCRIPT.encode("utf-8")).decode("utf-8")


launch_template_data = {
    "ImageId": "ami-0e53db6fd757e38c7",
    "InstanceType": "t2.micro",
    "KeyName": "bazinga",
    "SecurityGroupIds": ["sg-0e7e357d262c268b3"],
    "TagSpecifications": [
        {
            "ResourceType": "instance",
            "Tags": [{"Key": "Name", "Value": "MyEC2Instance"}],
        }
    ],
    "UserData": encoded_script,
}

response = ec2_client.create_launch_template(
    LaunchTemplateName="amazon_linux", LaunchTemplateData=launch_template_data
)

autoscaling_client.create_auto_scaling_group(
    AutoScalingGroupName="web-asg",
    LaunchTemplate={"LaunchTemplateName": "amazon_linux"},
    MinSize=1,
    MaxSize=3,
    DesiredCapacity=1,
    VPCZoneIdentifier="subnet-0f890cffb6a13f728",  # Replace with your subnet ID
)

# Create scale-up policy
scale_up_policy = autoscaling_client.put_scaling_policy(
    AutoScalingGroupName="web-asg",
    PolicyName="scale-up",
    AdjustmentType="ChangeInCapacity",
    ScalingAdjustment=1,
    Cooldown=300,
)

# Create scale-down policy
scale_down_policy = autoscaling_client.put_scaling_policy(
    AutoScalingGroupName="web-asg",
    PolicyName="scale-down",
    AdjustmentType="ChangeInCapacity",
    ScalingAdjustment=-1,
    Cooldown=300,
)

# Create CloudWatch alarms
cloudwatch_client.put_metric_alarm(
    AlarmName="scale-up-alarm",
    MetricName="CPUUtilization",
    Namespace="AWS/EC2",
    Statistic="Average",
    Period=60,
    EvaluationPeriods=1,
    Threshold=70.0,
    ComparisonOperator="GreaterThanThreshold",
    AlarmActions=[scale_up_policy["PolicyARN"]],
)

cloudwatch_client.put_metric_alarm(
    AlarmName="scale-down-alarm",
    MetricName="CPUUtilization",
    Namespace="AWS/EC2",
    Statistic="Average",
    Period=60,
    EvaluationPeriods=1,
    Threshold=30.0,
    ComparisonOperator="LessThanThreshold",
    AlarmActions=[scale_down_policy["PolicyARN"]],
)
