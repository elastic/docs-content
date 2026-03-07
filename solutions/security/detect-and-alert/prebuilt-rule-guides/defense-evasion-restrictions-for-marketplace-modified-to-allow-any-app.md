---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Google Workspace Restrictions for Marketplace Modified to Allow Any App" prebuilt detection rule.'
---

# Google Workspace Restrictions for Marketplace Modified to Allow Any App

## Triage and analysis

### Investigating Google Workspace Restrictions for Marketplace Modified to Allow Any App

Google Workspace Marketplace is an online store for free and paid web applications that work with Google Workspace services and third-party software. Listed applications are based on Google APIs or Google Apps Script and created by both Google and third-party developers.

Marketplace applications require access to specific Google Workspace resources. Applications can be installed by individual users, if they have permission, or can be installed for an entire Google Workspace domain by administrators. Consent screens typically display what permissions and privileges the application requires during installation. As a result, malicious Marketplace applications may require more permissions than necessary or have malicious intent.

Google clearly states that they are not responsible for any product on the Marketplace that originates from a source other than Google.

This rule identifies when the global allow-all setting is enabled for Google Workspace Marketplace applications.

#### Possible investigation steps

- Identify the associated user accounts by reviewing `user.name` or `user.email` fields in the alert.
- This rule relies on data from `google_workspace.admin`, thus indicating the associated user has administrative privileges to the Marketplace.
- Search for `event.action` is `ADD_APPLICATION` to identify applications installed after these changes were made.
    - The `google_workspace.admin.application.name` field will help identify what applications were added.
- With the user account, review other potentially related events within the last 48 hours.
- Re-assess the permissions and reviews of the Marketplace applications to determine if they violate organizational policies or introduce unexpected risks.
- With access to the Google Workspace admin console, determine if the application was installed domain-wide or individually by visiting `Apps > Google Workspace Marketplace Apps`.

### False positive analysis

- Identify the user account associated with this action and assess their administrative privileges with Google Workspace Marketplace.
- Google Workspace administrators may intentionally add an application from the marketplace based on organizational needs.
    - Follow up with the user who added the application to ensure this was intended.
- Verify the application identified has been assessed thoroughly by an administrator.

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
- Review the permissions assigned to the implicated user to ensure that the least privilege principle is being followed.
- Implement security best practices [outlined](https://support.google.com/a/answer/7587183) by Google.
- Determine the initial vector abused by the attacker and take action to prevent reinfection via the same vector.
- Using the incident response data, update logging and audit policies to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).

## Setup

The Google Workspace Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.

### Important Information Regarding Google Workspace Event Lag Times
- As per Google's documentation, Google Workspace administrators may observe lag times ranging from minutes up to 3 days between the time of an event's occurrence and the event being visible in the Google Workspace admin/audit logs.
- To reduce the risk of false negatives, consider reducing the interval that the Google Workspace (formerly G Suite) Filebeat module polls Google's reporting API for new events.
- By default, `var.interval` is set to 2 hours (2h). Consider changing this interval to a lower value, such as 10 minutes (10m).
- See the following references for further information:
  - https://support.google.com/a/answer/7061566
  - https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-module-google_workspace.html
