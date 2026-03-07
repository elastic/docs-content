---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Sensitive File Access followed by Compression" prebuilt detection rule.
---

# Sensitive File Access followed by Compression

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Sensitive File Access followed by Compression

Data exfiltration is a critical phase of many attack campaigns where threat actors collect and stage sensitive data for transfer out of the environment. On macOS, attackers commonly target high-value files such as SSH keys, AWS credentials, browser cookies, and login keychains. This detection rule identifies a behavioral pattern where a process accesses sensitive files and subsequently creates compressed archives, which is a hallmark of data staging activity prior to exfiltration.

### Possible investigation steps

- Review the process.entity_id and process.name fields to identify the application that accessed sensitive files and created the compressed archive.
- Examine the file.path fields in both events to determine which specific sensitive files were accessed and where the archive was created.
- Analyze the process.parent.executable and process.command_line to understand how the process was launched and whether it originated from a suspicious source.
- Check for network connection events from the same process or host shortly after the compression activity, as this may indicate attempted exfiltration.
- Investigate the user.name associated with the activity to determine if the behavior is consistent with their role and normal operations.
- Review the destination path of the compressed file to assess whether it was placed in a location commonly used for staging, such as /Users/Shared or temporary directories.
- Correlate with other security alerts on the same host to identify if this is part of a broader attack chain.

### False positive analysis

- Legitimate backup applications may access sensitive files and create compressed archives as part of scheduled backup operations. Verify the process against known backup tools like Time Machine or third-party backup solutions.
- System administrators performing manual archiving of configuration files or credentials for secure storage may trigger this rule. Confirm with IT operations if such activities were planned.
- Development workflows may involve compressing SSH keys or credentials for transfer between development environments. Review with development teams before escalating.
- Some applications may legitimately compress browser data or credentials during migrations or exports. Verify the application's purpose and user intent.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent any pending data exfiltration.
- Identify and quarantine the compressed archive file to prevent it from being transferred or deleted by the attacker.
- Conduct a thorough review of the files that were accessed and compressed to assess the scope of potential data exposure.
- Rotate all credentials that may have been compromised, including SSH keys, AWS access keys, API tokens, and any passwords stored in keychains or browsers.
- Perform a forensic analysis of the system to identify the initial access vector and any persistence mechanisms.
- Review network logs and proxy data to determine if any data was successfully exfiltrated prior to detection.
- Escalate to the incident response team for further investigation if the activity appears to be part of a coordinated attack campaign.

