# AWS Automated EC2 Cost Optimizer

## Project Overview
In typical corporate cloud environments, development and staging servers are frequently left running 24/7, despite being idle outside of standard business hours (weekends and nights). This project implements an event-driven, serverless automation system that automatically shuts down non-essential development instances at night and spins them back up in the morning, reducing idle EC2 computing costs by up to **65%**.

## AWS Services & Tech Stack Used
* **Amazon EC2:** Hosted virtual servers categorized by tags (`Environment: Development` vs `Environment: Production`).
* **AWS Lambda:** Serverless execution environment running a Python script utilizing the **Boto3 SDK**.
* **Amazon EventBridge (Scheduler):** Configured with cron expressions to handle timed triggers for morning and evening routines.
* **AWS IAM:** Enforced principle of least privilege by building a custom role allowing only `Describe`, `Start`, and `Stop` permissions for EC2.

## Key Features
* **Tag-Based Targeting:** The script uses AWS API filters to safely target only instances tagged with `Environment: Development`, ensuring live production environments are never disrupted.
* **State Awareness:** The function checks current instance states (`running` or `stopped`) before sending API calls, preventing redundant execution cycles.
* **Zero-Cost Infrastructure:** Operates entirely within the AWS Free Tier, resulting in an automated cost-saving solution with $0 overhead.

## How to Deploy This
1. **IAM Setup:** Create an IAM policy with `ec2:DescribeInstances`, `ec2:StartInstances`, and `ec2:StopInstances` permissions and attach it to a Lambda execution role.
2. **Lambda Deployment:** Deploy the Python script provided in `lambda_function.py` and ensure the function timeout is set to 10 seconds to handle cold starts.
3. **EventBridge Automation:** Set up two EventBridge recurring schedules:
   * **Stop Schedule:** Cron (`0 19 * * ? *`) passing JSON payload `{"action": "stop"}`
   * **Start Schedule:** Cron (`0 9 * * ? *`) passing JSON payload `{"action": "start"}`
