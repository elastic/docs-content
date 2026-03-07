---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS RDS DB Instance Restored" prebuilt detection rule.
---

# AWS RDS DB Instance Restored

## Triage and analysis

### Investigating AWS RDS DB Instance Restored

Restoring an RDS DB instance from a snapshot or from S3 is a powerful operation that recreates a full database environment. While legitimate for recovery, migrations, or cloning, adversaries may use restore actions to access historical data, duplicate sensitive environments, evade guardrails, or prepare for data exfiltration. 

This rule detects successful invocation of `RestoreDBInstanceFromDBSnapshot` and `RestoreDBInstanceFromS3`, both of which may indicate attempts to rehydrate old datasets, bypass deletion protection, or establish a shadow environment for further malicious actions.

#### Possible investigation steps

- **Identify the actor and execution context**
  - Review `aws.cloudtrail.user_identity.arn`, `aws.cloudtrail.user_identity.type`, and `aws.cloudtrail.user_identity.access_key_id`.
  - Check `user.name`, `source.ip`, and `user_agent.original` to determine how the restore was executed (console, CLI, automation, SDK).

- **Understand what was restored and why**
  - Inspect `aws.cloudtrail.request_parameters` to identify:
    - Snapshot identifier or S3 location used as the restore source.
    - The new DB instance identifier and configuration parameters.
  - Determine:
    - Whether the snapshot/backup used for the restore contains sensitive or high-value data.
    - Whether this restore created a publicly accessible instance, changed security groups, or used unusual storage/instance classes.

- **Reconstruct the activity flow**
  - Use `@timestamp` to correlate the restore event with:
    - Snapshot creation, copy, or export events.
    - IAM policy changes or privilege escalations.
    - Deletion or modification of the original database.
    - Other RDS lifecycle actions such as `ModifyDBInstance`, `DeleteDBInstance`, or backup configuration changes.
  - Look for signs of attacker staging:
    - Prior enumeration activity (`DescribeDBSnapshots`, `DescribeDBInstances`).
    - Recent logins from unusual IPs or federated sessions without MFA.

- **Correlate with broader behavior**
  - Pivot in CloudTrail on:
    - The same snapshot identifier.
    - The same actor or access key ID.
    - The newly created DB instance identifier.
  - Examine:
    - Whether the restored DB was modified immediately after (e.g., security groups opened, deletion protection disabled).
    - Whether there were large-volume read operations or export actions following the restore.
    - Whether the restore is part of a pattern of parallel suspicious activity (snapshot copying, S3 backups, cross-account actions).

- **Validate intent with owners**
  - Confirm with the application/database/platform teams:
    - Whether the restore was requested or part of an authorized operational workflow.
    - Whether this restore corresponds to migration, testing, DR drill, or another planned activity.
    - Whether the restored environment should exist (and for how long).

### False positive analysis

- **Legitimate maintenance and DR workflows**
  - Many teams restore databases for patch testing, DR validation, schema testing, or migration.
- **Automated restore workflows**
  - CI/CD pipelines or internal automation may restore DBs to generate staging or dev environments.
- **Third-party tooling**
  - Backup/DR solutions, migration tools, or observability platforms may restore DB instances for operational reasons. Tune based on `user_agent.original` or known service roles.

### Response and remediation

- **Contain the restored environment**
  - If unauthorized:
    - Apply restrictive security groups to block access.
    - Disable public accessibility if enabled.
    - Evaluate whether deletion protection or backup retention is misconfigured.

- **Assess data exposure and intent**
  - Work with data owners to evaluate:
    - The sensitivity of the restored environment.
    - Whether any reads, dumps, or exports occurred post-restore.
    - Whether the restore enabled the attacker to access older or deleted data.

- **Investigate scope and related activity**
  - Review CloudTrail for:
    - Additional restores, exports, or copies.
    - IAM changes allowing expanded privileges.
    - Unusual authentication events or federated sessions without MFA.
    - Related destructive actions (snapshot deletion, backup disabled, instance deletion).

- **Hardening and preventive controls**
  - Enforce least privilege for `rds:RestoreDBInstanceFromDBSnapshot` and `rds:RestoreDBInstanceFromS3`.
  - Use IAM conditions to restrict restore actions by network, principal, or region.
  - Add AWS Config and Security Hub controls for monitoring:
    - Unapproved restores.
    - Public or misconfigured restored instances.
  - Consider SCPs that prevent RDS restores in production accounts except through controlled roles.

- **Post-incident improvements**
  - Rotate credentials for affected IAM users/roles.
  - Update change management processes to ensure restore actions are tracked and approved.
  - Adjust rule exceptions sparingly and ensure high-risk restores continue to generate alerts.

### Additional information

- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **Security Best Practices:** [AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/).

