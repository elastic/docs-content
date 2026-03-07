---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS IAM Group Deletion" prebuilt detection rule.'
---

# AWS IAM Group Deletion

## Triage and analysis

### Investigating AWS IAM Group Deletion

Attackers sometimes remove groups to erase evidence, disrupt operations, or prevent users from receiving needed permissions (Impact). Deletion can also follow malicious cleanup after attaching policies and using the group briefly. This alert fires on `DeleteGroup` API call. Consider intentional disruption or covering tracks, particularly if the group was privileged or recently modified.

### Possible investigation steps

- **Identify the actor and environment**  
  - Review `aws.cloudtrail.user_identity.arn`, `aws.cloudtrail.user_identity.access_key_id`.  
  - Check `source.ip`, `user_agent.original`, `cloud.account.id`, `cloud.region` for atypical activity.

- **Determine what was lost**
  - From `aws.cloudtrail.request_parameters`, capture `groupName`.  
  - Use history or logs to identify existing members and attached policies prior to deletion (ex: `GetGroup`, `ListAttachedGroupPolicies`).  
  - Determine if the group contained privileged roles/policies that could have been weaponized.

- **Correlate with related activity**
  - Look in the prior 1–24h for `DetachGroupPolicy`, `RemoveUserFromGroup`, `DeleteGroupPolicy`, which often precede deletion in adversary cleanup workflows.  
  - After deletion, monitor for creation of new similarly-named groups, or re-attachment of policies to other groups/roles.

### False positive analysis

- Projects & services that are being decommissioned often require group deletion. Confirm through internal inventory and change control.  
- Sandbox or dev accounts frequently create and delete groups; ensure the environment context is understood.

### Response and remediation

- **Containment**: If deletion was unauthorized, restrict the actor’s IAM privileges and block further configuration changes.  
- **Investigation and scoping**: Recover details of the deleted group (members, policies) from logs or AWS Config, and determine the impact of the deletion (which users lost membership, service account disruption).  
- **Recovery and hardening**: Recreate the group if necessary, restore intended policies and memberships, enforce change-control for group deletions, restrict `iam:DeleteGroup` privileges, and create alerts for destructive IAM operations.

### Additional information
[AWS Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/)
