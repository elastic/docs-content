---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS Discovery API Calls via CLI from a Single Resource" prebuilt detection rule.
---

# AWS Discovery API Calls via CLI from a Single Resource

## Triage and analysis

### Investigating AWS Discovery API Calls via CLI from a Single Resource

This rule detects when a single AWS identity executes more than five unique discovery-related API calls (`Describe*`, `List*`, `Get*`, or `Generate*`) within a 10-second window using the AWS CLI.  
High volumes of diverse “read-only” API calls in such a short period can indicate scripted reconnaissance, often an early phase of compromise after credential exposure or access to a compromised EC2 instance.  

#### Possible Investigation Steps

**Identify the actor and session context**
- **Actor ARN (`aws.cloudtrail.user_identity.arn`)**: Determine which IAM user, role, or service principal performed the actions.  
  - Check whether this identity normally performs enumeration activity or belongs to automation infrastructure.  
- **Identity type (`Esql.aws_cloudtrail_user_identity_arn_type`)**: Validate if the caller is a human IAM user, assumed role, or federated identity. Unusual types (e.g., temporary credentials from an unfamiliar role) may indicate lateral movement.  
- **Access key (`Esql.aws_cloudtrail_user_identity_access_key_id_values`)** – Identify which specific access key or temporary credential was used.  
  - If multiple suspicious keys are found, use AWS IAM console or `aws iam list-access-keys` to determine when they were last used or rotated.  
- **Account (`Esql.cloud_account_id_values`)** – Confirm which AWS account was affected and whether it matches the intended operational context (e.g., production vs. sandbox).

**Assess the API call pattern and intent**
- **Distinct action count (`Esql.event_action_count_distinct`)**: Note how many unique API calls occurred within each 10-second window. Counts far above normal operational baselines may indicate scripted reconnaissance.  
- **API actions (`Esql.event_action_values`)**: Review which discovery APIs were invoked.  
  - Focus on services such as EC2 (`DescribeInstances`), IAM (`ListRoles`, `ListAccessKeys`), S3 (`ListBuckets`), and KMS (`ListKeys`), which adversaries frequently query to map assets.  
- **Service providers (`Esql.event_provider_values`)**: Identify which AWS services were targeted.  
  - Multi-service enumeration (IAM + EC2 + S3) suggests broad discovery rather than a specific diagnostic task.  
- **Time window (`Esql.time_window_date_trunc`)**: Verify whether activity occurred during normal maintenance windows or outside expected hours.

**Analyze the source and origin**
- **Source IP (`Esql.source_ip_values`)**: Check the originating IPs to determine whether the calls came from a known internal host, an EC2 instance, or an unfamiliar external network.  
  - Compare with known corporate CIDR ranges, VPC flow logs, or guardrail baselines.  
- **Source organization (`Esql.source_as_organization_name_values`)**: Review the associated ASN or organization.  
  - If the ASN belongs to a commercial ISP or VPN service, investigate possible credential compromise or remote attacker usage.

**Correlate with additional events**
- Search CloudTrail for the same `aws.cloudtrail.user_identity.arn` or `aws_cloudtrail_user_identity_access_key_id_values` within ±30 minutes.  
  - Look for follow-on actions such as `GetCallerIdentity`, `AssumeRole`, `CreateAccessKey`, or data access (`GetObject`, `CopySnapshot`).  
  - Correlate this enumeration with authentication anomalies or privilege-related findings.  
- Cross-reference `Esql.cloud_account_id_values` with other alerts for lateral or privilege escalation patterns.

### False positive analysis

Legitimate, high-frequency API activity may originate from:
- **Inventory or compliance automation**: Scripts or tools such as AWS Config, Cloud Custodian, or custom CMDB collection performing periodic Describe/List calls.  
- **Operational monitoring systems**: DevOps pipelines, Terraform, or deployment verifiers enumerating resources.  
- **Security tooling**: Security scanners performing asset discovery across services.

Validate by confirming:
- Whether the `aws.cloudtrail.user_identity.arn` corresponds to a documented automation or monitoring identity.  
- That the observed `Esql.event_action_values` match known inventory or cost-reporting workflows.  
- Timing alignment with approved maintenance schedules.

### Response and remediation

If the activity is unexpected or originates from unrecognized credentials, follow AWS’s incident-handling guidance:

**Contain**
- Temporarily disable or rotate the access key (`Esql.aws_cloudtrail_user_identity_access_key_id_values`) using IAM.  
- Restrict outbound connectivity for the instance or resource from which the API calls originated.

**Investigate**
- Retrieve full CloudTrail logs for the actor and `Esql.time_window_date_trunc` interval.  
- Identify any subsequent write or privilege-modification actions.  
- Review associated IAM policies for excessive permissions.

**Recover and Harden**
- Rotate credentials, enforce MFA on human users, and tighten IAM role trust policies.  
- Implement AWS Config rules or SCPs to monitor and restrict large-scale enumeration.

**Post-Incident Actions**
- Document the finding and response in your organization’s IR management system.  
- Update detection logic or allow-lists for known benign automation.  
- Validate recovery by confirming no new suspicious discovery bursts occur.

### Additional information

- **AWS Documentation**
  - [CloudTrail Event Reference](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference.html)
  - [AWS Security Incident Response Guide](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/aws-security-incident-response-guide.pdf)
- **AWS Playbook Resources**
  - [AWS Incident Response Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/tree/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks)
  - [AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework)


