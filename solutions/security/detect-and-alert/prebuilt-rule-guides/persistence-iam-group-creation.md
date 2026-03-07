---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS IAM Group Creation" prebuilt detection rule.'
---

# AWS IAM Group Creation

## Triage and analysis

### Investigating AWS IAM Group Creation

AWS IAM allows organizations to manage user access and permissions securely. Groups in IAM simplify permission management by allowing multiple users to inherit the same permissions. However, adversaries may exploit this by creating unauthorized groups to gain persistent access. This alert fires on `CreateGroup`. New group creation may indicate attacker staging for persistence, especially if followed by policy attachments or user additions.

#### Possible investigation steps

- **Identify the actor and context**  
  - Check `aws.cloudtrail.user_identity.arn`, `aws.cloudtrail.user_identity.access_key_id` to determine who performed the group creation.  
  - Review `source.ip`, `user_agent.original`, `cloud.account.id`, `cloud.region` for unusual network, client, or region usage.

- **Examine the group details**  
  - From `aws.cloudtrail.response_elements`, extract `groupName` and `path` (e.g., /service/, /dev/).
  - Look for immediate follow-on changes by the same actor within the next 15–30 minutes:
    - AttachGroupPolicy (especially AdministratorAccess or broad s3:*, iam:*).
    - AddUserToGroup (who was added and when?).
  - Use GetGroup to enumerate current group membership and attached policies during triage.

- **Correlate with broader activity**  
  - Look for prior suspicious actions by the same user: `AssumeRole`, `CreateAccessKey`, new IAM user/role.  
  - After group creation, watch for data-access or configuration changes (e.g., S3 policy updates, KMS key policy changes) 

### False positive analysis

- IAM onboarding workflows or DevOps pipelines creating groups for new projects can trigger this alert.  
- Test or sandbox accounts often create and delete groups routinely, validate account context and approval flows.

### Response and remediation:

- **Containment**: 
  - If suspicious, disable further changes by the actor (temporarily remove IAM write privileges or deactivate keys).
  - Place a change freeze on the newly created group (block `AttachGroupPolicy`/`AddUserToGroup` via SCP/permissions boundary until review completes).

- **Investigation and scoping**: 
  - Use `GetGroup`, `ListAttachedGroupPolicies`, `ListUsersInGroup` to enumerate the group’s state and identify any suspicious policies or members. Investigate any attached policies granting broad privileges. 
  - Hunt for same-actor `AttachGroupPolicy`/`AddUserToGroup` events across the last 24–48h.
 
- **Recovery and hardening**: 
  - Delete unauthorized, unused or suspicious groups. remove rogue policies/members.
  - Restrict who can call `iam:CreateGroup`, `iam:AttachGroupPolicy`, and `iam:AddUserToGroup` (least privilege). 

### Additional information
[AWS Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/)
