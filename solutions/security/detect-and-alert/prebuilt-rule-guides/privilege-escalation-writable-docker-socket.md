---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Privilege Escalation through Writable Docker Socket" prebuilt detection rule.'
---

# Potential Privilege Escalation through Writable Docker Socket

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Privilege Escalation through Writable Docker Socket

Docker sockets facilitate communication between the Docker client and daemon, typically restricted to root or specific groups. Adversaries with write access can exploit these sockets to execute containers with elevated privileges, potentially accessing the host system. The detection rule identifies suspicious activities by monitoring processes like Docker and Socat for unauthorized socket interactions, focusing on non-root users attempting to execute commands, thus flagging potential privilege escalation attempts.

### Possible investigation steps

- Review the alert details to identify the specific process name (either "docker" or "socat") and the associated arguments that triggered the alert, focusing on the use of "unix://*/docker.sock" or "unix://*/dockershim.sock".
- Check the user and group IDs associated with the process to confirm they are non-root, as indicated by the exclusion of user.Ext.real.id and group.Ext.real.id being "0".
- Investigate the user account involved in the alert to determine if they should have access to Docker sockets and whether their permissions have been misconfigured or compromised.
- Examine the system logs and Docker daemon logs for any additional context or anomalies around the time of the alert to identify any unauthorized or suspicious activities.
- Assess the current state of the system for any unauthorized containers that may have been started, and inspect their configurations and running processes for signs of privilege escalation attempts.
- Verify the integrity and permissions of the Docker socket files to ensure they have not been altered to allow unauthorized access.

### False positive analysis

- Legitimate administrative tasks by non-root users with elevated permissions can trigger the rule. To manage this, identify trusted users or groups who regularly perform such tasks and create exceptions for their activities.
- Automated scripts or services that require Docker socket access for legitimate operations may be flagged. Review these scripts or services and whitelist their specific process names or arguments to prevent false positives.
- Development environments where developers frequently use Docker for testing might cause alerts. Consider creating a separate monitoring policy for development environments or exclude known development user accounts from this rule.
- Continuous integration/continuous deployment (CI/CD) pipelines that interact with Docker sockets can be mistakenly identified as threats. Ensure that these pipelines are running under specific service accounts and exclude these accounts from the rule.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or lateral movement.
- Terminate any unauthorized Docker containers that were started by non-root users, especially those interacting with Docker sockets.
- Review and revoke any unnecessary write permissions to Docker sockets for non-root users and groups, ensuring only trusted users have access.
- Conduct a thorough audit of user accounts and group memberships on the affected system to identify and remove any unauthorized or suspicious accounts.
- Restore the system from a known good backup if unauthorized changes or access to sensitive data are detected.
- Implement monitoring and alerting for any future unauthorized access attempts to Docker sockets, focusing on non-root user activities.
- Escalate the incident to the security operations team for further investigation and to assess potential impacts on other systems within the network.
