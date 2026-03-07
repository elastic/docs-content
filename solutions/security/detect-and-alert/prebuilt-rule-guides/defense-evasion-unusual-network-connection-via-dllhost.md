---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Network Connection via DllHost" prebuilt detection rule.
---

# Unusual Network Connection via DllHost

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Network Connection via DllHost

Dllhost.exe is a legitimate Windows process used to host DLL services. Adversaries may exploit it for stealthy command and control by initiating unauthorized network connections. The detection rule identifies suspicious dllhost.exe activity by monitoring outbound connections to non-local IPs, which may indicate malicious intent. This approach helps in identifying potential threats by focusing on unusual network behaviors associated with this process.

### Possible investigation steps

- Review the process start event for dllhost.exe to confirm its legitimacy by checking the process arguments and the parent process that initiated it.
- Analyze the destination IP addresses involved in the network connections to determine if they are known malicious or suspicious entities, using threat intelligence sources.
- Check the timeline of events to see if there are any other unusual activities on the host around the time of the dllhost.exe network connection, such as other process executions or file modifications.
- Investigate the user account associated with the dllhost.exe process to determine if there are any signs of compromise or unauthorized access.
- Examine the network traffic patterns from the host to identify any other unusual outbound connections that might indicate broader malicious activity.

### False positive analysis

- Legitimate software updates or system maintenance tasks may cause dllhost.exe to make outbound connections. Users can monitor and whitelist known update servers to prevent these from being flagged.
- Certain enterprise applications might use dllhost.exe for legitimate network communications. Identify and document these applications, then create exceptions for their known IP addresses.
- Automated scripts or administrative tools that leverage dllhost.exe for network tasks can trigger false positives. Review and exclude these scripts or tools by specifying their associated IP ranges.
- Cloud-based services or virtual environments might route traffic through dllhost.exe. Verify these services and exclude their IP addresses from the detection rule to avoid unnecessary alerts.

### Response and remediation

- Isolate the affected host from the network immediately to prevent further unauthorized communications and potential lateral movement.
- Terminate the suspicious dllhost.exe process to stop any ongoing malicious activity and prevent further outbound connections.
- Conduct a thorough scan of the affected system using updated antivirus and anti-malware tools to identify and remove any additional malicious software or artifacts.
- Review and analyze the network logs to identify any other systems that may have been targeted or compromised, and apply similar containment measures if necessary.
- Restore the affected system from a known good backup to ensure that any potential backdoors or persistent threats are removed.
- Implement network segmentation to limit the ability of similar threats to spread across the network in the future.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional organizational measures are required.
