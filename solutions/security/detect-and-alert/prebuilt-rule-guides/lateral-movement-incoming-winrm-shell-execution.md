---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Incoming Execution via WinRM Remote Shell" prebuilt detection rule.'
---

# Incoming Execution via WinRM Remote Shell

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Incoming Execution via WinRM Remote Shell

Windows Remote Management (WinRM) is a protocol that allows for remote management and execution of commands on Windows machines. While beneficial for legitimate administrative tasks, adversaries can exploit WinRM for lateral movement by executing commands remotely. The detection rule identifies suspicious activity by monitoring network traffic on specific ports and processes initiated by WinRM, flagging potential unauthorized remote executions.

### Possible investigation steps

- Review the network traffic logs to confirm the presence of incoming connections on ports 5985 or 5986, which are used by WinRM, and verify if these connections are expected or authorized.
- Identify the source IP address of the incoming connection and determine if it belongs to a known and trusted network or device. Investigate any unfamiliar or suspicious IP addresses.
- Examine the process tree for the process initiated by winrshost.exe to identify any unusual or unauthorized processes that were started as a result of the remote execution.
- Check the user account associated with the WinRM session to ensure it is legitimate and has not been compromised. Look for any signs of unauthorized access or privilege escalation.
- Correlate the event with other security logs, such as authentication logs, to identify any related suspicious activities or patterns that might indicate lateral movement or a broader attack campaign.
- Investigate the timeline of events to determine if there are any other related alerts or activities occurring around the same time that could provide additional context or evidence of malicious intent.

### False positive analysis

- Legitimate administrative tasks using WinRM can trigger alerts. Regularly review and whitelist known administrative IP addresses or users to reduce false positives.
- Automated scripts or management tools that use WinRM for routine tasks may be flagged. Identify these scripts and create exceptions for their specific process names or execution paths.
- Monitoring tools that check system health via WinRM might be misidentified as threats. Exclude these tools by specifying their source IPs or process names in the detection rule.
- Scheduled tasks that utilize WinRM for updates or maintenance can cause alerts. Document these tasks and adjust the rule to ignore their specific execution patterns.
- Internal security scans or compliance checks using WinRM should be accounted for. Coordinate with security teams to recognize these activities and exclude them from triggering alerts.

### Response and remediation

- Isolate the affected host immediately from the network to prevent further lateral movement and potential data exfiltration.
- Terminate any suspicious processes associated with WinRM, particularly those not originating from legitimate administrative tools or known good sources.
- Review and revoke any unauthorized access credentials or accounts that may have been used to initiate the WinRM session.
- Conduct a thorough examination of the affected host for any additional signs of compromise, such as unauthorized software installations or changes to system configurations.
- Restore the affected system from a known good backup if any malicious activity or unauthorized changes are confirmed.
- Implement network segmentation to limit the ability of threats to move laterally across the network, focusing on restricting access to critical systems.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
