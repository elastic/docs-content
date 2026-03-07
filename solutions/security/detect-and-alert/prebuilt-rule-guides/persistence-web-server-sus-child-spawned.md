---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Process Spawned from Web Server Parent" prebuilt detection rule.
---

# Unusual Process Spawned from Web Server Parent

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Process Spawned from Web Server Parent

Web servers like Apache, Nginx, and others are crucial for hosting applications and services. Adversaries exploit these servers by spawning unauthorized processes to maintain persistence or execute malicious commands. The detection rule identifies anomalies by monitoring low-frequency process spawns from web server parents, focusing on unusual user IDs, directories, and process counts, which may indicate potential threats.

### Possible investigation steps

- Review the process.executable and process.command_line fields to understand the nature of the process that was spawned and assess if it aligns with expected behavior for the web server environment.
- Examine the process.working_directory to determine if the directory is a legitimate location for web server operations or if it appears suspicious, such as being outside typical web server directories.
- Check the user.name and user.id fields to verify if the process was executed by a legitimate web server user or if it was initiated by an unexpected or unauthorized user account.
- Investigate the process.parent.executable to confirm whether the parent process is a known and trusted web server executable or if it has been tampered with or replaced.
- Correlate the event with other logs or alerts from the same agent.id to identify any additional suspicious activities or patterns that may indicate a broader compromise.
- Assess the host.os.type to ensure the alert pertains to a Linux system, as specified in the query, and verify if there are any known vulnerabilities or misconfigurations on the host that could have been exploited.

### False positive analysis

- Processes related to legitimate web server maintenance tasks may trigger alerts. Review scheduled tasks or cron jobs that align with the alert timing and consider excluding these specific processes if they are verified as non-threatening.
- Development environments often spawn processes that mimic attack patterns. Identify and exclude processes originating from known development directories or executed by development user accounts.
- Automated scripts or monitoring tools running under web server user accounts can be mistaken for malicious activity. Verify these scripts and add exceptions for their specific process names or working directories.
- Frequent updates or deployments in web applications can lead to unusual process spawns. Document these activities and exclude related processes if they consistently match the alert criteria during known update windows.
- Custom web server modules or plugins may execute processes that appear suspicious. Validate these modules and exclude their associated processes if they are part of normal operations.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further malicious activity and potential lateral movement.
- Terminate any suspicious processes identified by the alert that are not part of legitimate web server operations.
- Conduct a thorough review of the process command lines and executables flagged by the alert to identify any malicious scripts or binaries. Remove or quarantine these files as necessary.
- Check for unauthorized changes in web server configurations or files within the working directories flagged by the alert. Restore any altered files from a known good backup.
- Review user accounts and permissions associated with the web server processes to ensure no unauthorized accounts or privilege escalations have occurred. Reset passwords and revoke unnecessary access.
- Monitor network traffic from the affected host for any signs of command and control communication, and block any identified malicious IP addresses or domains.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are compromised.

