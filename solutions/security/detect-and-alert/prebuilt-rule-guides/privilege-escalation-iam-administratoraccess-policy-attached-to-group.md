---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS IAM AdministratorAccess Policy Attached to Group" prebuilt detection rule.
---

# AWS IAM AdministratorAccess Policy Attached to Group

## Triage and analysis

### Investigating AWS IAM AdministratorAccess Policy Attached to Group

The AWS-managed `AdministratorAccess` policy grants full administrative privileges across all AWS services.  
When attached to a group, all group members inherit this access, often unintentionally broadening the blast radius of a compromise.  
Adversaries can exploit `iam:AttachGroupPolicy` permissions to escalate privileges or establish persistence by attaching this policy to an existing user group.

#### Possible investigation steps

- **Identify the affected group and calling principal.**  
  Review `aws.cloudtrail.user_identity.arn` (caller) and `aws.cloudtrail.request_parameters.groupName` (target group).  
  Validate whether this aligns with legitimate change management or automation workflows.  

- **Review group membership.**  
  Enumerate current members using `aws iam get-group`.  
  Determine whether unauthorized users could have gained administrative access as a result.  

- **Inspect CloudTrail details.**  
  Check `source.ip`, `user_agent.original`, and `source.geo` fields for anomalies.  
  Compare with historical operations by the same principal.  

- **Correlate related IAM activity.**  
  Search for adjacent events such as `AddUserToGroup`, `CreateUser`, or `AttachUserPolicy`.  
  These may indicate chained privilege escalation.  

- **Assess propagation of privileges.**  
  If the group has many members or is linked to cross-account roles, the impact may extend beyond a single user.  
  Document all affected identities for containment.  

### False positive analysis

- **Intentional access updates.**  
  Policy attachment may occur during legitimate administrative provisioning. Confirm via ticketing systems.  
- **Automation or compliance tasks.**  
  Some environments use centralized scripts to attach AdministratorAccess temporarily. Validate through automation logs.  

### Response and remediation

**Immediate containment**
- Detach the policy from the affected group (`aws iam detach-group-policy`).  
- Review and limit group membership. Temporarily remove non-essential users or disable access for impacted accounts.  
- Rotate credentials for users who inherited admin privileges from the attachment.  
- Enable MFA on all impacted accounts.  

**Evidence preservation**
- Export the triggering `AttachGroupPolicy` event and related CloudTrail entries ±30 minutes from the alert.  
- Preserve AWS Config and GuardDuty records to support forensic analysis.  

**Scoping and investigation**
- Review additional IAM operations from the same caller (`CreateAccessKey`, `AttachRolePolicy`, `UpdateAssumeRolePolicy`).  
- Identify whether new groups or roles were created shortly before or after the event.  
- Check for subsequent API activity by newly privileged users (for example, S3, EC2, or IAM modifications).  

**Recovery and hardening**
- Reinforce least privilege, avoid assigning `AdministratorAccess` to groups.  
- Use role-based access control with scoped permissions.   
- Enable CloudTrail, GuardDuty, and Security Hub across all regions.  
- Implement SCPs at the organization level to restrict direct `AdministratorAccess` attachments.  

### Additional information
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/): response steps related to IAM policy modification and unauthorized privilege escalation..  
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/): for containment, analysis, and recovery guidance.
- **AWS Documentation:** [AdministratorAccess Policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_job-functions.html#jf_administrator).

