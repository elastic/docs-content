---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Entra ID PowerShell Sign-in" prebuilt detection rule.
---

# Entra ID PowerShell Sign-in

## Triage and analysis

### Investigating Entra ID PowerShell Sign-in

Azure Active Directory PowerShell for Graph (Azure AD PowerShell) is a module IT professionals commonly use to manage their Azure Active Directory. The cmdlets in the Azure AD PowerShell module enable you to retrieve data from the directory, create new objects in the directory, update existing objects, remove objects, as well as configure the directory and its features.

This rule identifies sign-ins that use the Azure Active Directory PowerShell module, which can indicate unauthorized access if done outside of IT or engineering.

#### Possible investigation steps

- Identify the user account that performed the action and whether it should perform this kind of action.
- Evaluate whether the user needs to access Azure AD using PowerShell to complete its tasks.
- Investigate other alerts associated with the user account during the past 48 hours.
- Consider the source IP address and geolocation for the involved user account. Do they look normal?
- Contact the account owner and confirm whether they are aware of this activity.
- Investigate suspicious actions taken by the user using the module, for example, modifications in security settings that weakens the security policy, persistence-related tasks, and data access.
- If you suspect the account has been compromised, scope potentially compromised assets by tracking servers, services, and data accessed by the account in the last 24 hours.

### False positive analysis

- If this activity is expected and noisy in your environment, consider adding IT, Engineering, and other authorized users as exceptions — preferably with a combination of user and device conditions.

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

The Azure Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
