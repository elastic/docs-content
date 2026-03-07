---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS CLI with Kali Linux Fingerprint Identified" prebuilt detection rule.
---

# AWS CLI with Kali Linux Fingerprint Identified

## Triage and Analysis

### Investigating AWS CLI with Kali Linux Fingerprint Identified

AWS CloudTrail captures the user agent string for API requests, which can provide insight into the operating system and tooling used. The presence of `distrib#kali` strongly suggests the AWS CLI was executed from a Kali Linux environment. Kali is widely used for penetration testing, red teaming, and adversarial operations, making its appearance in AWS API telemetry noteworthy, especially when associated with sensitive actions or unexpected identities.

This detection focuses on successful AWS CLI activity and should be evaluated in the context of who performed the action, what was accessed or modified, and where the request originated.

### Possible investigation steps

**Identify the actor**
- Review `aws.cloudtrail.user_identity.arn` and `aws.cloudtrail.user_identity.access_key_id` to determine which IAM
  principal was used.
- Check whether this principal normally interacts with AWS via CLI tooling and whether Kali Linux usage is expected.

**Review access patterns and actions**
- Examine the API calls associated with this user agent for high-risk activity such as IAM changes, data access, snapshot
  sharing, logging modification, or persistence-related actions.
- Look for sequences indicating initial access or expansion, such as `GetSessionToken`, `AssumeRole`, or privilege
  escalation attempts.
- Determine whether the activity scope aligns with the role’s intended permissions and business function.

**Inspect source network and tooling context**
- Review `source.ip`, `source.geo` fields, and ASN to determine whether the request originated from an expected corporate
  network, VPN, or known security testing infrastructure.
- Analyze `user_agent.original` to confirm CLI usage and identify automation versus interactive usage.
- Sudden shifts from console-based access to CLI usage from Kali may indicate credential compromise.

**Correlate with surrounding activity**
- Search for additional CloudTrail events tied to the same access key or session before and after this detection.
- Look for evidence of follow-on actions such as resource creation, configuration changes, or attempts to disable logging and monitoring services.
- Assess whether the activity represents a single isolated request or part of a broader behavioral chain.

### False positive analysis

- Internal red team or security testing activity may legitimately generate Kali-based AWS CLI traffic. Confirm scope,
  timing, and authorization with security leadership.
- Compare against historical behavior for the same IAM principal to determine whether Kali usage is a deviation from
  baseline access patterns.

### Response and remediation

- If the activity is unauthorized, immediately revoke or rotate the affected access keys or invalidate the active
  session.
- Review IAM permissions associated with the identity and reduce scope where possible to enforce least privilege.
- Investigate for additional indicators of compromise, including unusual role assumptions, new credential creation, or
  data access from the same identity.
- Notify security operations and incident response teams if the activity aligns with known adversary behaviors or appears
  part of a larger intrusion.
- Consider adding guardrails or conditional access controls (such as source IP restrictions or MFA enforcement) for
  sensitive IAM principals.

### Additional information
- **[AWS IR Playbooks](https://github.com/aws-samples/aws-incident-response-playbooks/blob/c151b0dc091755fffd4d662a8f29e2f6794da52c/playbooks/)** 
- **[AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework/tree/a8c7b313636b406a375952ac00b2d68e89a991f2/docs)** 
- **[AWS Knowledge Center – Security Best Practices](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/)**

