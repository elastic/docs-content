---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS RDS DB Snapshot Shared with Another Account" prebuilt detection rule.
---

# AWS RDS DB Snapshot Shared with Another Account

## Triage and analysis

### Investigating AWS RDS DB Snapshot Shared with Another Account

Amazon RDS DB snapshots capture full backups of database instances and clusters. Modifying a snapshot’s restore
attributes to include external AWS accounts allows those accounts to restore and fully access the underlying data.
While cross-account snapshot sharing is widely used for migrations and disaster-recovery workflows, adversaries may
abuse this mechanism for stealthy data exfiltration, restoring the snapshot in infrastructure they control, outside of your monitoring boundary.

This rule detects successful modifications to snapshot attributes where one or more additional AWS accounts are added to the snapshot’s restore permissions.

#### Possible investigation steps

- **Identify the actor and context**
  - Review `aws.cloudtrail.user_identity.arn` and `aws.cloudtrail.user_identity.access_key_id`.
  - Determine whether the caller is an automation role, interactive user, CI/CD pipeline, or previously unseen principal.
  - Check `source.ip` and `user_agent.original` for signs of unauthorized access or atypical tooling.

- **Understand what snapshot was shared**
  - From `aws.cloudtrail.request_parameters`, extract:
    - The snapshot or cluster snapshot identifier.
    - The list of `valuesToAdd` accounts added to `attributeName=restore`.
  - Identify the associated database instance or cluster and evaluate:
    - Data classification level (PII, customer data, secrets, credentials, financials, etc.)
    - Application ownership and business impact.

- **Validate the external account**
  - Determine whether the recipient account:
    - Belongs to your AWS Organization.
    - Has previously been authorized for snapshot restore operations.
    - Represents a new or unexpected dependency.
  - Cross-reference with known partner accounts or migration plans.

- **Correlate with related activity**
  - Pivot in CloudTrail on the same user identity or account to identify:
    - Prior reconnaissance actions (`DescribeDBSnapshots`, `DescribeDBInstances`).
    - Snapshot copying or creation of manual snapshots just before sharing.
    - IAM privilege escalation (`AttachRolePolicy`, `PutUserPolicy`, `AssumeRole` patterns).
    - Unusual RDS configuration changes (backup retention decrease, deletion protection toggles).

- **Assess for exfiltration indicators**
  - Look for:
    - Subsequent `CopyDBSnapshot` or `StartExportTask` events.
    - Snapshot downloads, exports, or restoration from the external account.
    - Snapshot attributes set to `all` (public sharing), which is extremely dangerous.

- **Validate operational intent**
  - Contact application owners, DBAs, or platform teams to confirm:
    - Whether migration, replication, or DR workflows explain the share.
    - Whether new accounts were intentionally onboarded.
    - Whether the timing aligns with approved change windows.

### False positive analysis

- **Legitimate migration or DR workflows**
  - Many organizations routinely share snapshots with other accounts for staging, analytics, or DR replication.

- **Automation roles**
  - Infrastructure-as-code pipelines and backup automation tools may modify snapshot permissions as part of normal behavior.

If behavior is expected and consistently performed by a known principal, tune the rule using exceptional user identities, service roles, or controlled organizational accounts.

### Response and remediation

- **Revoke unauthorized sharing**
  - Immediately remove unauthorized accounts from snapshot restore attributes.
  - Ensure the snapshot is not publicly shared.

- **Contain potential compromise**
  - Rotate access keys or credentials for the principal that performed the modification.
  - Review IAM permissions to ensure only approved roles can share snapshots.

- **Assess impact**
  - Determine whether the external account restored the snapshot and accessed data.
  - If data exposure is likely, notify compliance, legal, and incident response teams.

- **Hardening and preventive controls**
  - Restrict snapshot sharing via IAM condition keys (`kms:ViaService`, `rds:dbSnapshotArn`, `aws:PrincipalArn`).
  - Use AWS Organizations SCPs to block cross-account snapshot sharing in production accounts.
  - Enable Config rules and Security Hub controls for public or cross-account snapshot access.

### Additional information
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **Security Best Practices:** [AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/).

