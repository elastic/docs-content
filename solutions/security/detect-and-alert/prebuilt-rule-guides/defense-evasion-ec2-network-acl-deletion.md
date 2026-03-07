---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS EC2 Network Access Control List Deletion" prebuilt detection rule.'
---

# AWS EC2 Network Access Control List Deletion

## Triage and analysis

### Investigating AWS EC2 Network Access Control List Deletion

AWS EC2 Network ACLs are essential for controlling inbound and outbound traffic to subnets, acting as a firewall layer. Adversaries may delete these ACLs to disable security controls, facilitating unauthorized access or data exfiltration. The detection rule monitors AWS CloudTrail logs for successful deletion events of ACLs or their entries, signaling potential defense evasion attempts.

### Possible investigation steps

- Review the AWS CloudTrail logs to identify the specific user or role associated with the deletion event by examining the user identity information in the logs.
- Check the time and date of the deletion event to determine if it coincides with any other suspicious activities or known maintenance windows.
- Investigate the source IP address and location from which the deletion request was made to assess if it aligns with expected access patterns or if it appears anomalous.
- Examine the AWS account activity around the time of the event to identify any other unusual actions or changes, such as the creation of new resources or modifications to existing ones.
- Assess the impact of the deleted Network ACL or entries by identifying the affected subnets and evaluating the potential exposure or risk to the network.
- Review any recent changes to IAM policies or roles that might have inadvertently granted excessive permissions to users or services, allowing them to delete Network ACLs.

### False positive analysis

- Routine maintenance or updates by authorized personnel may trigger deletion events. Verify if the deletion aligns with scheduled maintenance activities and consider excluding these events from alerts.
- Automated scripts or infrastructure-as-code tools like Terraform or CloudFormation might delete and recreate ACLs as part of normal operations. Identify these tools and exclude their actions from triggering alerts.
- Changes in network architecture or security policy updates can lead to legitimate ACL deletions. Document these changes and adjust the detection rule to ignore such planned modifications.
- Ensure that the AWS accounts involved in the deletion events are recognized and trusted. Exclude actions from these accounts if they are part of regular administrative tasks.
- Collaborate with the security team to establish a baseline of normal ACL deletion activities and refine the detection rule to minimize false positives based on this baseline.

### Response and remediation

- Immediately isolate the affected subnet to prevent further unauthorized access or data exfiltration. This can be done by applying a restrictive security group or temporarily removing the subnet from the VPC.
- Review AWS CloudTrail logs to identify the source of the deletion event, including the IAM user or role responsible, and assess whether the action was authorized or part of a larger compromise.
- Recreate the deleted Network ACL or its entries using the most recent backup or configuration documentation to restore intended security controls.
- Implement a temporary monitoring solution to track any further unauthorized changes to network ACLs or related security configurations.
- Escalate the incident to the security operations team for a comprehensive investigation to determine the root cause and scope of the breach, including potential lateral movement or data exfiltration.
- Revoke or rotate credentials for any compromised IAM users or roles involved in the deletion event to prevent further unauthorized actions.
- Enhance detection capabilities by configuring alerts for any future unauthorized changes to network ACLs, ensuring rapid response to similar threats.

## Setup

The AWS Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
