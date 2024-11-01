import base64
import boto3
import time

ec2_client = boto3.client("ec2")
autoscaling_client = boto3.client("autoscaling")
cloudwatch_client = boto3.client("cloudwatch")

USER_DATA_SCRIPT = """#!/bin/bash
sudo yum update -y
sudo yum install -y httpd stress
sudo systemctl start httpd
sudo systemctl enable httpd
sudo chmod -R 755 /var/www/html/
sudo curl -o /var/www/html/index.html https://raw.githubusercontent.com/knightofcookies/knightofcookies.github.io/main/index.html
"""

# sudo stress -c 10


encoded_script = base64.b64encode(USER_DATA_SCRIPT.encode("utf-8")).decode("utf-8")

# launch_template_data = {
#     "ImageId": "ami-0e53db6fd757e38c7",
#     "InstanceType": "t2.micro",
#     "KeyName": "bazinga",
#     "SecurityGroupIds": ["sg-0e7e357d262c268b3"],
#     "TagSpecifications": [
#         {
#             "ResourceType": "instance",
#             "Tags": [{"Key": "Name", "Value": "MyEC2Instance"}],
#         }
#     ],
#     "UserData": encoded_script,
# }

# response = ec2_client.create_launch_template(
#     LaunchTemplateName="amazon_linux", LaunchTemplateData=launch_template_data
# )

autoscaling_client.create_auto_scaling_group(
    AutoScalingGroupName="web-asg",
    LaunchTemplate={"LaunchTemplateName": "amazon_linux"},
    MinSize=1,
    MaxSize=3,
    DesiredCapacity=1,
    VPCZoneIdentifier="subnet-0f890cffb6a13f728",  # Replace with your subnet ID
)


def create_scaling_policies():
    scale_up_policy = autoscaling_client.put_scaling_policy(
        AutoScalingGroupName="web-asg",
        PolicyName="scale-up",
        AdjustmentType="ChangeInCapacity",
        ScalingAdjustment=1,
        Cooldown=60,
    )

    scale_down_policy = autoscaling_client.put_scaling_policy(
        AutoScalingGroupName="web-asg",
        PolicyName="scale-down",
        AdjustmentType="ChangeInCapacity",
        ScalingAdjustment=-1,
        Cooldown=60,
    )

    cloudwatch_client.put_metric_alarm(
        AlarmName="HighCPUUtilization",
        MetricName="CPUUtilization",
        Namespace="AWS/EC2",
        Statistic="Average",
        Period=60,
        EvaluationPeriods=1,
        Threshold=30.0,
        ComparisonOperator="GreaterThanThreshold",
        Dimensions=[{"Name": "AutoScalingGroupName", "Value": "web-asg"}],
        AlarmActions=[scale_up_policy["PolicyARN"]],
        Unit="Percent",
    )

    cloudwatch_client.put_metric_alarm(
        AlarmName="LowCPUUtilization",
        MetricName="CPUUtilization",
        Namespace="AWS/EC2",
        Statistic="Average",
        Period=60,
        EvaluationPeriods=1,
        Threshold=10.0,
        ComparisonOperator="LessThanThreshold",
        Dimensions=[{"Name": "AutoScalingGroupName", "Value": "web-asg"}],
        AlarmActions=[scale_down_policy["PolicyARN"]],
        Unit="Percent",
    )


create_scaling_policies()


time.sleep(60)

response = autoscaling_client.describe_auto_scaling_groups(
    AutoScalingGroupNames=["web-asg"]
)
instances = response["AutoScalingGroups"][0]["Instances"]
print(f"Number of instances: {len(instances)}")
