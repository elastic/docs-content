---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious System Commands Executed by Previously Unknown Executable" prebuilt detection rule.'
---

# Suspicious System Commands Executed by Previously Unknown Executable

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious System Commands Executed by Previously Unknown Executable

In Linux environments, system commands are essential for managing processes and configurations. Adversaries exploit this by executing commands via unknown executables in vulnerable directories, aiming to run unauthorized code. The detection rule identifies such anomalies by monitoring command executions from unfamiliar sources, excluding known safe processes, thus highlighting potential threats for further investigation.

### Possible investigation steps

- Review the process.executable path to determine if it is located in a commonly abused directory such as /tmp, /dev/shm, or /var/tmp, which may indicate malicious intent.
- Examine the process.args to identify which specific system command was executed (e.g., hostname, id, ifconfig) and assess whether its execution is typical for the system's normal operations.
- Check the process.parent.executable to understand the parent process that initiated the suspicious command execution, ensuring it is not a known safe process or a legitimate system service.
- Investigate the user account associated with the process to determine if it has the necessary permissions and if the activity aligns with the user's typical behavior.
- Correlate the event with other logs or alerts from the same host to identify any patterns or additional suspicious activities that may indicate a broader compromise.
- Assess the risk score and severity in the context of the environment to prioritize the investigation and response efforts accordingly.

### False positive analysis

- System maintenance scripts or automated tasks may trigger alerts if they execute common system commands from directories like /tmp or /var/tmp. To handle this, identify these scripts and add their executables to the exclusion list.
- Custom user scripts that perform routine checks using commands like ls or ps might be flagged. Review these scripts and consider adding their paths to the known safe processes to prevent unnecessary alerts.
- Development or testing environments often use temporary executables in directories such as /dev/shm. If these are known and non-threatening, include their paths in the exception list to reduce false positives.
- Some monitoring tools or agents might execute commands like uptime or whoami from non-standard locations. Verify these tools and update the exclusion criteria to include their executables or parent processes.
- In environments with containerized applications, processes running from /run/containerd or similar paths might be incorrectly flagged. Ensure these paths are accounted for in the exclusion settings if they are part of legitimate operations.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious processes identified by the alert, especially those originating from unknown executables in commonly abused directories.
- Conduct a thorough review of the affected directories (e.g., /tmp, /var/tmp, /dev/shm) to identify and remove any unauthorized or malicious files or executables.
- Restore any altered system configurations or files from a known good backup to ensure system integrity.
- Implement stricter access controls and permissions on the directories identified in the alert to prevent unauthorized executable placement.
- Monitor the system for any signs of persistence mechanisms, such as cron jobs or startup scripts, and remove any that are unauthorized.
- Escalate the incident to the security operations team for further analysis and to determine if additional systems may be compromised.
