---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "DPKG Package Installed by Unusual Parent Process" prebuilt detection rule.
---

# DPKG Package Installed by Unusual Parent Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating DPKG Package Installed by Unusual Parent Process

DPKG is a core utility for managing Debian packages on Linux systems, crucial for software installation and maintenance. Adversaries may exploit DPKG to install malicious packages, leveraging unusual parent processes to evade detection. The detection rule identifies such anomalies by monitoring DPKG executions initiated by atypical parent processes, signaling potential unauthorized package installations.

### Possible investigation steps

- Review the process tree to identify the parent process of the dpkg execution. Determine if the parent process is legitimate or unusual for package installations.
- Examine the command-line arguments used with the dpkg command, specifically looking for the "-i" or "--install" flags, to understand what package was being installed.
- Check the source and integrity of the package being installed to ensure it is from a trusted repository or source.
- Investigate the user account under which the dpkg command was executed to determine if it has the necessary permissions and if the activity aligns with the user's typical behavior.
- Correlate the event with other logs or alerts around the same timeframe to identify any related suspicious activities or patterns.
- Assess the system for any signs of compromise or unauthorized changes following the package installation.

### False positive analysis

- System updates or maintenance scripts may trigger the rule when legitimate administrative tools or scripts use dpkg to install updates. To handle this, identify and whitelist known maintenance scripts or processes that regularly perform package installations.
- Automated deployment tools like Ansible or Puppet might use dpkg for software deployment, leading to false positives. Exclude these tools by adding their process names to an exception list if they are part of your standard operations.
- Custom internal applications or scripts that manage software installations could also cause alerts. Review these applications and, if verified as safe, configure exceptions for their parent processes.
- Developers or system administrators using dpkg for testing or development purposes might inadvertently trigger the rule. Establish a policy for such activities and exclude known development environments or user accounts from triggering alerts.
- Backup or recovery operations that reinstall packages as part of their process can be mistaken for malicious activity. Identify these operations and exclude their associated processes from the rule.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized package installations or lateral movement by the adversary.
- Terminate the dpkg process if it is still running to stop any ongoing malicious package installation.
- Identify and remove any suspicious or unauthorized packages installed by the dpkg command using the package management tools available on the system.
- Conduct a thorough review of the system's package installation logs and history to identify any other potentially malicious packages or unusual installation activities.
- Restore the system from a known good backup if malicious packages have altered critical system components or configurations.
- Implement stricter access controls and monitoring on systems to prevent unauthorized use of package management utilities by non-administrative users or processes.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected, ensuring a coordinated response to the threat.
