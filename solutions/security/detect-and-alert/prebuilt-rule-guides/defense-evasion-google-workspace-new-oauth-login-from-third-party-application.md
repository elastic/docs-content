---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "First Time Seen Google Workspace OAuth Login from Third-Party Application" prebuilt detection rule.
---

# First Time Seen Google Workspace OAuth Login from Third-Party Application

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating First Time Seen Google Workspace OAuth Login from Third-Party Application

OAuth is a protocol that allows third-party applications to access user data without exposing credentials, enhancing security in Google Workspace. However, adversaries can exploit OAuth by using compromised credentials to gain unauthorized access, mimicking legitimate users. The detection rule identifies unusual OAuth logins by monitoring authorization events linked to new third-party applications, flagging potential misuse for further investigation.

### Possible investigation steps

- Review the event details to identify the specific third-party application involved by examining the google_workspace.token.client.id field.
- Check the google_workspace.token.scope.data field to understand the scope of permissions granted to the third-party application and assess if they align with expected usage.
- Investigate the user account associated with the OAuth authorization event to determine if there are any signs of compromise or unusual activity.
- Correlate the timestamp of the OAuth login event with other security logs to identify any concurrent suspicious activities or anomalies.
- Verify if the third-party application is known and authorized within the organization by consulting with relevant stakeholders or reviewing application whitelists.
- Assess the risk and impact of the OAuth login by considering the privileges of the user account and the sensitivity of the accessed resources.

### False positive analysis

- New legitimate third-party applications: Users may frequently integrate new third-party applications for productivity or collaboration. To manage this, maintain a whitelist of known and trusted applications and exclude them from triggering alerts.
- Regular updates to existing applications: Some applications may update their OAuth client IDs during version upgrades. Monitor application update logs and adjust the detection rule to exclude these known updates.
- Internal development and testing: Organizations developing their own applications may trigger this rule during testing phases. Coordinate with development teams to identify and exclude these internal applications from alerts.
- Frequent use of service accounts: Service accounts used for automation or integration purposes might appear as new logins. Document and exclude these service accounts from the detection rule to prevent false positives.

### Response and remediation

- Immediately revoke the OAuth token associated with the suspicious third-party application to prevent further unauthorized access.
- Conduct a thorough review of the affected user's account activity to identify any unauthorized actions or data access that may have occurred.
- Reset the credentials of the affected user and any other users who may have been compromised, ensuring that strong, unique passwords are used.
- Notify the affected user and relevant stakeholders about the incident, providing guidance on recognizing phishing attempts and securing their accounts.
- Implement additional monitoring for the affected user and similar OAuth authorization events to detect any further suspicious activity.
- Escalate the incident to the security operations team for a deeper investigation into potential lateral movement or data exfiltration.
- Review and update OAuth application permissions and policies to ensure that only trusted applications have access to sensitive data and services.

## Setup

The Google Workspace Fleet integration, Filebeat module, or similarly structured data is required to be compatible with this rule.
### Important Information Regarding Google Workspace Event Lag Times
- As per Google's documentation, Google Workspace administrators may observe lag times ranging from minutes up to 3 days between the time of an event's occurrence and the event being visible in the Google Workspace admin/audit logs.
- This rule is configured to run every 10 minutes with a lookback time of 130 minutes.
- To reduce the risk of false negatives, consider reducing the interval that the Google Workspace (formerly G Suite) Filebeat module polls Google's reporting API for new events.
- By default, `var.interval` is set to 2 hours (2h). Consider changing this interval to a lower value, such as 10 minutes (10m).
- See the following references for further information:
  - https://support.google.com/a/answer/7061566
  - https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-module-google_workspace.html
