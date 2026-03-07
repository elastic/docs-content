---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Command Execution from Web Server Parent" prebuilt detection rule.'
---

# Unusual Command Execution from Web Server Parent

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Command Execution from Web Server Parent

Web servers, such as Apache or Nginx, are crucial for hosting web applications, often running on Linux systems. Adversaries exploit vulnerabilities in these servers to execute arbitrary commands, typically through web shells, blending malicious activity with legitimate server processes. The detection rule identifies suspicious command executions originating from web server processes, focusing on unusual patterns and contexts, such as unexpected working directories or command structures, to flag potential compromises.

### Possible investigation steps

- Review the process.command_line field to understand the specific command executed and assess its legitimacy or potential malicious intent.
- Examine the process.working_directory to determine if the command was executed from an unusual or suspicious directory, which could indicate a compromise.
- Check the process.parent.executable and process.parent.name fields to identify the parent process and verify if it is a known web server or related service that could be exploited.
- Investigate the user.name and user.id fields to confirm if the command was executed by a legitimate user or service account, or if it was potentially executed by an unauthorized user.
- Correlate the @timestamp with other logs and events to identify any related activities or anomalies occurring around the same time, which could provide additional context or evidence of an attack.
- Assess the agent.id to determine if the alert is isolated to a single host or if similar activities are observed across multiple hosts, indicating a broader issue.

### False positive analysis

- Web development or testing environments may frequently execute commands from web server processes. To handle this, exclude specific working directories like /var/www/dev or /var/www/test from the rule.
- Automated scripts or cron jobs running under web server user accounts can trigger alerts. Identify these scripts and add exceptions for their specific command lines or user IDs.
- Legitimate administrative tasks performed by web server administrators might appear suspicious. Document these tasks and exclude their associated command lines or parent executables.
- Continuous integration or deployment processes that involve web server interactions can be mistaken for threats. Exclude known CI/CD tool command lines or working directories from the rule.
- Monitoring or logging tools that interact with web server processes may generate false positives. Identify these tools and exclude their specific process names or parent executables.

### Response and remediation

- Isolate the affected host immediately to prevent further malicious activity and lateral movement within the network. This can be done by removing the host from the network or applying network segmentation.

- Terminate any suspicious processes identified by the detection rule, especially those originating from web server parent processes executing shell commands. Use process IDs and command lines from the alert to target specific processes.

- Conduct a thorough review of the web server logs and application logs to identify any unauthorized access or modifications. Look for patterns that match the command execution detected and any other anomalies.

- Patch the web server and any associated applications to address known vulnerabilities that may have been exploited. Ensure that all software is up to date with the latest security patches.

- Restore the affected system from a known good backup if any unauthorized changes or persistent threats are detected. Ensure that the backup is free from compromise before restoration.

- Implement additional monitoring and alerting for similar activities, focusing on unusual command executions and web server behavior. Enhance logging and alerting to capture more detailed information about process executions and network connections.

- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if the attack is part of a larger campaign. Provide them with all relevant data and findings from the initial containment and remediation steps.
