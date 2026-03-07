---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Docker Socket Enumeration" prebuilt detection rule.
---

# Docker Socket Enumeration

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Docker Socket Enumeration

Docker sockets facilitate communication between the Docker client and daemon, enabling container management. Adversaries exploit this by accessing the socket to control containers, potentially escalating privileges or moving laterally. The detection rule identifies suspicious processes interacting with the Docker socket, using specific commands, to flag unauthorized enumeration attempts.

### Possible investigation steps

- Review the process details to confirm the presence of suspicious commands interacting with the Docker socket, specifically looking for the use of tools like curl, socat, nc, netcat, ncat, or nc.traditional.
- Examine the command line arguments of the flagged process to understand the intent and scope of the interaction with the Docker socket, focusing on paths like /var/run/docker.sock or /run/docker.sock.
- Identify the user account under which the suspicious process was executed to assess if it has legitimate access to Docker resources or if it might be compromised.
- Check the historical activity of the involved user and process to determine if this behavior is anomalous or part of a known pattern.
- Investigate any recent changes or deployments in the Docker environment that might explain the interaction with the Docker socket, such as new container setups or updates.
- Correlate the alert with other security events or logs from the same host or network segment to identify potential lateral movement or privilege escalation attempts.

### False positive analysis

- Legitimate administrative tasks using tools like curl or socat to interact with Docker for monitoring or management purposes can trigger alerts. To handle this, create exceptions for specific user accounts or scripts that are known to perform these tasks regularly.
- Automated scripts or services that check the status of Docker containers might be flagged. Identify these scripts and whitelist their process names or command lines to prevent unnecessary alerts.
- Development environments where developers frequently use command-line tools to interact with Docker may cause false positives. Consider excluding specific development machines or user groups from the rule to reduce noise.
- Continuous integration or deployment pipelines that use Docker commands as part of their workflow can be mistaken for enumeration attempts. Exclude these processes by identifying their unique command patterns or execution contexts.
- Security tools that perform regular audits or checks on Docker environments might trigger the rule. Verify these tools and add them to an exception list to avoid false alerts.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or lateral movement.
- Terminate any suspicious processes identified in the alert that are interacting with the Docker socket, such as those using curl, socat, or netcat.
- Conduct a thorough review of Docker containers on the affected host to identify any unauthorized or malicious containers. Stop and remove any that are not recognized or are deemed suspicious.
- Check for any unauthorized changes to Docker configurations or images and revert them to a known good state.
- Review and restrict permissions on the Docker socket file (/var/run/docker.sock) to limit access to only trusted users and processes.
- Escalate the incident to the security operations team for further investigation and to determine if additional hosts or systems are affected.
- Implement enhanced monitoring and logging for Docker socket interactions to detect and respond to similar threats more quickly in the future.

