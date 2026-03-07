---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Privilege Escalation via Container Misconfiguration" prebuilt detection rule.'
---

# Potential Privilege Escalation via Container Misconfiguration

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Privilege Escalation via Container Misconfiguration

Containers, managed by tools like runc and ctr, isolate applications for security and efficiency. Misconfigurations can allow attackers to exploit these tools, running containers with elevated privileges or accessing sensitive host resources. The detection rule identifies suspicious use of these utilities by non-root users in interactive sessions, flagging potential privilege escalation attempts.

### Possible investigation steps

- Review the alert details to identify the specific non-root user and group involved in the suspicious activity, as indicated by the user.Ext.real.id and group.Ext.real.id fields.
- Examine the process tree to understand the parent-child relationship of the processes, focusing on the interactive nature of both the process and its parent, as indicated by process.interactive and process.parent.interactive fields.
- Investigate the command-line arguments used with the runc or ctr utilities, particularly looking for the use of "run" and any potentially dangerous flags like "--privileged" or "--mount" that could indicate an attempt to escalate privileges.
- Check the system logs and audit logs for any additional context around the time of the alert, focusing on any other suspicious activities or anomalies involving the same user or process.
- Assess the configuration and access controls of the container management tools on the host to identify any misconfigurations or vulnerabilities that could have been exploited.

### False positive analysis

- Non-root users in development environments may frequently use runc or ctr for legitimate container management tasks. To mitigate this, consider creating exceptions for specific user IDs or groups known to perform these actions regularly.
- Automated scripts or CI/CD pipelines might execute container commands interactively without root permissions. Identify these scripts and exclude their associated user accounts or process names from triggering the rule.
- Some system administrators may operate with non-root accounts for security reasons but still require access to container management tools. Document these users and adjust the rule to exclude their activities by user ID or group ID.
- Training or testing environments where users are encouraged to experiment with container configurations might trigger false positives. Implement a separate monitoring policy for these environments to reduce noise in production alerts.

### Response and remediation

- Immediately isolate the affected container to prevent further unauthorized access or potential lateral movement within the host system.
- Terminate any suspicious container processes identified by the detection rule to halt any ongoing privilege escalation attempts.
- Conduct a thorough review of container configurations and permissions, specifically focusing on the use of runc and ctr utilities, to identify and rectify any misconfigurations that allow non-root users to execute privileged operations.
- Implement strict access controls and enforce the principle of least privilege for container management utilities to ensure only authorized users can execute privileged commands.
- Monitor for any additional signs of compromise or unusual activity on the host system, particularly focusing on processes initiated by non-root users with elevated privileges.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on the broader environment.
- Update and enhance detection capabilities to include additional indicators of compromise related to container misconfigurations and privilege escalation attempts, ensuring timely alerts for similar threats in the future.
