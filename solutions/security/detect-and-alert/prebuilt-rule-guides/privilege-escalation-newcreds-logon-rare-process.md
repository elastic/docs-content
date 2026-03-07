---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "First Time Seen NewCredentials Logon Process" prebuilt detection rule.
---

# First Time Seen NewCredentials Logon Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating First Time Seen NewCredentials Logon Process

The NewCredentials logon type in Windows allows processes to impersonate a user without requiring a new logon session, often used for legitimate tasks like network resource access. However, adversaries can exploit this by forging access tokens to escalate privileges and bypass controls. The detection rule identifies unusual processes performing this logon type, excluding known system paths and service accounts, to flag potential misuse indicative of token manipulation attacks.

### Possible investigation steps

- Review the process executable path to determine if it is a known or expected application, especially since the query excludes common system paths like Program Files.
- Investigate the SubjectUserName to identify the user account associated with the logon event and determine if it is a legitimate user or a potential compromised account.
- Check the historical activity of the identified process and user account to see if this behavior is consistent with past actions or if it is anomalous.
- Correlate the event with other security logs to identify any preceding or subsequent suspicious activities, such as failed logon attempts or unusual network connections.
- Assess the environment for any recent changes or incidents that might explain the unusual logon process, such as software updates or new application deployments.
- Consult threat intelligence sources to determine if the process or behavior is associated with known malicious activity or threat actors.

### False positive analysis

- Legitimate administrative tools or scripts may trigger this rule if they use the NewCredentials logon type for network resource access. To manage this, identify and whitelist these tools by their process executable paths.
- Scheduled tasks or automated processes running under service accounts might be flagged. Review these tasks and exclude them by adding exceptions for known service account names.
- Software updates or installations that require elevated privileges could cause false positives. Monitor these activities and create exceptions for the specific processes involved in regular update cycles.
- Custom in-house applications that use impersonation for legitimate purposes may be detected. Work with development teams to document these applications and exclude their process paths from the rule.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious processes identified as using the NewCredentials logon type that are not part of known system paths or service accounts.
- Revoke any potentially compromised access tokens and reset credentials for affected user accounts to prevent further misuse.
- Conduct a thorough review of recent logon events and process executions on the affected system to identify any additional unauthorized activities or compromised accounts.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring for similar suspicious logon activities across the network to detect and respond to potential future attempts promptly.
- Review and update access control policies and token management practices to mitigate the risk of access token manipulation in the future.
