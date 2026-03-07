---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS IAM Login Profile Added for Root" prebuilt detection rule.
---

# AWS IAM Login Profile Added for Root

## Triage and analysis

### Investigating AWS IAM Login Profile Added for Root

This rule detects when a console login profile is created for the AWS root account.  
A login profile enables password-based console access, and because the root user has unrestricted privileges, creating one is an extremely high-impact event. Adversaries who temporarily gain root-level credentials (for example, through an STS session or credential compromise) may use `CreateLoginProfile` without specifying a `userName` to add a password to the root account. This grants persistent access even if the attacker’s API keys are later rotated or disabled.

### Possible investigation steps

**Assess the timing and context of the event**
- Review the `@timestamp` to determine when the `CreateLoginProfile` call occurred.  
  - Correlate this time window with other root or IAM activity such as `AssumeRoot`, `GetSessionToken`, `ConsoleLogin`, or `CreateAccessKey`.  
  - Check for follow-on activity, especially `ConsoleLogin` events or `UpdateLoginProfile`, which may indicate that the root password was used immediately after creation.

**Investigate event origin and session details**
- Review `source.ip` and `user_agent.original`:
  - Determine if the request originated from an expected network range, VPN endpoint, or geolocation.
  - Identify whether the access was interactive (for example, browser or AWS console) or automated (`aws-cli`, SDK, or API client).
- Examine `aws.cloudtrail.user_identity.access_key_id` and associated STS session context to see if temporary credentials were used.
- Compare this event’s IP and access key to any other recent CloudTrail activity to identify potential lateral movement or multi-account access attempts.

**Analyze the login profile creation**
- Review `aws.cloudtrail.request_parameters` and `aws.cloudtrail.response_elements`:
  - Check whether `passwordResetRequired` was set to `true` or omitted, absence may imply that the attacker created a password they intend to reuse.
- Cross-reference this action with previous failed login attempts, password recovery requests, or `AssumeRoot` behavior.

**Correlate related identity and access behavior**
- Search for additional IAM management activity:
  - `AttachUserPolicy`, `AttachRolePolicy`, or `PutUserPolicy` granting elevated permissions.
  - New `AccessKey` creation or `UpdateAccessKey` events tied to the same session.
- Review GuardDuty findings or any other detections referencing this account or IP around the same time period.
- If available, correlate with CloudTrail to detect if other resource creation or configuration changes followed the login profile addition.

**Validate with account owner or authorized personnel**
- Contact the designated account or root credential owner to confirm whether this action was intentional (for example, during an account recovery).
- Review any internal change-management or service ticketing systems for an approved request matching this activity.

### False positive analysis

Although rare, legitimate scenarios include:
- **Authorized account recovery** : An administrator or AWS Support might temporarily add a root login profile to regain access. Validate against documented recovery workflows.  
- **Controlled testing or sandbox environments** : Certain sandbox accounts may reuse root credentials for automation or demonstration purposes. Tag and exclude these accounts from this rule where appropriate.  
- **Automated provisioning** : Review any account bootstrap or recovery automation scripts that may invoke `CreateLoginProfile` on root credentials.

For any potential false positive, verify that:
- The `source.ip` and `user_agent.original` values align with expected administrative locations and tools.  
- The change was recorded during a maintenance window or known security operation.

### Response and remediation

> Any unapproved creation of a login profile for the root account is a critical security incident requiring immediate containment and credential rotation.

**Containment**
- Delete the newly created root login profile if it was not authorized.  
- Rotate the root account password using AWS’s official password-reset workflow.  
- Revoke any active sessions, temporary credentials, or tokens associated with this event.  
- Verify that multi-factor authentication (MFA) is enabled and functioning on the root account.  
- Check that no root access keys exist — if present, remove them immediately.

**Investigation and scoping**
- Examine CloudTrail logs from 30 minutes before and after this event to identify correlated actions.  
- Capture and securely store these logs in an isolated S3 bucket with Object Lock enabled to preserve forensic integrity.  
- Investigate for additional IAM or STS operations by the same `access_key_id` or IP address that may indicate privilege escalation or persistence attempts.  
- Review whether any new IAM roles, users, or policies were created in proximity to this event.

**Recovery and hardening**
- Reset the root password and distribute the new credentials securely to authorized custodians only.  
- Ensure MFA is enforced for all administrative and root-level access.  
- Audit all IAM policies for least-privilege adherence, focusing on `iam:CreateLoginProfile`, `iam:UpdateLoginProfile`, and `iam:CreateAccessKey` permissions.  
- Enable Cloudtrail, GuardDuty, AWS Config, and Security Hub across all regions for continuous monitoring of root and IAM activity.  
- Review your organization’s playbooks and detection coverage for root-level persistence techniques, and update procedures as needed.

**Post-incident actions**
- Notify AWS account owners and your security operations center of the incident.  
- Conduct a post-mortem to determine the initial vector of compromise (e.g., stolen credentials, misconfigured role chaining, or insufficient MFA).  
- Update alerting thresholds and detection logic to minimize mean time to detect (MTTD) and respond (MTTR).

### Additional information

- **AWS Incident Response Playbooks**  
  - [IRP-CredCompromise](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/IRP-CredCompromise.md) – Containment and recovery for suspected credential abuse.  
- **AWS Customer Playbook Framework**  
  - [Compromised_IAM_Credentials.md](https://github.com/aws-samples/aws-customer-playbook-framework/blob/a8c7b313636b406a375952ac00b2d68e89a991f2/docs/Compromised_IAM_Credentials.md) – Steps to contain, investigate, and recover from credential compromise.  
- **AWS Documentation**  
  - [CreateLoginProfile API Reference](https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateLoginProfile.html)  
  - [Root User Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user-best-practices.html)

