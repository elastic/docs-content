---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS IAM User Addition to Group" prebuilt detection rule.
---

# AWS IAM User Addition to Group

## Triage and analysis

### Investigating AWS IAM User Addition to Group

This rule detects when an IAM user is added to an IAM group via the `AddUserToGroup` API call. If the target group holds elevated privileges, this action may immediately grant that user wide-ranging access useful for credential misuse or lateral movement. This rule helps detect unauthorized privilege escalation via group membership change. Treat as high-risk when the destination group has wide scope (e.g., AdministratorAccess or permissive inline policies).

#### Possible investigation steps

- **Identify the actor and target**  
  - Check `aws.cloudtrail.user_identity.arn` for who added the user.  
  - From `aws.cloudtrail.request_parameters`, capture `userName` (added user) and `groupName` (destination group).  
  - Check `source.ip`, `user_agent.original`, `cloud.region` for unusual patterns.

- **Examine the group’s privileges**  
  - Use `GetGroup`, `ListAttachedGroupPolicies` to see what policies the group holds. Look for `AdministratorAccess`, `iam:*`, `s3:*`, `ec2:*` or cross-account permissions.  
  - Check whether the group was recently created (`CreateGroup`) or recently escalated (`AttachGroupPolicy`). Common attacker pattern: create > attach policy > add user.

- **Correlate with surrounding activity**  
  - Look for preceding events by the actor: `AssumeRole`, `GetSessionToken`, `CreateAccessKey`, `AttachGroupPolicy`.  
  - Follow the added user’s activities after group membership. Look for sensitive operations (e.g., IAM actions, S3 policy changes, EC2 snapshot/AMI activity).


### False positive analysis

- Onboarding or role transitions may legitimately add users to groups.  
- Automated Identity-Management pipelines may add many users to service groups; validate know

### Response and remediation

- **Containment**:
  - If unapproved, remove the user from the group immediately (`RemoveUserFromGroup`) and rotate their access keys.
  - Temporarily restrict group policy changes while assessing blast radius.

- **Investigation and scoping**:
  - Review all actions executed by the newly added user since the change (ex: PutBucketPolicy, CreateAccessKey, PassRole).
  - Confirm whether other users were added to the same group within the same window. 

- **Recovery and hardening**: 
  - Enforce least privilege by redesigning large-group membership. 
  - Restrict `iam:AddUserToGroup` to only appropriate service principals with approval workflow. 
  - Create detections for AttachGroupPolicy to powerful policies and for mass AddUserToGroup patterns.

### Additional information
[AWS Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/)

