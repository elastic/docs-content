---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Exim4 Child Process" prebuilt detection rule.'
---

# Unusual Exim4 Child Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Exim4 Child Process

Exim4 is a widely used mail transfer agent on Linux systems, responsible for routing and delivering email. Adversaries may exploit Exim4 by spawning unexpected child processes to execute malicious commands, thereby evading detection and maintaining persistence. The detection rule identifies suspicious child processes initiated by Exim4, excluding known legitimate processes, to flag potential misuse.

### Possible investigation steps

- Review the alert details to identify the specific unusual child process name and command line arguments that were executed under the parent process exim4.
- Examine the process tree to understand the hierarchy and context of the spawned process, including any sibling or child processes that may indicate further malicious activity.
- Check the user account associated with the exim4 process to determine if it aligns with expected usage patterns or if it might be compromised.
- Investigate the source and destination of any network connections initiated by the unusual child process to identify potential data exfiltration or command and control activity.
- Analyze system logs around the time of the alert to identify any related events or anomalies that could provide additional context or evidence of compromise.
- Correlate the findings with other alerts or incidents in the environment to determine if this activity is part of a broader attack campaign.

### False positive analysis

- Development tools like cmake, gcc, and cppcheck may trigger false positives if they are used in environments where Exim4 is installed. To mitigate this, ensure these tools are included in the exclusion list if they are part of regular development activities.
- System maintenance scripts that utilize commands such as readlink, grep, and stat might be flagged. Review these scripts and add them to the exclusion list if they are verified as part of routine system operations.
- Automated deployment or configuration management tools that invoke systemctl or update-exim4.conf can be mistaken for suspicious activity. Confirm these processes are legitimate and add them to the exclusion list to prevent unnecessary alerts.
- If Exim4 is used in conjunction with SSH services, processes like sshd may appear as child processes. Verify the legitimacy of these connections and exclude them if they are part of expected behavior.
- Regularly review and update the exclusion list to reflect changes in system operations or new legitimate processes that may arise, ensuring the rule remains effective without generating excessive false positives.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Terminate any suspicious child processes of Exim4 that are not recognized as legitimate, using process management tools like `kill` or `pkill`.
- Conduct a thorough review of the Exim4 configuration files and scripts to identify unauthorized modifications or additions, and restore them from a known good backup if necessary.
- Scan the system for additional indicators of compromise, such as unauthorized user accounts or scheduled tasks, and remove any malicious artifacts found.
- Apply security patches and updates to Exim4 and the operating system to mitigate known vulnerabilities that could be exploited by attackers.
- Monitor the system for any recurrence of unusual Exim4 child processes and adjust logging and alerting to capture detailed information for further analysis.
- Escalate the incident to the security operations team for a comprehensive investigation and to determine if other systems in the network may be affected.
