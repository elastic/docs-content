---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS STS Role Chaining" prebuilt detection rule.
---

# AWS STS Role Chaining

## Triage and analysis

### Investigating AWS STS Role Chaining

Role chaining occurs when a role assumed with temporary credentials (`AssumeRole`) is used to assume another role. While supported by AWS, chaining can increase risk of Privilege escalation, if the second role grants broader permissions; and Persistence, since each chained AssumeRole refreshes the session with up to 1-hour duration. This new terms rule triggers on the first observed combination of one role (`aws.cloudtrail.user_identity.session_context.session_issuer.arn`) assuming another (`aws.cloudtrail.resources.arn`). 

### Possible investigation steps

- **Review Alert Context**: Investigate the alert, focusing on `aws.cloudtrail.user_identity.session_context.session_issuer.arn` (the calling role) and `aws.cloudtrail.resources.arn` (the target role).  

- **Determine scope and intent.** Check `aws.cloudtrail.recipient_account_id` and `aws.cloudtrail.resources.account_id` fields to identify whether the chaining is Intra-account (within the same AWS account) or Cross-account (from another AWS account).  

- **Check role privileges.** Compare policies of the calling and target roles. Determine if chaining increases permissions (for example, access to S3 data, IAM modifications, or admin privileges).  

- **Correlate with other activity.** Look for related alerts or CloudTrail activity within ±30 minutes: policy changes, unusual S3 access, or use of sensitive APIs. Use `aws.cloudtrail.user_identity.arn` to track behavior from the same role session, use `aws.cloudtrail.user_identity.session_context.session_issuer.arn` to track broader behavior from the role itself.

- **Validate legitimacy.** Contact the account or service owner to confirm if the chaining was expected (for example, automation pipelines or federated access flows).  

- **Geography & source.** Review `cloud.region`, `source.address`, and other `geo` fields to assess if the activity originates from expected regions or network ranges.  

### False positive analysis

- **Expected role chaining.** Some organizations use role chaining as part of multi-account access strategies. Maintain an allowlist of known `issuer.arn` - `target.arn` pairs.  
- **Automation and scheduled tasks.** CI/CD systems or monitoring tools may assume roles frequently. Validate by `userAgent` and historical behavior.  
- **Test/dev environments.** Development accounts may generate experimental chaining patterns. Tune rules or exceptions to exclude low-risk accounts.  

### Response and remediation

**Immediate steps**
- **Preserve evidence.** Export triggering CloudTrail events (±30 minutes) into a restricted evidence bucket. Include session context, source IP, and user agent.  
- **Notify owners.** Contact the owners of both roles to validate intent.  

**Containment (if suspicious)**
- **Revoke temporary credentials.** [Revoke Session Permissions](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_revoke-sessions.html) if possible, or attach [AWSDenyALL policy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSDenyAll.html) to the originating role.  
- **Restrict risky roles.** Apply least-privilege policies or temporarily deny `sts:AssumeRole` for suspicious principals.  
- **Enable monitoring.** Ensure CloudTrail and GuardDuty are active in all regions to detect further chaining.  

**Scope and hunt**
- Search for additional AssumeRole activity by the same `issuer.arn` or `resources.arn` across other accounts and regions.  
- Look for privilege escalation attempts (for example, IAM `AttachRolePolicy`, `UpdateAssumeRolePolicy`) or sensitive data access following the chain.  

**Recovery & hardening**
- Apply least privilege to all roles, limiting trust policies to only required principals.  
- Enforce MFA where possible on AssumeRole operations.  
- Periodically review role chaining patterns to validate necessity; remove unused or risky trust relationships.  
- Document and tune new terms exceptions for known, legitimate chains.  

### Additional information
 
- [AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/): NIST-aligned templates for evidence, containment, eradication, recovery, post-incident. 
- [AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/): Practical response steps for account and IAM misuse scenarios
- AWS IAM Best Practices: [AWS docs](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html) for reducing risk from temporary credentials.  

## Setup

The AWS Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.

