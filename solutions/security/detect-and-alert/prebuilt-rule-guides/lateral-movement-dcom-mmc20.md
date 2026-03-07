---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Incoming DCOM Lateral Movement with MMC" prebuilt detection rule.'
---

# Incoming DCOM Lateral Movement with MMC

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Incoming DCOM Lateral Movement with MMC

Distributed Component Object Model (DCOM) enables software components to communicate over a network, often used in Windows environments for remote management. Adversaries exploit DCOM to execute commands remotely, leveraging applications like MMC20 to move laterally. The detection rule identifies suspicious activity by monitoring network traffic and process creation patterns, flagging potential misuse when MMC initiates remote commands, indicating possible lateral movement or defense evasion tactics.

### Possible investigation steps

- Review the network traffic logs to identify the source IP address that initiated the connection to the host running mmc.exe. Verify if this IP address is known and expected within the network environment.
- Examine the process creation logs to confirm the parent-child relationship between mmc.exe and any suspicious processes. Investigate the child processes for any unusual or unauthorized activities.
- Check the source and destination ports (both should be >= 49152) involved in the network connection to determine if they align with typical application behavior or if they are indicative of potential misuse.
- Investigate the timeline of events to see if there are any other related alerts or activities on the same host or originating from the same source IP address, which could provide additional context or indicate a broader attack pattern.
- Correlate the findings with any existing threat intelligence or known attack patterns related to DCOM abuse and lateral movement to assess the potential risk and impact on the organization.

### False positive analysis

- Legitimate administrative tasks using MMC may trigger the rule. Regularly review and document routine administrative activities to differentiate them from suspicious behavior.
- Automated scripts or management tools that use MMC for remote management can cause false positives. Identify and whitelist these tools by their process and network patterns.
- Internal network scanning or monitoring tools might mimic the behavior detected by the rule. Exclude known IP addresses or ranges associated with these tools to reduce noise.
- Scheduled tasks or maintenance operations that involve MMC could be misinterpreted as lateral movement. Ensure these tasks are logged and recognized as part of normal operations.
- Software updates or patches that require MMC to execute remote commands might trigger alerts. Maintain an updated list of such activities and exclude them from triggering the rule.

### Response and remediation

- Isolate the affected host immediately from the network to prevent further lateral movement and contain the threat.
- Terminate any suspicious processes associated with mmc.exe on the affected host to stop any ongoing malicious activity.
- Conduct a thorough review of the affected host's event logs and network traffic to identify any additional indicators of compromise or other affected systems.
- Reset credentials for any accounts that were accessed or potentially compromised during the incident to prevent unauthorized access.
- Apply patches and updates to the affected systems and any other vulnerable systems in the network to mitigate known vulnerabilities that could be exploited.
- Implement network segmentation to limit the ability of threats to move laterally within the network in the future.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional actions are necessary.
