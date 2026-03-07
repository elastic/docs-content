---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Persistence via Folder Action Script" prebuilt detection rule.
---

# Persistence via Folder Action Script

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Persistence via Folder Action Script

Folder Action scripts on macOS automate tasks by executing scripts when folder contents change. Adversaries exploit this by attaching malicious scripts to folders, ensuring execution upon folder events, thus achieving persistence. The detection rule identifies suspicious script executions by monitoring specific processes initiated by the UserScriptService, excluding known benign scripts, to flag potential threats.

### Possible investigation steps

- Review the process details to confirm the execution of a script by checking the process name and arguments, ensuring it matches the suspicious criteria outlined in the detection rule.
- Investigate the parent process, com.apple.foundation.UserScriptService, to understand the context of the script execution and identify any unusual behavior or anomalies.
- Examine the specific folder associated with the Folder Action script to determine if it has been modified recently or contains any unauthorized or unexpected scripts.
- Check the user account associated with the script execution to verify if the activity aligns with normal user behavior or if it indicates potential compromise.
- Look for any additional related alerts or logs that might provide further context or evidence of malicious activity, such as other script executions or file modifications around the same time.

### False positive analysis

- Scripts associated with legitimate applications like iTerm2 and Microsoft Office may trigger alerts. These are known benign scripts and can be excluded by adding their paths to the exception list in the detection rule.
- Custom user scripts that automate routine tasks might be flagged. Users should review these scripts and, if verified as safe, add their specific paths to the exclusion criteria.
- Development environments that frequently execute scripts for testing purposes can cause false positives. Developers should ensure that these scripts are executed in a controlled environment and consider excluding their paths if they are consistently flagged.
- System maintenance scripts that are scheduled to run during folder events might be detected. Users should verify these scripts' legitimacy and exclude them if they are part of regular system operations.
- Backup or synchronization tools that use scripts to manage file changes in folders could be mistakenly identified. Confirm these tools' activities and exclude their script paths if they are part of trusted operations.

### Response and remediation

- Isolate the affected system from the network to prevent further execution of the malicious script and potential lateral movement.
- Terminate any suspicious processes identified by the detection rule, particularly those initiated by the UserScriptService that match the query criteria.
- Remove or disable the malicious Folder Action script from the affected folder to prevent future execution.
- Conduct a thorough review of the affected system's folder action scripts to identify and remove any additional unauthorized or suspicious scripts.
- Restore any affected files or system components from a known good backup to ensure system integrity.
- Monitor the system for any signs of re-infection or further suspicious activity, focusing on processes and scripts similar to those identified in the alert.
- Escalate the incident to the security team for further investigation and to determine if additional systems are affected, ensuring a comprehensive response to the threat.
