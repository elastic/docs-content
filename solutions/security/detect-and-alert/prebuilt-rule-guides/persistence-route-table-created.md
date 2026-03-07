---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS EC2 Route Table Created" prebuilt detection rule.
---

# AWS EC2 Route Table Created

## Triage and analysis

### Investigating AWS EC2 Route Table Created

AWS Route Tables are crucial components in managing network traffic within AWS environments, directing data between subnets and internet gateways. Adversaries may exploit route tables to reroute traffic for data exfiltration or to establish persistence by creating unauthorized routes. The detection rule monitors successful creation events of route tables, flagging potential misuse by correlating specific AWS CloudTrail logs, thus aiding in identifying unauthorized network configuration changes.

### Possible investigation steps

- Investigate the AWS account and IAM user or role to determine if the action aligns with expected behavior and permissions.
- Examine the newly created route table's configuration to identify any unauthorized or suspicious routes that could indicate potential misuse or data exfiltration attempts.
- Correlate the event with other network security monitoring data to identify any unusual traffic patterns or anomalies that coincide with the route table creation.
- Assess the environment for any recent changes or incidents that might explain the creation of the route table, such as new deployments or infrastructure modifications.

### False positive analysis

- Routine infrastructure updates or deployments may trigger route table creation events. To manage this, establish a baseline of expected behavior during scheduled maintenance windows and exclude these from alerts.
- Automated cloud management tools often create route tables as part of their operations. Identify these tools and create exceptions for their known activities to reduce noise.
- Development and testing environments frequently undergo changes, including the creation of route tables. Consider excluding these environments from alerts or applying a different set of monitoring rules.
- Legitimate changes by authorized personnel can be mistaken for suspicious activity. Implement a process to verify and document authorized changes, allowing for quick exclusion of these events from alerts.
- Multi-account AWS setups might have centralized networking teams that create route tables across accounts. Coordinate with these teams to understand their activities and exclude them from triggering alerts.

### Response and remediation

- If unauthorized, remove permissions for related actions from the user or role. You can use the managed [AWSDenyAll](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSDenyAll.html) policy. 
- Review the newly created route table and any associated routes to identify unauthorized entries. Remove any routes that are not part of the expected network configuration.
- Conduct a thorough audit of IAM roles and permissions to ensure that only authorized users have the ability to create or modify route tables. Revoke any excessive permissions identified.
- Implement network monitoring to detect unusual traffic patterns that may indicate data exfiltration or other malicious activities.
- Escalate the incident to the security operations team for further investigation and to determine if additional AWS resources have been compromised.
- Review AWS CloudTrail logs for any other suspicious activities around the time of the route table creation to identify potential indicators of compromise.
- Update security policies and procedures to include specific guidelines for monitoring and responding to unauthorized route table modifications, ensuring rapid detection and response in the future.

## Setup

The AWS Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
