---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Sublime Plugin or Application Script Modification" prebuilt detection rule.
---

# Sublime Plugin or Application Script Modification

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Sublime Plugin or Application Script Modification

Sublime Text, a popular text editor, supports plugins and scripts written in Python to enhance functionality. Adversaries may exploit this by altering these scripts to execute malicious code whenever the application launches, achieving persistence. The detection rule identifies suspicious modifications or creations of Python files in specific Sublime directories on macOS, excluding legitimate processes, to flag potential threats.

### Possible investigation steps

- Review the file path and name of the modified or created Python file to determine if it aligns with known Sublime Text plugin directories, specifically checking paths like "/Users/*/Library/Application Support/Sublime Text*/Packages/*.py" and "/Applications/Sublime Text.app/Contents/MacOS/sublime.py".
- Examine the process that triggered the file change or creation event, ensuring it is not one of the excluded legitimate processes such as those from "/Applications/Sublime Text*.app/Contents/*" or "/usr/local/Cellar/git/*/bin/git".
- Analyze the contents of the modified or newly created Python file for any suspicious or unauthorized code, focusing on scripts that may execute commands or connect to external networks.
- Check the modification or creation timestamp of the file to correlate with any known user activity or other security events that occurred around the same time.
- Investigate the user account associated with the file modification to determine if the activity aligns with their typical behavior or if it might indicate compromised credentials.
- Look for any additional indicators of compromise on the host, such as unusual network connections or other file modifications, to assess the broader impact of the potential threat.

### False positive analysis

- Legitimate Sublime Text updates or installations may trigger the rule by modifying or creating Python files in the specified directories. Users can mitigate this by temporarily disabling the rule during known update periods or by verifying the update source.
- Development activities involving Sublime Text plugins or scripts can cause false positives. Developers should consider excluding their specific user paths or processes from the rule to prevent unnecessary alerts.
- Automated backup or synchronization tools that modify Sublime Text configuration files might be flagged. Users can exclude these tools' processes from the rule to avoid false positives.
- System maintenance or cleanup scripts that interact with Sublime Text directories could trigger alerts. Identifying and excluding these scripts from the rule can help manage false positives.
- Version control operations, such as those involving git, may modify files in the monitored directories. Users should ensure that legitimate git processes are included in the exclusion list to prevent false alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further spread of any potential malicious activity.
- Terminate any suspicious processes related to Sublime Text that are not part of the legitimate process list provided in the detection rule.
- Restore the modified or newly created Python files in the specified Sublime directories from a known good backup to ensure no malicious code persists.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection tools to identify and remove any additional malicious payloads.
- Review system logs and the history of file changes to identify any unauthorized access or modifications, and document findings for further analysis.
- Escalate the incident to the security operations team for a deeper investigation into potential compromise vectors and to assess the need for broader organizational response.
- Implement additional monitoring on the affected system and similar environments to detect any recurrence of the threat, ensuring enhanced logging for the specified directories and processes.
