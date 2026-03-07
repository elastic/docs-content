---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Incoming Execution via PowerShell Remoting" prebuilt detection rule.
---

# Incoming Execution via PowerShell Remoting

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Incoming Execution via PowerShell Remoting

PowerShell Remoting enables administrators to execute commands on remote Windows systems, facilitating efficient management. However, adversaries can exploit this feature for lateral movement within a network. The detection rule identifies suspicious activity by monitoring network traffic on specific ports and processes initiated by PowerShell Remoting, flagging potential unauthorized remote executions.

### Possible investigation steps

- Review the network traffic logs to identify the source IP address involved in the alert, ensuring it is not a known or authorized management system.
- Check the destination port (5985 or 5986) to confirm it aligns with PowerShell Remoting activity and verify if the connection was expected or authorized.
- Investigate the process tree on the affected host to determine if the process initiated by wsmprovhost.exe is legitimate or if it shows signs of suspicious activity.
- Examine the parent process of wsmprovhost.exe to identify any unusual or unauthorized processes that may have triggered the PowerShell Remoting session.
- Correlate the event with user activity logs to determine if the remote execution was performed by a legitimate user or if there are signs of compromised credentials.
- Assess the risk score and severity in the context of the organization's environment to prioritize the response and determine if further containment or remediation actions are necessary.

### False positive analysis

- Legitimate administrative tasks using PowerShell Remoting can trigger the rule. To manage this, identify and whitelist known administrative IP addresses or user accounts that frequently perform remote management tasks.
- Automated scripts or scheduled tasks that use PowerShell Remoting for system maintenance might be flagged. Review and document these scripts, then create exceptions for their specific process names or execution paths.
- Security tools or monitoring solutions that leverage PowerShell Remoting for legitimate purposes may cause alerts. Verify these tools and exclude their associated network traffic or processes from the detection rule.
- Internal IT support activities that involve remote troubleshooting using PowerShell Remoting can be mistaken for threats. Maintain a list of support personnel and their IP addresses to exclude them from triggering alerts.
- Regular software updates or patch management processes that utilize PowerShell Remoting should be considered. Identify these processes and exclude their network traffic or process executions to prevent false positives.

### Response and remediation

- Isolate the affected host immediately from the network to prevent further lateral movement by the adversary.
- Terminate any suspicious PowerShell processes identified, especially those initiated by wsmprovhost.exe, to stop unauthorized remote executions.
- Conduct a thorough review of recent user activity and access logs on the affected host to identify any unauthorized access or changes.
- Reset credentials for any accounts that were used in the suspicious activity to prevent further unauthorized access.
- Apply patches and updates to the affected systems to address any vulnerabilities that may have been exploited.
- Enhance monitoring on the network for unusual activity on ports 5985 and 5986 to detect any future attempts at unauthorized PowerShell Remoting.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are compromised.
