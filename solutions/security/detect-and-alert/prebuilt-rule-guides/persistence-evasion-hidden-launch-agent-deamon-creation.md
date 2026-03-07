---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Creation of Hidden Launch Agent or Daemon" prebuilt detection rule.
---

# Creation of Hidden Launch Agent or Daemon

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Creation of Hidden Launch Agent or Daemon

Launch agents and daemons in macOS are background services that start at login or system boot, respectively, to perform various tasks. Adversaries exploit this by creating hidden agents or daemons to maintain persistence and evade defenses. The detection rule identifies suspicious creation of these services by monitoring specific system paths for new entries, alerting analysts to potential unauthorized persistence mechanisms.

### Possible investigation steps

- Review the file path of the newly created launch agent or daemon to determine if it matches any known legitimate software installations or updates.
- Check the file creation timestamp to correlate with any recent user activities or system changes that might explain the creation of the file.
- Investigate the contents of the .plist file to identify the program or script it is set to execute, and assess whether it is a known or potentially malicious application.
- Examine the user account associated with the file path, especially if it is located in a user's Library directory, to determine if the user has a history of installing unauthorized software.
- Cross-reference the file path and associated executable with threat intelligence sources to identify any known indicators of compromise or malicious behavior.
- Look for any other recent file modifications or creations in the same directory that might indicate additional persistence mechanisms or related malicious activity.

### False positive analysis

- System or application updates may create or modify launch agents or daemons as part of legitimate processes. Users can monitor update schedules and correlate alerts with known update activities to verify legitimacy.
- Some third-party applications install launch agents or daemons to provide background services or updates. Users should maintain an inventory of installed applications and their expected behaviors to identify benign entries.
- User-created scripts or automation tools might use launch agents or daemons for personal productivity tasks. Users can document and exclude these known scripts from monitoring to reduce noise.
- Administrative tools or security software might create temporary launch agents or daemons during scans or system maintenance. Users should verify the source and purpose of these entries and consider excluding them if they are part of routine operations.
- Regularly review and update exclusion lists to ensure they reflect current system configurations and software installations, minimizing the risk of overlooking new threats.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent potential lateral movement or data exfiltration by the adversary.
- Identify and terminate any suspicious processes associated with the newly created launch agent or daemon using Activity Monitor or command-line tools like `launchctl`.
- Remove the unauthorized launch agent or daemon by deleting the corresponding `.plist` file from the identified path. Ensure the file is not recreated by monitoring the directory for changes.
- Conduct a thorough review of user accounts and permissions on the affected system to ensure no unauthorized accounts or privilege escalations have occurred.
- Restore the system from a known good backup if the integrity of the system is in question and further compromise is suspected.
- Escalate the incident to the security operations team for a deeper forensic analysis to determine the root cause and scope of the intrusion.
- Update and enhance endpoint detection and response (EDR) solutions to improve monitoring and alerting for similar persistence mechanisms in the future.
