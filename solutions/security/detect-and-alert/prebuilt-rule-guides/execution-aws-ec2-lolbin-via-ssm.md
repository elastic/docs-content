---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS EC2 LOLBin Execution via SSM SendCommand" prebuilt detection rule.
---

# AWS EC2 LOLBin Execution via SSM SendCommand

## Triage and analysis

### Investigating AWS EC2 LOLBin Execution via SSM SendCommand

AWS Systems Manager (SSM) enables remote command execution on EC2 instances without SSH/RDP access. While legitimate for administration, adversaries exploit this by running LOLBins—system utilities abused for malicious purposes like data theft or backdoors. This detection correlates CloudTrail API logs with endpoint telemetry using SSM command IDs, bypassing AWS's parameter redaction to reveal actual executed commands and identify suspicious activity.

This is an ESQL aggregation-based rule, thus all original event fields and detail may not be present in the alert. It is recommended to pivot into the raw events from both data sources for full context during investigation.

### Possible investigation steps

- Review the SSM command ID in the alert to track the full lifecycle of the command from initiation to execution across both CloudTrail and endpoint data
- Examine the CloudTrail user identity, including the ARN and access key ID, to determine who initiated the SSM command and verify if the activity is authorized
- Analyze the command lines of the executed LOLBins to understand what commands were run and assess their intent, looking for indicators of data exfiltration, reverse shells, or reconnaissance
- Check the source IP address and user agent from the CloudTrail event to identify if the request came from an expected location or tool
- Investigate the affected EC2 instances for other suspicious activities or signs of compromise during the same timeframe, including network connections and file modifications
- Review the SSM shell process details to see the full context of what the SSM agent executed and identify the parent-child process relationships
- Correlate the timing between the CloudTrail event and endpoint execution to ensure they occurred within the detection window and represent the same activity
- Check if the same user identity or source IP has executed similar SSM commands on other EC2 instances in your environment

### False positive analysis

- Routine administrative scripts that use utilities like curl, wget, or python for legitimate configuration management should be documented and excluded by user identity or source IP
- Automated monitoring tools that execute commands via SSM for health checks or data collection can be filtered by identifying their consistent patterns and access key IDs
- DevOps CI/CD pipelines that deploy or test applications using SSM may trigger alerts; create exceptions based on known automation roles or specific command patterns
- Security scanning tools that legitimately use SSM for vulnerability assessments should be allowlisted by their known IAM roles or source IPs
- Scheduled maintenance tasks using LOLBins for backup, log rotation, or data synchronization can be excluded by command pattern matching or execution timing

### Response and remediation

- Immediately isolate the affected EC2 instance from the network to prevent further unauthorized command execution or lateral movement
- Review AWS CloudTrail logs to identify the IAM user, role, or access key associated with the suspicious SSM command and revoke or rotate compromised credentials
- Terminate any unauthorized processes identified on the endpoint that match the LOLBin execution patterns detected in the alert
- Conduct a forensic analysis of the affected EC2 instance to identify any persistence mechanisms, backdoors, or data exfiltration indicators
- Implement stricter IAM policies to limit SSM `SendCommand` permissions to only trusted users and roles, following the principle of least privilege
- Enable multi-factor authentication (MFA) for IAM users with SSM execution privileges to reduce the risk of credential compromise
- Review and update VPC security groups and network ACLs to restrict outbound traffic from EC2 instances to only necessary destinations, preventing data exfiltration
- Escalate the incident to the security operations center (SOC) for further investigation and to determine if additional AWS resources or accounts have been compromised

