---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS RDS DB Instance Made Public" prebuilt detection rule.'
---

# AWS RDS DB Instance Made Public

## Triage and analysis

### Investigating AWS RDS DB Instance Made Public

This rule detects when an Amazon RDS DB instance or cluster is created or modified with
`publiclyAccessible=true`. While some environments operate publicly accessible RDS instances,
unexpected exposure of a database to the internet is a meaningful security risk. Adversaries who
gain access to AWS credentials may modify a DB instance’s public accessibility to exfiltrate data,
establish persistence, or bypass internal network restrictions. 

#### Possible Investigation Steps

- **Identify the actor**
  - Review `aws.cloudtrail.user_identity.arn`, `aws.cloudtrail.user_identity.type`, and `access_key_id` to determine which IAM principal made the change.
  - Determine whether the user, role, or automation service typically manages RDS configurations.

- **Examine the request parameters**
  - Review `aws.cloudtrail.request_parameters` for:
    - `publiclyAccessible=true`
    - DBInstanceIdentifier / DBClusterIdentifier
    - Additional changes included in the same modification request (e.g., master user changes, security group updates)

- **Validate the target resource**
  - Determine the sensitivity of the instance:
    - What data does it store?
    - Is it production, staging, dev, or ephemeral?
  - Confirm whether the instance was previously private.

- **Assess network exposure**
  - Check associated security groups for:
    - `0.0.0.0/0` (unrestricted ingress)
    - Unexpected IP ranges  
  - Review VPC/subnet placement to determine if the instance is reachable externally.

- **Correlate with other recent CloudTrail activity**
  - Look for related events performed by the same actor:
    - `AuthorizeSecurityGroupIngress`
    - `ModifyDBInstance`
    - IAM policy modifications enabling broader DB access
  - Look for indicators of credential misuse:
    - unusual `source.ip`
    - unusual `user_agent.original`
    - MFA not used (`session_context.mfa_authenticated=false`)

- **Validate intent with owners**
  - Contact the service or database owner to confirm whether the change was an approved part of a deployment or migration.

### False Positive Analysis

- **Expected public-access configuration**
  - Some workloads intentionally require public access (e.g., internet-facing reporting tools).
  - Validate against change management tickets, deployment pipelines, or Terraform/IaC automation logs.

### Response and Remediation

- **Containment**
  - If exposure is unauthorized:
    - Modify the instance to disable public access (`publiclyAccessible=false`).
    - Restrict the security group inbound rules immediately.
    - Snapshot the instance to preserve state if compromise is suspected.

- **Investigation**
  - Review all recent actions from the same IAM principal.
  - Check for data access patterns (CloudWatch, RDS Enhanced Monitoring, VPC Flow Logs).
  - Identify whether this exposure correlates with suspicious outbound network activity.

- **Hardening**
  - Require private-only RDS instances unless explicitly documented.
  - Enforce security group least privilege and block public DB access via:
    - AWS Config rules (`rds-instance-public-access-check`)
    - Service Control Policies (SCPs) preventing public RDS settings
  - Implement continuous monitoring for network or configuration drift.

- **Recovery**
  - Restore the database to a private subnet if necessary.
  - Rotate credentials used by the DB instance and associated applications.
  - Document the incident and update policies or IaC templates to prevent recurrence.

### Additional Information:

- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **Security Best Practices:** [AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/).
