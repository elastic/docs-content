---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS IAM Roles Anywhere Profile Creation" prebuilt detection rule.'
---

# AWS IAM Roles Anywhere Profile Creation

## Triage and analysis

### Investigating AWS IAM Roles Anywhere Profile Creation

AWS IAM Roles Anywhere allows external workloads — such as CI/CD runners, on-premises systems, or third-party services — 
to assume IAM roles securely by presenting a certificate from a trusted anchor. A profile defines the IAM roles that 
can be assumed, the trust anchor they are associated with, and session duration limits.

This rule detects when a new Roles Anywhere profile is created using the `CreateProfile` API call. Unauthorized profile 
creation can enable persistent external access if tied to over-privileged roles or to trust anchors associated with 
unauthorized certificate authorities (CAs). Monitoring profile creation is crucial to ensuring that only approved roles 
and anchors are in use.

#### Possible investigation steps

- **Identify the actor**
  - Review `aws.cloudtrail.user_identity.arn` and `aws.cloudtrail.user_identity.access_key_id` to determine 
    which IAM user, role, or principal created the profile.
  - Check whether this identity normally manages Roles Anywhere configurations.

- **Review profile configuration**
  - Inspect `aws.cloudtrail.request_parameters` for key values such as:
    - `profileName`
    - `roleArns` – confirm that the listed IAM roles are expected and not overly permissive.
    - `trustAnchorArn` – verify the trust anchor is valid and authorized.
    - `durationSeconds` – check for unusually long session durations.
  - Determine if multiple roles were attached, which may indicate excessive privilege aggregation.

- **Correlate related activity**
  - Check for prior or concurrent events by the same actor, including:
    - `CreateTrustAnchor` with external or unauthorized certificate authorities.
    - `CreateRole`, `PutRolePolicy`, or `AttachRolePolicy` for privilege escalation paths.
  - Review whether subsequent `AssumeRoleWithCertificate` events occurred, indicating use of the new profile.

- **Assess the source context**
  - Investigate `source.ip`, `user_agent.original`, and `source.geo` fields to identify if this request originated from an unfamiliar host, region, or automation client (e.g., `boto3`, `curl`, custom SDKs).
  - Compare to baseline patterns of legitimate IAM or infrastructure automation.

- **Validate legitimacy**
  - Contact the responsible team (e.g., platform, PKI, or IAM administration) to confirm whether this profile creation 
    aligns with approved change management or onboarding activities.


### False positive analysis:

- **Legitimate administrative actions**
  - IAM or PKI engineers may legitimately create profiles during setup of new external integrations or workloads. 
    Validate against change control records and deployment logs.
- **Authorized automation**
  - Infrastructure-as-code (IaC) pipelines (Terraform, CloudFormation, etc.) may automatically create profiles. 
    Confirm these operations are sourced from known automation accounts or IP ranges.
- **Development and testing**
  - Lab or sandbox accounts may test Roles Anywhere configurations with less restrictive controls. 
    Ensure alerts from non-production accounts are tuned accordingly.

### Response and remediation:

- **Immediate review and containment**
  - If unauthorized, disable or delete the created profile (`aws rolesanywhere delete-profile`) and review all 
    associated IAM roles for misuse.
  - Rotate any credentials or revoke certificates issued from unapproved trust anchors.

- **Investigation**
  - Search CloudTrail for additional related actions by the same identity, such as 
    `CreateTrustAnchor`, `AssumeRoleWithCertificate`, or cross-account access attempts.
  - Verify whether any sessions have been initiated using the new profile and identify 
    which roles were assumed.

- **Recovery and hardening**
  - Restrict `rolesanywhere:CreateProfile` to a small set of administrative roles.
  - Implement AWS Config or Security Hub controls to alert on unauthorized or overly 
    permissive Roles Anywhere profiles.
  - Audit IAM role trust policies linked to external anchors and ensure adherence to the 
    principle of least privilege.
  - Review and document all approved Roles Anywhere profiles and their corresponding trust anchors.

### Additional information

- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **Security Best Practices:** [AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/).
