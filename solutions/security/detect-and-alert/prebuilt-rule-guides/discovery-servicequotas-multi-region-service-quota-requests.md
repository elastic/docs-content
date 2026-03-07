---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS Service Quotas Multi-Region GetServiceQuota Requests" prebuilt detection rule.
---

# AWS Service Quotas Multi-Region GetServiceQuota Requests

## Triage and analysis

### Investigating AWS Service Quotas Multi-Region GetServiceQuota Requests

AWS Service Quotas define usage limits for AWS services and are commonly referenced during capacity planning or automation. However, adversaries frequently enumerate EC2 on-demand instance quotas across many regions to identify where they can rapidly deploy compute resources for malicious purposes such as cryptocurrency mining, botnet hosting, or malware staging. This rule detects unusually fast, multi-region enumeration of the EC2 on-demand vCPU quota (`L-1216C47A`), a pattern that is uncommon for normal administrative activity and strongly associated with cloud infrastructure discovery.

### Possible investigation steps

**Identify the actor**
- Review `aws.cloudtrail.user_identity.arn` and `aws.cloudtrail.user_identity.access_key_id` to determine whether the requests originated from an IAM user, role, or assumed role. Validate whether this principal is expected to perform quota discovery or capacity analysis across many regions.

**Evaluate the scope of discovery**
- Review the `cloud.region` values to determine which regions were queried and whether they align with regions normally used by your organization. Rapid enumeration of rarely used or disabled regions increases suspicion.

**Inspect request origin and tooling**
- Review `source.ip`, `source.as.organization.name`, and `user_agent.original` to determine whether the activity originated from a trusted corporate network, known cloud automation environment, or an unexpected hosting provider or VPN.
- Unexpected user agents or hosting providers may indicate compromised credentials or an attacker-controlled instance.

**Correlate with follow-on activity**
- Search for subsequent EC2-related actions such as `RunInstances`, `RequestSpotInstances`, `CreateLaunchTemplate`, or `ModifyInstanceAttribute` following the quota discovery.
- Review recent IAM activity for the same principal, including access key creation, role assumptions, or policy changes.

**Assess intent and risk**
- Determine whether this activity aligns with a known operational task (capacity planning, onboarding, automation testing), or whether it represents unexplained reconnaissance behavior.
- If the principal is newly created, rarely used, or exhibiting other anomalous behavior, treat this as high risk.

### False positive analysis
- Multi-region quota discovery may be legitimate in organizations with global deployments, centralized cloud governance, or automated capacity monitoring.
- Infrastructure-as-code pipelines, quota management tools, or internal cloud platforms may periodically enumerate quotas.

### Response and remediation
- If the activity is unauthorized or suspicious, immediately rotate or disable access keys associated with the principal and revoke active sessions.
- Review CloudTrail activity for evidence of follow-on abuse, particularly EC2 instance launches, network changes, or IAM modifications.
- Apply tighter IAM permissions to restrict access to Service Quotas APIs where not explicitly required.
- Enforce MFA on IAM users and consider conditional access controls (such as source IP or VPC restrictions) for sensitive roles.
- Notify security operations and cloud platform teams to assess potential impact and determine whether containment actions (such as SCP enforcement or account isolation) are required.
- Update detection coverage to monitor for EC2 provisioning attempts following quota discovery to catch resource abuse early.

### Additional information
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **[AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/)**

