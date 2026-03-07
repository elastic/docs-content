---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS SSM Session Started to EC2 Instance" prebuilt detection rule.'
---

# AWS SSM Session Started to EC2 Instance

## Triage and analysis

### Investigating AWS SSM Session Started to EC2 Instance

This rule detects the first instance of an AWS user or role initiating an SSM session to an EC2 instance, which could be indicative of legitimate administrative activities or potential malicious actions like command execution or lateral movement.

#### Possible Investigation Steps

- **Examine the Session Start Event**: Review the AWS CloudTrail log for the event.
    - Determine the target EC2 instance using `aws.cloudtrail.request_parameters`.
- **Verify User Identity and Role**: Check the user’s ARN and access key ID (`aws.cloudtrail.user_identity.access_key_id`).
    - Determine if their role typically requires initiating SSM sessions.
- **Assess Geographic and IP Context**: Analyze the source IP (`source.ip`) and geographic location (`source.geo`) from which the session was initiated.
    - Determine if these are consistent with typical user locations or if they raise suspicions of compromise or misuse.
- **Review Session Details**: Examine details like the session ID and stream URL (`aws.cloudtrail.response_elements`) to understand the scope and nature of the session.
    - Check if any commands executed during the session were unauthorized or out of ordinary practices.
- **Correlate with Other Security Events**: Look for other related security events around the time of the session start to identify any pattern or broader attack vector that may involve this user or EC2 instance.

### False Positive Analysis

- **Legitimate Administrative Activities**: Confirm whether the SSM session was initiated for valid administrative purposes such as system maintenance, patching, or configuration updates. Verify with the respective teams or personnel.

### Response and Remediation

- **Incident Response Activation**: If malicious intent or actions are confirmed, activate the incident response protocol.
    - This includes containment of the threat, eradication of the adversary’s presence, recovery of affected systems, and a thorough investigation.
- **Validate and Reinforce Security Policies**: Ensure that policies around SSM session initiation are strict and adhere to the principle of least privilege.
    - Update IAM policies if necessary to tighten controls.
- **Enhance Monitoring and Alerts**: Improve monitoring of SSM sessions, particularly focusing on sessions that involve sensitive or critical EC2 instances.
    - Adjust alerting mechanisms to flag unusual session initiations promptly.

### Additional Information

For more in-depth understanding of managing SSM sessions and security best practices, refer to the [AWS Systems Manager documentation](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_StartSession.html). Additionally, consider the security implications and best practices outlined in [AWS SSM privilege escalation techniques](https://cloud.hacktricks.xyz/pentesting-cloud/aws-security/aws-privilege-escalation/aws-ssm-privesc).
