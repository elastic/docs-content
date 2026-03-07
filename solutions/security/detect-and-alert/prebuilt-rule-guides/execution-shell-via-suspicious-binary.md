---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Reverse Shell via Suspicious Binary" prebuilt detection rule.
---

# Potential Reverse Shell via Suspicious Binary

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Reverse Shell via Suspicious Binary

Reverse shells are a common technique used by attackers to gain persistent access to a compromised system. They exploit legitimate shell environments to execute commands remotely. Adversaries often deploy binaries in unusual directories to evade detection. The detection rule identifies suspicious binaries executed in these locations, followed by network activity and shell spawning, indicating potential reverse shell activity. This approach helps in identifying unauthorized access attempts on Linux systems.

### Possible investigation steps

- Review the process execution details to identify the suspicious binary's path and name, focusing on the directories specified in the query such as /tmp, /var/tmp, and /dev/shm.
- Examine the parent process of the suspicious binary to determine if it was spawned by a legitimate shell process like bash or sh, as indicated in the query.
- Analyze the network activity associated with the suspicious binary, paying attention to the destination IP address to identify any external connections that are not local (i.e., not 127.0.0.1 or ::1).
- Check the process tree to see if a new shell was spawned following the network activity, which could indicate a reverse shell attempt.
- Investigate the user account under which the suspicious process was executed to assess if it aligns with expected behavior or if it might be compromised.
- Correlate the event timestamps to understand the sequence of actions and verify if they align with typical reverse shell behavior patterns.

### False positive analysis

- Legitimate administrative scripts or binaries may be executed from directories like /tmp or /var/tmp during maintenance tasks. To handle this, create exceptions for known scripts or binaries used by trusted administrators.
- Automated deployment tools might temporarily use directories such as /dev/shm or /run for staging files. Identify these tools and exclude their processes from triggering the rule.
- Custom monitoring or backup scripts could initiate network connections from non-standard directories. Review these scripts and whitelist their activities if they are verified as safe.
- Development or testing environments might involve executing binaries from unusual locations. Ensure these environments are well-documented and exclude their processes from the detection rule.
- Some legitimate applications may spawn shells as part of their normal operation. Identify these applications and add them to an exception list to prevent false alerts.

### Response and remediation

- Isolate the affected system from the network immediately to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified by the detection rule, especially those originating from unusual directories or involving shell spawning.
- Conduct a thorough review of the system's scheduled tasks, startup scripts, and cron jobs to identify and remove any unauthorized entries that may have been added by the attacker.
- Analyze network logs to identify any external IP addresses involved in the suspicious network activity and block these IPs at the firewall to prevent further connections.
- Restore the affected system from a known good backup to ensure that any malicious changes are reverted.
- Update and patch the system to the latest security standards to close any vulnerabilities that may have been exploited.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on other systems within the network.
