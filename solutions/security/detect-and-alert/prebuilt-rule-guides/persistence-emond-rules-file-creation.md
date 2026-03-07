---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Emond Rules Creation or Modification" prebuilt detection rule.'
---

# Emond Rules Creation or Modification

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Emond Rules Creation or Modification

The Event Monitor Daemon (emond) on macOS is a service that executes commands based on specific system events. Adversaries can exploit this by crafting rules to trigger malicious actions during events like startup or login. The detection rule monitors for new or altered emond rule files, signaling potential unauthorized modifications that could indicate persistence tactics.

### Possible investigation steps

- Review the file path of the modified or newly created emond rule to determine if it matches known legitimate configurations or if it appears suspicious, focusing on paths like "/private/etc/emond.d/rules/*.plist" and "/private/var/db/emondClients/*".
- Check the timestamp of the file creation or modification to correlate with any known user activity or scheduled tasks that could explain the change.
- Analyze the contents of the modified or newly created plist file to identify any commands or scripts that are set to execute, looking for signs of malicious intent or unauthorized actions.
- Investigate the user account associated with the file modification event to determine if the activity aligns with their typical behavior or if it suggests potential compromise.
- Cross-reference the event with other security alerts or logs from the same timeframe to identify any related suspicious activities or patterns that could indicate a broader attack.

### False positive analysis

- System or application updates may modify emond rule files as part of legitimate maintenance activities. Users can create exceptions for known update processes by identifying the associated process names or hashes and excluding them from alerts.
- Administrative tasks performed by IT personnel, such as configuring new system policies or settings, might involve legitimate changes to emond rules. To handle these, maintain a list of authorized personnel and their activities, and exclude these from triggering alerts.
- Security software or management tools that automate system configurations could also modify emond rules. Identify these tools and their expected behaviors, and configure exceptions based on their typical file paths or process identifiers.
- Scheduled maintenance scripts that interact with emond rules for system health checks or optimizations should be documented. Exclude these scripts by verifying their signatures or paths to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent potential lateral movement or further execution of malicious rules.
- Review and back up the current emond rule files located in the specified directories to understand the scope of modifications and preserve evidence for further analysis.
- Remove or revert any unauthorized or suspicious emond rule files to their original state to stop any malicious actions triggered by these rules.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection tools to identify and remove any additional malware or persistence mechanisms.
- Restore the system from a known good backup if the integrity of the system is in question and unauthorized changes cannot be fully reversed.
- Escalate the incident to the security operations team for further investigation and to determine if other systems may be affected by similar unauthorized emond rule modifications.
- Implement enhanced monitoring and alerting for changes to emond rule files to quickly detect and respond to future unauthorized modifications.
