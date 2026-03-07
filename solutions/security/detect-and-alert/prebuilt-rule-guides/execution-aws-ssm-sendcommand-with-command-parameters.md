---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS SSM `SendCommand` with Run Shell Command Parameters" prebuilt detection rule.
---

# AWS SSM `SendCommand` with Run Shell Command Parameters

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating AWS SSM `SendCommand` with Run Shell Command Parameters

AWS Systems Manager (SSM) allows remote command execution on EC2 instances via the `SendCommand` API, using scripts like `AWS-RunShellScript` or `AWS-RunPowerShellScript`. Adversaries may exploit this to execute unauthorized commands without direct access. The detection rule identifies unusual command executions by monitoring process activities, flagging first-time occurrences within a week to spot potential threats.

### Possible investigation steps

- Review the alert details to identify the specific EC2 instance and the user account associated with the `SendCommand` API call.
- Check the AWS CloudTrail logs for the `SendCommand` event to gather additional context, such as the source IP address, user agent, and any associated IAM roles or policies.
- Investigate the command parameters used in the `SendCommand` API call, focusing on the `commands` field to determine the nature and intent of the executed script.
- Examine the process execution history on the affected host to identify any unusual or unauthorized processes that may have been initiated as a result of the command.
- Assess the recent activity of the user account involved in the alert to identify any other suspicious actions or deviations from normal behavior.
- Verify the integrity and security posture of the affected EC2 instance, checking for any signs of compromise or unauthorized changes.

### False positive analysis

- Routine administrative tasks using AWS SSM SendCommand may trigger alerts. Identify and document regular maintenance scripts and exclude them from detection to reduce noise.
- Automated deployment processes often use AWS-RunShellScript or AWS-RunPowerShellScript. Review deployment logs and whitelist these processes if they are verified as non-threatening.
- Monitoring or compliance checks that utilize SSM for gathering system information can be mistaken for malicious activity. Confirm these activities with the relevant teams and create exceptions for known benign operations.
- Scheduled tasks or cron jobs that execute commands via SSM should be reviewed. If they are part of standard operations, consider excluding them from the rule to prevent false positives.
- Development and testing environments frequently use SSM for testing scripts. Ensure these environments are well-documented and apply exceptions to avoid unnecessary alerts.

### Response and remediation

- Immediately isolate the affected EC2 instance from the network to prevent further unauthorized command execution and potential lateral movement.
- Review the AWS CloudTrail logs to identify the source of the `SendCommand` API call, including the IAM user or role that initiated the command, and assess whether the access was legitimate or compromised.
- Revoke or rotate the credentials of the IAM user or role involved in the suspicious activity to prevent further unauthorized access.
- Conduct a thorough examination of the affected EC2 instance to identify any unauthorized changes or installed malware, and restore the instance from a known good backup if necessary.
- Implement stricter IAM policies and permissions to limit the use of the `SendCommand` API to only trusted users and roles, ensuring the principle of least privilege is enforced.
- Enable multi-factor authentication (MFA) for all IAM users with permissions to execute commands on EC2 instances to add an additional layer of security.
- Escalate the incident to the security operations team for further investigation and to determine if additional instances or resources have been compromised.
