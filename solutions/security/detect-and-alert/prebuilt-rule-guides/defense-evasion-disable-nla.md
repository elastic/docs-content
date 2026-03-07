---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Network-Level Authentication (NLA) Disabled" prebuilt detection rule.
---

# Network-Level Authentication (NLA) Disabled

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Network-Level Authentication (NLA) Disabled

Network-Level Authentication (NLA) enhances security for Remote Desktop Protocol (RDP) by requiring user authentication before establishing a session. Adversaries may disable NLA to exploit vulnerabilities at the Windows sign-in screen, bypassing authentication for persistence tactics. The detection rule identifies registry changes that disable NLA, signaling potential unauthorized access attempts.

### Possible investigation steps

- Review the registry event logs to confirm the modification of the UserAuthentication value in the specified registry paths, ensuring the change was not part of a legitimate administrative action.
- Identify the user account and process responsible for the registry modification by examining the event logs for associated user and process information.
- Check for any recent Remote Desktop Protocol (RDP) connection attempts or sessions on the affected host to determine if unauthorized access was achieved following the NLA disablement.
- Investigate the timeline of the registry change to correlate with any other suspicious activities or alerts on the host, such as the execution of unusual processes or network connections.
- Assess the host for signs of persistence mechanisms, particularly those leveraging Accessibility Features like Sticky Keys, which may have been enabled following the NLA disablement.
- Evaluate the security posture of the affected system, including patch levels and existing security controls, to identify potential vulnerabilities that could have been exploited.

### False positive analysis

- Administrative changes to RDP settings can trigger false positives when IT personnel intentionally modify registry settings for legitimate purposes. To handle this, create exceptions for known administrative activities by documenting and excluding these specific registry changes from alerts.
- Software updates or installations that modify RDP settings might be flagged as false positives. To mitigate this, maintain a list of trusted software and their expected registry changes, and configure the detection system to ignore these during update windows.
- Automated scripts or management tools that adjust RDP configurations for compliance or performance reasons can also cause false positives. Identify these tools and their expected behavior, then set up exclusions for their registry modifications to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Re-enable Network-Level Authentication (NLA) on the affected system by modifying the registry value back to its secure state, ensuring that "UserAuthentication" is set to "1" or "0x00000001".
- Conduct a thorough review of recent user activity and system logs to identify any unauthorized access or changes made during the period NLA was disabled.
- Reset passwords for all accounts that have accessed the affected system to mitigate potential credential compromise.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring on the affected system and similar endpoints to detect any further attempts to disable NLA or other suspicious activities.
- Review and update endpoint security policies to ensure that registry changes related to NLA are monitored and alerts are generated for any unauthorized modifications.
