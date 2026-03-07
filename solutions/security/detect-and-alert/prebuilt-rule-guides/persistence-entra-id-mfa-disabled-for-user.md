---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Entra ID MFA Disabled for User" prebuilt detection rule.
---

# Entra ID MFA Disabled for User

## Triage and analysis

### Investigating Entra ID MFA Disabled for User

Multi-factor authentication is a process in which users are prompted during the sign-in process for an additional form of identification, such as a code on their cellphone or a fingerprint scan.

If you only use a password to authenticate a user, it leaves an insecure vector for attack. If the password is weak or has been exposed elsewhere, an attacker could be using it to gain access. When you require a second form of authentication, security is increased because this additional factor isn't something that's easy for an attacker to obtain or duplicate.

For more information about using MFA in Microsoft Entra ID, access the [official documentation](https://docs.microsoft.com/en-us/azure/active-directory/authentication/concept-mfa-howitworks#how-to-enable-and-use-azure-ad-multi-factor-authentication).

This rule identifies the deactivation of MFA for an Entra ID user account. This modification weakens account security and can lead to the compromise of accounts and other assets.

#### Possible investigation steps

- Identify the user account that performed the action and whether it should perform this kind of action.
- Investigate other alerts associated with the user account during the past 48 hours.
- Contact the account and resource owners and confirm whether they are aware of this activity.
- Correlate with Entra ID Sign-In Logs to identify anomalous sign-in attempts following MFA disablement.
- This rule does not identify if the user was removed from a conditional access policy (CAP) with MFA requirements.
    - Instead the rule identifies both legacy and modern MFA disablement through user settings.
- Check if this operation was approved and performed according to the organization's change management policy.
- If you suspect the account has been compromised, scope potentially compromised assets by tracking servers, services, and data accessed by the account in the last 24 hours.

### False positive analysis

- While this activity can be done by administrators, all users must use MFA. The security team should address any potential benign true positive (B-TP), as this configuration can risk the user and domain.

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
- Reactivate multi-factor authentication for the user.
- Review the permissions assigned to the implicated user to ensure that the least privilege principle is being followed.
- Implement security defaults [provided by Microsoft](https://docs.microsoft.com/en-us/azure/active-directory/fundamentals/concept-fundamentals-security-defaults).
- Determine the initial vector abused by the attacker and take action to prevent reinfection via the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

