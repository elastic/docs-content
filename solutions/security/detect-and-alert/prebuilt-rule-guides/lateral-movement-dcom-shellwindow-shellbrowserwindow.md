---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Incoming DCOM Lateral Movement with ShellBrowserWindow or ShellWindows" prebuilt detection rule.'
---

# Incoming DCOM Lateral Movement with ShellBrowserWindow or ShellWindows

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Incoming DCOM Lateral Movement with ShellBrowserWindow or ShellWindows

DCOM enables software components to communicate over a network, often used in Windows environments for legitimate inter-process communication. Adversaries exploit DCOM, particularly ShellBrowserWindow or ShellWindows, to execute commands remotely, facilitating stealthy lateral movement. The detection rule identifies suspicious network activity and process creation patterns, such as incoming TCP connections to high ports and explorer.exe spawning processes, which may indicate DCOM abuse.

### Possible investigation steps

- Review the network activity to identify the source IP address of the incoming TCP connection. Verify if the source IP is known or expected within the network environment.
- Examine the process tree for explorer.exe to identify any unusual or unexpected child processes that were spawned. Investigate these processes for any signs of malicious activity.
- Check the destination port and source port numbers to determine if they are commonly used for legitimate services or if they are unusual for the environment.
- Correlate the event with other security logs or alerts to identify any additional suspicious activities or patterns associated with the same source IP or process entity.
- Investigate the user account associated with the explorer.exe process to determine if there are any signs of compromise or unauthorized access.
- Review historical data for any previous occurrences of similar network connections or process creations to identify potential patterns or repeated attempts.

### False positive analysis

- Legitimate software updates or installations may trigger the rule due to the use of DCOM for remote management tasks. Users can create exceptions for known update processes by identifying their specific network and process patterns.
- Internal IT management tools that utilize DCOM for remote administration might cause false positives. Review and whitelist these tools by confirming their source IP addresses and process behaviors.
- Automated scripts or scheduled tasks that leverage DCOM for legitimate purposes can be mistaken for lateral movement. Document and exclude these tasks by correlating their execution times and process chains.
- Network scanning or monitoring tools that generate high-port TCP connections could be misinterpreted as suspicious activity. Validate and exclude these tools by cross-referencing their network traffic with known benign sources.
- User-initiated remote desktop sessions or file transfers using DCOM may appear as lateral movement. Verify and exclude these activities by checking user authentication logs and session details.

### Response and remediation

- Isolate the affected host immediately from the network to prevent further lateral movement and potential data exfiltration.
- Terminate any suspicious processes spawned by explorer.exe that are not part of normal operations, focusing on those initiated through high TCP ports.
- Conduct a thorough review of recent network connections and process creation logs on the affected host to identify any additional compromised systems or lateral movement attempts.
- Reset credentials for any accounts that were active on the affected host during the time of the alert to prevent unauthorized access.
- Apply patches and updates to the affected systems to address any vulnerabilities that may have been exploited during the attack.
- Enhance monitoring and logging on the network to detect similar DCOM abuse attempts, ensuring that alerts are configured for high TCP port activity and unusual process spawning by explorer.exe.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional containment or remediation actions are necessary.
