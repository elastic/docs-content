---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Incoming DCOM Lateral Movement via MSHTA" prebuilt detection rule.
---

# Incoming DCOM Lateral Movement via MSHTA

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Incoming DCOM Lateral Movement via MSHTA

DCOM allows software components to communicate over a network, enabling remote execution of applications like MSHTA, which runs HTML applications. Adversaries exploit this by executing commands remotely, bypassing traditional security measures. The detection rule identifies suspicious MSHTA activity by monitoring process starts and network traffic, focusing on unusual port usage and remote IP addresses, indicating potential lateral movement attempts.

### Possible investigation steps

- Review the process start event for mshta.exe on the affected host to gather details such as the process entity ID, command-line arguments, and parent process information to understand how mshta.exe was executed.
- Analyze the network traffic associated with the mshta.exe process, focusing on the source and destination IP addresses and ports, to identify any unusual or unauthorized remote connections.
- Check the source IP address involved in the network event to determine if it is known or associated with any previous suspicious activity or if it belongs to an internal or external network.
- Investigate the timeline of events on the host to identify any preceding or subsequent suspicious activities that might indicate a broader attack pattern or lateral movement attempts.
- Correlate the findings with other security logs and alerts from the same host or network segment to identify any additional indicators of compromise or related malicious activities.
- Assess the risk and impact of the detected activity by considering the host's role within the network and any sensitive data or systems it may have access to.

### False positive analysis

- Legitimate administrative tasks using MSHTA for remote management can trigger the rule. Identify and document these tasks, then create exceptions for known administrative IP addresses or specific user accounts.
- Automated software updates or deployments that utilize MSHTA may appear as suspicious activity. Monitor and whitelist the IP addresses and ports associated with these updates to prevent false positives.
- Internal network scanning tools or security assessments might mimic lateral movement behavior. Coordinate with IT and security teams to recognize these activities and exclude them from triggering alerts.
- Custom applications that leverage MSHTA for inter-process communication could be flagged. Review these applications and exclude their known processes or network patterns from the detection rule.
- Remote desktop or support tools that use MSHTA for legitimate purposes should be identified. Whitelist these tools by their process names or associated network traffic to reduce unnecessary alerts.

### Response and remediation

- Isolate the affected host immediately from the network to prevent further lateral movement and potential data exfiltration.
- Terminate the mshta.exe process on the affected host to stop any ongoing malicious activity.
- Conduct a thorough examination of the affected host to identify any additional malicious files or processes, focusing on those initiated around the time of the alert.
- Reset credentials for any accounts that were active on the affected host during the time of the alert to prevent unauthorized access.
- Review and restrict DCOM permissions and configurations on the affected host and other critical systems to limit the potential for similar attacks.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if other systems have been compromised.
- Update detection mechanisms and threat intelligence feeds to enhance monitoring for similar DCOM-based lateral movement attempts in the future.
