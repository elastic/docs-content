---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "RPM Package Installed by Unusual Parent Process" prebuilt detection rule.'
---

# RPM Package Installed by Unusual Parent Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating RPM Package Installed by Unusual Parent Process

RPM is a package management system crucial for managing software on Linux distributions like Red Hat and CentOS. Adversaries may exploit RPM by installing backdoored or malicious packages to gain persistence or initial access. The detection rule identifies anomalies by flagging RPM installations initiated by atypical parent processes, which could indicate unauthorized or suspicious activity. This helps in early detection of potential threats by monitoring process execution patterns.

### Possible investigation steps

- Review the parent process of the RPM installation to determine if it is a known and legitimate process. Investigate any unusual or unexpected parent processes that initiated the RPM command.
- Examine the command-line arguments used with the RPM process, specifically looking for the "-i" or "--install" flags, to confirm the installation action and gather more context about the package being installed.
- Check the timestamp of the event to correlate it with other activities on the system, such as user logins or other process executions, to identify any suspicious patterns or anomalies.
- Investigate the user account under which the RPM installation was executed to determine if it aligns with expected administrative activities or if it indicates potential unauthorized access.
- Analyze the network activity around the time of the RPM installation to identify any external connections that could suggest data exfiltration or communication with a command and control server.
- Review system logs and other security alerts from the same timeframe to identify any additional indicators of compromise or related suspicious activities.

### False positive analysis

- System administrators or automated scripts may frequently install RPM packages as part of routine maintenance or updates. To manage this, create exceptions for known administrative accounts or specific scripts that regularly perform these actions.
- Some legitimate software deployment tools might use non-standard parent processes to install RPM packages. Identify and whitelist these tools to prevent unnecessary alerts.
- Development environments might trigger RPM installations through unusual parent processes during testing or software builds. Exclude these environments or specific processes from the rule to reduce false positives.
- Custom or third-party management tools that are not widely recognized might also cause alerts. Review and whitelist these tools if they are verified as safe and necessary for operations.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential lateral movement or further compromise.
- Terminate any suspicious processes related to the RPM installation that were initiated by unusual parent processes.
- Conduct a thorough review of the installed RPM packages to identify and remove any unauthorized or malicious software.
- Restore the system from a known good backup if malicious packages have been confirmed and system integrity is compromised.
- Update and patch the system to ensure all software is up-to-date, reducing the risk of exploitation through known vulnerabilities.
- Implement stricter access controls and monitoring on systems to prevent unauthorized RPM installations, focusing on unusual parent processes.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
