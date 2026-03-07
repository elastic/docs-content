---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "AWS STS GetCallerIdentity API Called for the First Time" prebuilt detection rule.'
---

# AWS STS GetCallerIdentity API Called for the First Time

## Triage and analysis

### Investigating AWS STS GetCallerIdentity API Called for the First Time

AWS Security Token Service (AWS STS) is a service that enables you to request temporary, limited-privilege credentials for users.
The `GetCallerIdentity` API returns details about the IAM user or role owning the credentials used to perform the operation.
No permissions are required to run this operation and the same information is returned even when access is denied.
This rule looks for use of the `GetCallerIdentity` API, excluding the `AssumedRole` identity type as use of `GetCallerIdentity` after assuming a role is common practice. This is a [New Terms](https://www.elastic.co/guide/en/security/current/rules-ui-create.html#create-new-terms-rule) rule indicating the first time a specific user identity has performed this operation.

#### Possible investigation steps

- Identify the account and its role in the environment.
- Identify the applications or users that should use this account.
- Investigate other alerts associated with the account during the past 48 hours.
- Investigate abnormal values in the `user_agent.original` field by comparing them with the intended and authorized usage and historical data. Suspicious user agent values include non-SDK, AWS CLI, custom user agents, etc.
- Assess whether this behavior is prevalent in the environment by looking for similar occurrences involving other users.
- Contact the account owner and confirm whether they are aware of this activity.
- Considering the source IP address and geolocation of the user who issued the command:
    - Do they look normal for the calling user?
    - If the source is an EC2 IP address, is it associated with an EC2 instance in one of your accounts or is the source IP from an EC2 instance that's not under your control?
- Review IAM permission policies for the user identity.
- If you suspect the account has been compromised, scope potentially compromised assets by tracking servers, services, and data accessed by the account in the last 24 hours.

### False positive analysis

- False positives may occur due to the intended usage of the service. Tuning is needed in order to have higher confidence. Consider adding exceptions — preferably with a combination of user agent and IP address conditions.
- Automation workflows that rely on the results from this API request may also generate false-positives. We recommend adding exceptions related to the `user.id` or `aws.cloudtrail.user_identity.arn` values to ignore these.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Disable or limit the account during the investigation and response.
- Identify the possible impact of the incident and prioritize accordingly; the following actions can help you gain context:
    - Identify the account role in the cloud environment.
    - Assess the criticality of affected services and servers.
    - Work with your IT team to identify and minimize the impact on users.
    - Identify if the attacker is moving laterally and compromising other accounts, servers, or services.
    - Identify any regulatory or legal ramifications related to this activity.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Rotate secrets or delete API keys as needed to revoke the attacker's access to the environment. Work with your IT teams to minimize the impact on business operations during these actions.
- Check if unauthorized new users were created, remove unauthorized new accounts, and request password resets for other IAM users.
- Consider enabling multi-factor authentication for users.
- Review the permissions assigned to the implicated user to ensure that the least privilege principle is being followed.
- Implement security best practices [outlined](https://aws.amazon.com/premiumsupport/knowledge-center/security-best-practices/) by AWS.
- Take the actions needed to return affected systems, data, or services to their normal operational levels.
- Identify the initial vector abused by the attacker and take action to prevent reinfection via the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
