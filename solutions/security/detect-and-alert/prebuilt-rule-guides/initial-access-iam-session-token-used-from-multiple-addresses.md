---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS Access Token Used from Multiple Addresses" prebuilt detection rule.
---

# AWS Access Token Used from Multiple Addresses

## Triage and Analysis

### Investigating AWS Access Token Used from Multiple Addresses

Access tokens are bound to a single user. Usage from multiple IP addresses may indicate the token was stolen and used elsewhere. By correlating this with additional detection criteria like multiple user agents, different cities, and different networks, we can improve the fidelity of the rule and help to eliminate false positives associated with expected behavior, like dual-stack IPV4/IPV6 usage.

#### Possible investigation steps

- **Identify the IAM User**: Examine the `aws.cloudtrail.user_identity.arn` stored in `user_id` and correlate with the `source.ips` stored in `ip_list` and `unique_ips` count to determine how widely the token was used.
- **Correlate Additional Detection Context**: Examine `activity_type` and `fidelity_score` to determine additional cities, networks or user agents associated with the token usage.
- **Determine Access Key Type**: Examine the `access_key_id` to determine whether the token is short-term (beginning with ASIA) or long-term (beginning with AKIA).
- **Check Recent MFA Events**: Determine whether the user recently enabled MFA, registered devices, or assumed a role using this token.
- **Review Workload Context**: Confirm whether the user was expected to be active across multiple cities, networks or user agent environments.
- **Trace Adversary Movement**: Pivot to related actions (e.g., `s3:ListBuckets`, `iam:ListUsers`, `sts:GetCallerIdentity`) to track further enumeration.

### False positive analysis

- Automation frameworks that rotate through multiple IPs or cloud functions with dynamic egress IPs may cause this alert to fire.
- Confirm geolocation and workload context before escalating.

### Response and remediation

- **Revoke the Token**: Disable or rotate the IAM credentials and invalidate the temporary session token.
- **Audit the Environment**: Look for signs of lateral movement or data access during the token's validity.
- **Strengthen Controls**: Require MFA for high-privilege actions, restrict access via policy conditions (e.g., IP range or device).

### Additional information

- [IAM Long-Term Credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)
- [STS Temporary Credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html)
- [Using MFA with Temporary Credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_enable-regions.html)
- [AWS Threat Detection Use Cases](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-fsbp-controls.html)

