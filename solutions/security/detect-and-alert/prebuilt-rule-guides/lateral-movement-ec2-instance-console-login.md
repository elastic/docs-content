---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS EC2 Instance Console Login via Assumed Role" prebuilt detection rule.'
---

# AWS EC2 Instance Console Login via Assumed Role

## Triage and analysis

### Investigating AWS EC2 Instance Console Login via Assumed Role

This rule detects successful AWS console or federation logins using temporary credentials tied to EC2 instance profiles. Under normal conditions, EC2 instances use their temporary credentials for programmatic API access — **not** for interactive console sessions. When an attacker gains access to an instance’s IMDS (Instance Metadata Service) or its environment variables, they may retrieve temporary STS credentials and attempt console logins to gain full access to the AWS account. A successful login of this type is rare and high-risk, as it strongly suggests credential theft or unauthorized session hijacking.

#### Possible investigation steps

- **Identify the source and actor**
  - Review `aws.cloudtrail.user_identity.arn`, `user.id`, and `user_agent.original` fields to confirm the session originated from an EC2 instance (`:i-` pattern).
  - Correlate the instance ID (`i-xxxxxx`) with the specific EC2 instance in your environment to identify its owner, purpose, and running applications.
  - Check `source.ip` and `cloud.region` to determine if the login originated from within AWS infrastructure (expected) or an external location (suspicious).

- **Correlate surrounding activity**
  - Pivot in Timeline to view the sequence of events leading up to the login, including:
    - STS token retrievals (`GetSessionToken`, `AssumeRole`, `GetCallerIdentity`)
    - Calls to the IMDS endpoint or local credential exfiltration attempts from the instance.
  - Investigate whether the same role or credentials were used for API actions following the login (e.g., `CreateUser`, `AttachRolePolicy`, or `ListBuckets`).

- **Assess IAM role exposure**
  - Determine which IAM role was associated with the instance at the time of the event and review its attached permissions.
  - Evaluate whether the role grants console access or permissions beyond what that workload normally requires.
  - Check for any recent changes to that role’s trust policy or attached policies.

- **Validate authorization**
  - Contact the EC2 instance owner or service team to confirm if any legitimate process should be logging in to the console.
  - If no legitimate activity can explain the login, treat the credentials as compromised.

### False positive analysis

This is very uncommon behavior.  
Known legitimate causes include:
- AWS or internal security automation that programmatically initiates console sessions for validation or testing.
- Forensic or incident-response automation that logs in using temporary credentials from a compromised instance.
- Red-team or penetration-testing activity designed to validate IMDS exposure or lateral movement scenarios.

For any other occurrence, treat the alert as potentially malicious.  
Validate through:
- The originating instance’s purpose and owner.
- Known automation patterns in `user_agent.original`.
- The timestamp alignment with planned testing or security validation.

### Response and remediation

- **Immediate containment**
  - Revoke the temporary credentials for the affected role (`aws sts revoke-session-token` or rotate the role credentials).
  - Isolate the associated EC2 instance (e.g., detach it from the VPC or security groups) to prevent further credential misuse.
  - Invalidate active console sessions via AWS CLI or the AWS Console.

- **Investigation and scoping**
  - Review CloudTrail logs for all actions associated with the compromised role in the preceding 24 hours.
  - Determine if additional roles or instances show similar `ConsoleLogin` patterns.
  - Search for network indicators of IMDS exploitation (e.g., requests to `169.254.169.254` from unauthorized binaries or users).

- **Recovery and hardening**
  - Rotate all credentials for affected roles and users.
  - Apply IMDSv2 enforcement to prevent credential harvesting from EC2 metadata.
  - Implement restrictive IAM policies: deny console access (`iam:PassRole`, `sts:GetFederationToken`) for non-human roles.

### Additional information
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **Security Best Practices:** [AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/).
