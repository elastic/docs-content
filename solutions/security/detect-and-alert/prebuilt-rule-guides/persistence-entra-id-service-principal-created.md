---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Entra ID Service Principal Created" prebuilt detection rule.
---

# Entra ID Service Principal Created

## Triage and analysis

### Investigating Entra ID Service Principal Created

Service Principals are identities used by applications, services, and automation tools to access specific resources. They grant specific access based on the assigned API permissions. Most organizations that work a lot with Azure AD make use of service principals. Whenever an application is registered, it automatically creates an application object and a service principal in an Azure AD tenant.

This rule looks for the addition of service principals. This behavior may enable attackers to impersonate legitimate service principals to camouflage their activities among noisy automations/apps.

#### Possible investigation steps

- Identify the user account that performed the action and whether it should perform this kind of action.
- Investigate other alerts associated with the user account during the past 48 hours.
- Consider the source IP address and geolocation for the user who issued the command. Do they look normal for the user?
- Consider the time of day. If the user is a human, not a program or script, did the activity take place during a normal time of day?
- Check if this operation was approved and performed according to the organization's change management policy.
- Contact the account owner and confirm whether they are aware of this activity.
- Examine the account's commands, API calls, and data management actions in the last 24 hours.
- If you suspect the account has been compromised, scope potentially compromised assets by tracking servers, services, and data accessed by the account in the last 24 hours.

### False positive analysis

If this rule is noisy in your environment due to expected activity, consider adding exceptions — preferably with a combination of user and device conditions.

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

