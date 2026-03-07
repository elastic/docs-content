---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Code Execution via Postgresql" prebuilt detection rule.
---

# Potential Code Execution via Postgresql

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Code Execution via Postgresql

PostgreSQL, a robust open-source database system, can be exploited by attackers to execute arbitrary code if they gain unauthorized access or exploit vulnerabilities like SQL injection. Adversaries may leverage command execution capabilities to perform malicious actions. The detection rule identifies suspicious processes initiated by the PostgreSQL user, focusing on shell executions that resemble command injection patterns, while excluding legitimate operations, to flag potential threats.

### Possible investigation steps

- Review the process details to confirm the presence of suspicious shell executions by the PostgreSQL user, focusing on processes with arguments containing "*sh" and "echo*".
- Check the parent process information to determine if the process was initiated by a known legitimate service, such as "puppet", or if it includes "BECOME-SUCCESS-" in the command line, which are excluded from the rule.
- Investigate the source of the PostgreSQL access to identify if it originated from an unauthorized or unusual IP address or user account.
- Analyze the timeline of events leading up to and following the alert to identify any patterns or additional suspicious activities that may indicate a broader attack.
- Correlate the alert with other security events or logs from the same host or network segment to assess if there are related indicators of compromise or ongoing threats.

### False positive analysis

- Puppet processes may trigger false positives due to their legitimate use of shell commands. To mitigate this, ensure that puppet-related processes are excluded by verifying that process.parent.name is set to "puppet".
- Automation tools that use shell scripts for configuration management might be flagged. Review and exclude these by checking for specific command patterns that are known to be safe, such as those containing "BECOME-SUCCESS".
- Scheduled maintenance scripts executed by the postgres user could be misidentified as threats. Identify these scripts and add them to an exclusion list based on their command line patterns.
- Regular database backup operations that involve shell commands might be mistakenly flagged. Document these operations and exclude them by matching their specific command line arguments.
- Custom monitoring scripts that execute shell commands under the postgres user should be reviewed and excluded if they are verified as non-malicious.

### Response and remediation

- Immediately isolate the affected PostgreSQL server from the network to prevent further unauthorized access or malicious actions.
- Terminate any suspicious processes identified by the detection rule to halt potential malicious activities.
- Conduct a thorough review of the PostgreSQL server logs to identify any unauthorized access attempts or successful exploitations, focusing on the timeframes around the detected events.
- Reset credentials for the PostgreSQL user and any other potentially compromised accounts to prevent further unauthorized access.
- Apply the latest security patches and updates to the PostgreSQL server to mitigate known vulnerabilities that could be exploited.
- Implement network segmentation to limit access to the PostgreSQL server, ensuring only authorized systems and users can connect.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on other systems within the network.
