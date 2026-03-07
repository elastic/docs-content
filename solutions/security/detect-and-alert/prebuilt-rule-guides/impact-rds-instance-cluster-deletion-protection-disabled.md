---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS RDS DB Instance or Cluster Deletion Protection Disabled" prebuilt detection rule.'
---

# AWS RDS DB Instance or Cluster Deletion Protection Disabled

## Triage and analysis

### Investigating AWS RDS DB Instance or Cluster Deletion Protection Disabled
 
Deletion protection is designed to safeguard RDS DB instances and clusters from accidental or unauthorized deletion. An adversary with privileged access in a compromised environment, can disable this safeguard before issuing a `DeleteDBInstance` or `DeleteDBCluster` action. This rule detects successful attempts to modify deletionProtection and set it to false on any RDS instance or cluster.

#### Possible investigation steps

- **Identify the Actor**
  - Review `aws.cloudtrail.user_identity.arn`, `aws.cloudtrail.user_identity.type`, and `access_key_id` to determine which IAM principal made the change.
  - Validate whether this principal normally performs RDS lifecycle operations.

- **Review Event Details**
  - Inspect `aws.cloudtrail.request_parameters` to confirm the targeted DB instance or cluster identifier.
  - Confirm that the request explicitly contains `deletionProtection=false`.

- **Contextualize the Change**
  - Determine if recent activities justify the removal of deletion protection (migration, decommissioning, or maintenance).
  - Compare the timestamp to normal operational hours or deployment windows.

- **Correlate with Additional Activity**
  - Look for subsequent or preceding RDS actions such as:
    - `DeleteDBInstance`
    - `DeleteDBCluster`
    - Security group modifications
    - Changes to parameter groups or backup retention policies.
  - Sudden removal of backups or snapshots may indicate imminent destructive activity.

- **Verify Environmental Risk**
  - Assess the sensitivity of data stored in the affected DB instance or cluster.
  - Determine if the instance is production, customer-facing, or mission-critical.

- **Interview Relevant Personnel**
  - Confirm with service owners or DB administrators whether the modification was intended and approved.

### False positive analysis

- **Expected Decommissioning**
  - Instances undergoing teardown or migration legitimately require deletion protection to be disabled first.

- **Inconsistent Historical Behavior**
  - Compare the action to historical modification patterns for the user or role. If the action aligns with past legitimate changes, it may not be suspicious.

### Response and remediation

- **Immediate Remediation**
  - If unauthorized, re-enable deletion protection (`deletionProtection=true`) on the affected DB instance or cluster.
  - Review security groups, backup retention, and snapshot policies for additional unauthorized changes.

- **Access Review**
  - Investigate credential exposure for the IAM principal that performed the action.
  - Rotate access keys or temporarily revoke permissions if compromise is suspected.

- **Containment**
  - If destructive intent is suspected, apply guardrails (e.g., IAM condition keys, SCPs) to prevent DB deletion.

- **Audit and Harden**
  - Ensure RDS instances adhere to least-privilege principles.
  - Restrict who can modify `ModifyDBInstance` or `ModifyDBCluster` destructive settings, such as deletion protection, backup retention, and public accessibility.

- **Incident Response Activation**
  - Treat unauthorized removal of deletion protection as a high-risk precursor to data destruction.
  - Trigger IR processes for containment, root cause analysis, and post-incident hardening.

### Additional information

- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **Security Best Practices:** [AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/).
