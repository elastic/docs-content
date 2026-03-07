---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "M365 or Entra ID Identity Sign-in from a Suspicious Source" prebuilt detection rule.'
---

# M365 or Entra ID Identity Sign-in from a Suspicious Source

## Triage and analysis

### Investigating M365 or Entra ID Identity Sign-in from a Suspicious Source

#### Possible investigation steps

- Investiguate all the alerts associated with the source.ip.
  - Verify the network security alert details associated with this source.ip.
  - Verify all sign-in events associated with this source.ip.
  - Consider the source IP address and geolocation for the involved user account.
  - Consider the device used to sign in. Is it registered and compliant?
- Investigate other alerts associated with the user account during the past 48 hours.
- Contact the account owner and confirm whether they are aware of this activity.
- Check if this operation was approved and performed according to the organization's change management policy.
- If you suspect the account has been compromised, scope potentially compromised assets by tracking servers, services, and data accessed by the account in the last 24 hours.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Disable or limit the account during the investigation and response.
- Identify the possible impact of the incident and prioritize accordingly; the following actions can help you gain context:
    - Identify the account role in the cloud environment.
    - Assess the criticality of affected services and servers.
    - Work with your IT team to identify and minimize the impact on users.
    - Identify if the attacker is moving laterally and compromising other accounts, servers, or services.
    - Identify any regulatory or legal ramifications related to this activity.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords or delete API keys as needed to revoke the attacker's access to the environment. Work with your IT teams to minimize the impact on business operations during these actions.
- Check if unauthorized new users were created, remove unauthorized new accounts, and request password resets for other IAM users.
- Consider enabling multi-factor authentication for users.
- Follow security best practices [outlined](https://docs.microsoft.com/en-us/azure/security/fundamentals/identity-management-best-practices) by Microsoft.
- Determine the initial vector abused by the attacker and take action to prevent reinfection via the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

## Setup

The Azure Fleet integration, Office 365 Logs Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
