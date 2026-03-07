---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Google Workspace Object Copied to External Drive with App Consent" prebuilt detection rule.
---

# Google Workspace Object Copied to External Drive with App Consent

## Triage and analysis

### Investigating Google Workspace Object Copied to External Drive with App Consent

Google Workspace users can share access to Drive objects such as documents, sheets, and forms via email delivery or a shared link. Shared link URIs have parameters like `view` or `edit` to indicate the recipient's permissions. The `copy` parameter allows the recipient to copy the object to their own Drive, which grants the object with the same privileges as the recipient. Specific objects in Google Drive allow container-bound scripts that run on Google's Apps Script platform. Container-bound scripts can contain malicious code that executes with the recipient's privileges if in their Drive.

This rule aims to detect when a user copies an external Drive object to their Drive storage and then grants permissions to a custom application via OAuth prompt.

#### Possible investigation steps
- Identify user account(s) associated by reviewing `user.name` or `source.user.email` in the alert.
- Identify the name of the file copied by reviewing `file.name` as well as the `file.id` for triaging.
- Identify the file type by reviewing `google_workspace.drive.file.type`.
- With the information gathered so far, query across data for the file metadata to determine if this activity is isolated or widespread.
- Within the OAuth token event, identify the application name by reviewing `google_workspace.token.app_name`.
    - Review the application ID as well from `google_workspace.token.client.id`.
    - This metadata can be used to report the malicious application to Google for permanent blacklisting.
- Identify the permissions granted to the application by the user by reviewing `google_workspace.token.scope.data.scope_name`.
    - This information will help pivot and triage into what services may have been affected.
- If a container-bound script was attached to the copied object, it will also exist in the user's drive.
    - This object should be removed from all users affected and investigated for a better understanding of the malicious code.

### False positive analysis
- Communicate with the affected user to identify if these actions were intentional
- If a container-bound script exists, review code to identify if it is benign or malicious

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
    - Resetting passwords will revoke OAuth tokens which could have been stolen.
- Reactivate multi-factor authentication for the user.
- Review the permissions assigned to the implicated user to ensure that the least privilege principle is being followed.
- Implement security defaults [provided by Google](https://cloud.google.com/security-command-center/docs/how-to-investigate-threats).
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
