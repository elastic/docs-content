---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS STS GetSessionToken Usage" prebuilt detection rule.
---

# AWS STS GetSessionToken Usage

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating AWS STS GetSessionToken Usage

AWS Security Token Service (STS) provides temporary credentials for AWS resources, crucial for managing access without long-term credentials. Adversaries may exploit `GetSessionToken` to create temporary credentials, enabling lateral movement and privilege escalation. The detection rule identifies successful `GetSessionToken` requests, flagging potential misuse for further investigation.

#### Possible investigation steps
- **Establish normal baseline behavior**
  - Use this rule’s data to determine which IAM users or automation scripts routinely perform `GetSessionToken`.
  - Monitor frequency, regions, and user agents (CLI, SDK, console) for each identity over time.

- **Identify anomalies**
  - Look for first-time or rare `GetSessionToken` usage by an IAM user.
  - Detect tokens issued without MFA when MFA is normally required.
  - Identify new or unexpected source IPs, geographies, or user agents (e.g., API calls from unfamiliar networks).
  - Check for multiple temporary tokens minted in rapid succession by the same user or access key.

- **Correlate with downstream activity**
  - Search for immediate follow-on events within 15 minutes of token creation:
    - `AssumeRole` into higher-privileged roles or cross-account roles.
    - Privileged API calls (e.g., `iam:*`, `s3:PutBucketPolicy`, `ec2:CreateSnapshot`).
    - New region access, resource enumeration, or credential operations (`GetCallerIdentity`, `ListUsers`, etc.).
  - Use this correlation to elevate contextual `GetSessionToken` behavior into actionable detections.

### Usage Notes
- This rule’s telemetry can support hunting queries such as:
  - `GetSessionToken` without `TokenCode` (no MFA)
  - New IP + `GetSessionToken` + `AssumeRole`
  - Rapid token issuance followed by API activity from a new ASN

Use these patterns in combination with related BBRs or detection rules for `AssumeRole` abuse, cross-account access,
or credential pivoting for more reliable threat detection.

