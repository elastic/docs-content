---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Remote Computer Account DnsHostName Update" prebuilt detection rule.'
---

# Remote Computer Account DnsHostName Update

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Remote Computer Account DnsHostName Update

In Active Directory environments, the DnsHostName attribute links computer accounts to their DNS names, crucial for network communication. Adversaries may exploit this by altering a non-domain controller's DnsHostName to mimic a domain controller, potentially exploiting vulnerabilities like CVE-2022-26923 for privilege escalation. The detection rule identifies suspicious changes by monitoring for remote updates to this attribute, especially when the new hostname resembles a domain controller's, flagging potential exploitation attempts.

### Possible investigation steps

- Review the event logs to confirm the occurrence of the "changed-computer-account" action, focusing on the user.id fields ("S-1-5-21-*", "S-1-12-1-*") to identify the user who initiated the change.
- Verify the new DnsHostName value against the list of legitimate domain controller DNS hostnames to assess if it matches any known domain controllers.
- Check the winlog.event_data.TargetUserName to ensure that the DnsHostName does not start with the computer name that was changed, which could indicate a false positive.
- Investigate the account associated with the user.id to determine if it has a history of suspicious activity or if it has been compromised.
- Examine recent changes or activities on the affected computer account to identify any unauthorized access or configuration changes.
- Correlate this event with other security alerts or logs to identify potential patterns or coordinated activities that might indicate a broader attack.

### False positive analysis

- Routine maintenance or updates to computer accounts may trigger the rule if the DnsHostName is temporarily set to a domain controller-like name. To manage this, create exceptions for known maintenance periods or specific administrative accounts performing these updates.
- Automated scripts or tools that update computer account attributes might inadvertently match the rule's conditions. Identify and exclude these scripts or tools by their user IDs or specific patterns in their operations.
- Legitimate changes in network architecture, such as the promotion of a server to a domain controller, could be flagged. Ensure that such changes are documented and create exceptions for the involved accounts or systems during the transition period.
- Temporary testing environments where non-domain controllers are configured with domain controller-like hostnames for testing purposes can cause false positives. Exclude these environments by their specific hostnames or network segments.
- Regularly review and update the list of known domain controller hostnames to ensure that legitimate changes in the network are not mistakenly flagged as suspicious.

### Response and remediation

- Immediately isolate the affected computer from the network to prevent further unauthorized changes or potential exploitation.
- Verify the legitimacy of the DnsHostName change by cross-referencing with known domain controller hostnames and authorized change requests.
- Revert any unauthorized changes to the DnsHostName attribute to its original state to restore proper network communication and prevent misuse.
- Conduct a thorough review of recent account activities and permissions for the user account involved in the change to identify any unauthorized access or privilege escalation attempts.
- Escalate the incident to the security operations team for further investigation and to assess potential exploitation of CVE-2022-26923 or other vulnerabilities.
- Implement additional monitoring on the affected system and similar systems to detect any further suspicious activities or attempts to exploit vulnerabilities.
- Review and update access controls and permissions for computer accounts in Active Directory to ensure only authorized personnel can make changes to critical attributes like DnsHostName.
