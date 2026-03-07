---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Privilege Escalation via Rogue Named Pipe Impersonation" prebuilt detection rule.'
---

# Privilege Escalation via Rogue Named Pipe Impersonation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Privilege Escalation via Rogue Named Pipe Impersonation

Named pipes in Windows facilitate inter-process communication, allowing data exchange between processes. Adversaries exploit this by creating rogue named pipes, tricking privileged processes into connecting and executing malicious actions under elevated privileges. The detection rule identifies suspicious named pipe creation events, focusing on patterns indicative of impersonation attempts, thus flagging potential privilege escalation activities.

### Possible investigation steps

- Review the event logs for the specific named pipe creation event identified by the query, focusing on the file.name field to determine the exact named pipe path and assess its legitimacy.
- Correlate the event with the process that created the named pipe by examining related process creation logs, identifying the process ID and executable responsible for the action.
- Investigate the user context under which the named pipe was created to determine if it aligns with expected behavior or if it indicates potential misuse of privileges.
- Check for any recent changes or anomalies in the system's configuration or user accounts that could suggest unauthorized access or privilege escalation attempts.
- Analyze historical data for similar named pipe creation events to identify patterns or repeated attempts that could indicate a persistent threat or ongoing attack.

### False positive analysis

- Legitimate software or system processes may create named pipes that match the detection pattern. Regularly review and whitelist known benign processes that frequently create named pipes to reduce noise.
- System management tools and monitoring software might generate named pipe creation events as part of their normal operation. Identify these tools and exclude their events from triggering alerts.
- Custom in-house applications that use named pipes for inter-process communication can trigger false positives. Work with development teams to document these applications and create exceptions for their activity.
- Scheduled tasks or scripts that run with elevated privileges and create named pipes could be mistaken for malicious activity. Ensure these tasks are documented and excluded from the detection rule.
- Security software or endpoint protection solutions may use named pipes for legitimate purposes. Verify these activities and adjust the rule to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious processes associated with the rogue named pipe to halt any ongoing malicious activities.
- Conduct a thorough review of the system's event logs, focusing on named pipe creation events, to identify any other potentially compromised processes or systems.
- Reset credentials for any accounts that may have been exposed or used in the privilege escalation attempt to prevent further unauthorized access.
- Apply security patches and updates to the affected system to address any vulnerabilities that may have been exploited.
- Implement enhanced monitoring for named pipe creation events across the network to detect and respond to similar threats in the future.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to ensure comprehensive remediation efforts are undertaken.
