---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Reverse Shell via Background Process" prebuilt detection rule.'
---

# Potential Reverse Shell via Background Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Reverse Shell via Background Process

In Linux environments, background processes can be manipulated to establish reverse shells, allowing adversaries to gain remote access. By exploiting shell commands to open network sockets, attackers can create backdoor connections. The detection rule identifies suspicious executions of background processes, like 'setsid' or 'nohup', with arguments indicating socket activity in '/dev/tcp', often initiated by common shell interpreters. This helps in flagging potential reverse shell activities for further investigation.

### Possible investigation steps

- Review the process details to confirm the presence of suspicious arguments, specifically looking for '/dev/tcp' in the process.args field, which indicates an attempt to open a network socket.
- Identify the parent process by examining the process.parent.name field to determine if it is one of the common shell interpreters like 'bash', 'dash', 'sh', etc., which could suggest a script-based execution.
- Check the user context under which the process was executed to assess if it aligns with expected user behavior or if it indicates potential compromise of a user account.
- Investigate the network activity associated with the host to identify any unusual outbound connections that could correlate with the reverse shell attempt.
- Correlate the event with other security alerts or logs from the same host to identify any preceding or subsequent suspicious activities that might indicate a broader attack pattern.
- Review historical data for similar process executions on the host to determine if this is an isolated incident or part of a recurring pattern.

### False positive analysis

- Legitimate administrative scripts may use background processes with network socket activity for maintenance tasks. Review the script's purpose and source to determine if it is authorized.
- Automated monitoring tools might execute commands that match the rule's criteria. Identify these tools and consider excluding their specific process names or paths from the rule.
- Development environments often run test scripts that open network connections. Verify the development context and exclude known development-related processes to reduce noise.
- Backup or synchronization software may use similar techniques to transfer data. Confirm the software's legitimacy and add exceptions for its processes if necessary.
- System updates or package management tools might trigger alerts when installing or updating software. Monitor these activities and whitelist trusted update processes.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious background processes identified by the alert, specifically those involving 'setsid' or 'nohup' with '/dev/tcp' in their arguments.
- Conduct a thorough review of the affected system's process and network activity logs to identify any additional indicators of compromise or lateral movement.
- Reset credentials for any accounts that were active on the affected system to prevent unauthorized access using potentially compromised credentials.
- Apply security patches and updates to the affected system to address any vulnerabilities that may have been exploited.
- Implement network segmentation to limit the ability of compromised systems to communicate with critical infrastructure or sensitive data repositories.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are affected.
