---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "WMI Incoming Lateral Movement" prebuilt detection rule.
---

# WMI Incoming Lateral Movement

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating WMI Incoming Lateral Movement

Windows Management Instrumentation (WMI) is a core Windows feature enabling remote management and data collection. Adversaries exploit WMI for lateral movement by executing processes on remote hosts, often bypassing traditional security measures. The detection rule identifies suspicious WMI activity by monitoring specific network connections and process executions, filtering out common false positives to highlight potential threats.

### Possible investigation steps

- Review the source IP address of the incoming RPC connection to determine if it is from a known or trusted network segment, excluding localhost addresses like 127.0.0.1 and ::1.
- Check the process name and parent process name, specifically looking for svchost.exe and WmiPrvSE.exe, to confirm the execution context and identify any unusual parent-child process relationships.
- Investigate the user ID associated with the process execution to ensure it is not a system account (S-1-5-18, S-1-5-19, S-1-5-20) and assess if the user has legitimate reasons for remote WMI activity.
- Examine the process executable path to verify it is not one of the excluded common false positives, such as those related to HPWBEM, SCCM, or other specified system utilities.
- Analyze the network connection details, including source and destination ports, to identify any patterns or anomalies that could indicate malicious lateral movement.
- Correlate the alert with other security events or logs from the same host or network segment to gather additional context and identify potential patterns of compromise.

### False positive analysis

- Administrative use of WMI for remote management can trigger alerts. To manage this, create exceptions for known administrative accounts or specific IP addresses used by IT staff.
- Security tools like Nessus and SCCM may cause false positives. Exclude processes associated with these tools by adding their executables to the exception list.
- System processes running with high integrity levels might be flagged. Exclude processes with integrity levels marked as "System" to reduce noise.
- Specific executables such as msiexec.exe and appcmd.exe with certain arguments can be safely excluded if they are part of routine administrative tasks.
- Regularly review and update the exception list to ensure it aligns with current network management practices and tools.

### Response and remediation

- Isolate the affected host immediately from the network to prevent further lateral movement by the adversary. This can be done by disabling network interfaces or using network segmentation tools.
- Terminate any suspicious processes identified as being executed via WMI on the affected host. Use task management tools or scripts to stop these processes.
- Conduct a thorough review of the affected host's WMI logs and process execution history to identify any unauthorized changes or additional malicious activity.
- Reset credentials for any accounts that were used in the suspicious WMI activity, especially if they have administrative privileges, to prevent further unauthorized access.
- Apply patches and updates to the affected host and any other systems that may be vulnerable to similar exploitation methods, ensuring that all security updates are current.
- Enhance monitoring and logging for WMI activity across the network to detect and respond to similar threats more quickly in the future. This includes setting up alerts for unusual WMI usage patterns.
- If the threat is confirmed to be part of a larger attack, escalate the incident to the appropriate security team or authority for further investigation and potential legal action.
