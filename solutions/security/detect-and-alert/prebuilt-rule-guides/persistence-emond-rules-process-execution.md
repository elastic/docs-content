---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Emond Child Process" prebuilt detection rule.
---

# Suspicious Emond Child Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Emond Child Process

The Event Monitor Daemon (emond) on macOS is a service that executes commands based on system events, like startup or user login. Adversaries exploit emond by crafting rules that trigger malicious scripts or commands during these events, enabling persistence. The detection rule identifies unusual child processes spawned by emond, such as shell scripts or command-line utilities, which are indicative of potential abuse.

### Possible investigation steps

- Review the process details to confirm the parent process is indeed emond and check the specific child process name against the list of suspicious processes such as bash, python, or curl.
- Investigate the command line arguments used by the suspicious child process to identify any potentially malicious commands or scripts being executed.
- Check the timing of the event to see if it coincides with known system events like startup or user login, which could indicate an attempt to establish persistence.
- Examine the user account associated with the process to determine if it is a legitimate user or potentially compromised account.
- Look for any recent changes to emond rules or configuration files that could have been modified to trigger the suspicious process execution.
- Correlate this event with other security alerts or logs from the same host to identify any patterns or additional indicators of compromise.

### False positive analysis

- System maintenance scripts may trigger the rule if they use shell scripts or command-line utilities. Review scheduled tasks or maintenance scripts and exclude them if they are verified as non-threatening.
- Legitimate software installations or updates might spawn processes like bash or curl. Monitor installation logs and exclude these processes if they align with known software updates.
- User-initiated scripts for automation or customization can cause alerts. Verify the user's intent and exclude these processes if they are part of regular user activity.
- Administrative tasks performed by IT staff, such as using launchctl for service management, may trigger the rule. Confirm these activities with IT staff and exclude them if they are part of routine administration.
- Development environments on macOS might use interpreters like Python or Perl. Validate the development activities and exclude these processes if they are consistent with the developer's workflow.

### Response and remediation

- Isolate the affected macOS system from the network to prevent further malicious activity and lateral movement.
- Terminate any suspicious child processes spawned by emond, such as shell scripts or command-line utilities, to halt ongoing malicious actions.
- Review and remove any unauthorized or suspicious emond rules that may have been added to execute malicious commands during system events.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malware or persistence mechanisms.
- Restore any altered or deleted system files from a known good backup to ensure system integrity.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for emond and related processes to detect similar threats in the future, ensuring alerts are configured for unusual child processes.
