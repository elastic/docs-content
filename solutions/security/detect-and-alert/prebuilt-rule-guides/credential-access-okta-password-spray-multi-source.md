---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Okta Password Spray (Multi-Source)" prebuilt detection rule.
---

# Potential Okta Password Spray (Multi-Source)

## Triage and analysis

### Investigating Potential Okta Password Spray (Multi-Source)

This rule identifies coordinated password spray attacks where multiple source IPs target multiple user accounts within a time window. This pattern indicates attackers using IP rotation to evade single-source detection while spraying passwords across the organization.

#### Possible investigation steps
- Review the list of targeted user accounts and check if any authentications succeeded.
- Examine the source IPs and their ASN ownership for signs of proxy, VPN, or cloud infrastructure.
- Check if Okta flagged any of the sources as known threats or proxies.
- Analyze the attempts-per-user ratio to confirm spray behavior versus brute force.
- Review the geographic distribution of source IPs for coordination patterns.
- Cross-reference with successful authentication events to identify potential compromises.

### False positive analysis
- Organization-wide password rotation or expiration events may cause widespread authentication failures.
- Misconfigured SSO or SAML integrations can cause batch failures from legitimate infrastructure.
- Penetration testing should be coordinated and whitelisted in advance.

### Response and remediation
- If attack is confirmed, notify affected users and enforce password resets for potentially compromised accounts.
- Block attacking IP ranges at the network perimeter.
- Enable or strengthen MFA for targeted accounts.
- Review Okta sign-on policies to add additional friction for suspicious authentication patterns.
- Consider temporary lockdowns for highly targeted accounts.

