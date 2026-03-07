---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Persistence via Atom Init Script Modification" prebuilt detection rule.'
---

# Potential Persistence via Atom Init Script Modification

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Persistence via Atom Init Script Modification

Atom, a popular text editor, allows customization via the `init.coffee` script, which executes JavaScript upon startup. Adversaries exploit this by embedding malicious code, ensuring persistence each time Atom launches. The detection rule identifies suspicious modifications to this script on macOS, excluding benign processes and root user actions, thus highlighting potential unauthorized persistence attempts.

### Possible investigation steps

- Review the file modification details for /Users/*/.atom/init.coffee to identify the exact changes made to the script.
- Investigate the process that modified the init.coffee file by examining the process name and user associated with the modification, ensuring it is not Atom, xpcproxy, or the root user.
- Check the user account involved in the modification for any unusual activity or recent changes, such as new software installations or privilege escalations.
- Analyze the content of the modified init.coffee file for any suspicious or unfamiliar JavaScript code that could indicate malicious intent.
- Correlate the modification event with other security alerts or logs from the same host to identify any related suspicious activities or patterns.
- If malicious code is found, isolate the affected system and conduct a deeper forensic analysis to determine the scope and impact of the potential compromise.

### False positive analysis

- Frequent legitimate updates to the init.coffee file by developers or power users can trigger alerts. To manage this, create exceptions for specific user accounts known to regularly modify this file for legitimate purposes.
- Automated scripts or tools that modify the init.coffee file as part of a legitimate configuration management process may cause false positives. Identify these processes and exclude them from the rule by adding their process names to the exception list.
- Non-malicious third-party Atom packages that require modifications to the init.coffee file for functionality can be mistaken for threats. Review and whitelist these packages if they are verified as safe and necessary for user workflows.
- System maintenance or administrative tasks performed by non-root users that involve changes to the init.coffee file might be flagged. Consider adding exceptions for these specific maintenance activities if they are routine and verified as non-threatening.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further execution of potentially malicious code.
- Review the contents of the `init.coffee` file to identify and document any unauthorized or suspicious code modifications.
- Remove any malicious code found in the `init.coffee` file and restore it to a known good state, either by reverting to a backup or by manually cleaning the file.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malware or persistence mechanisms.
- Change the credentials of the user account associated with the modified `init.coffee` file to prevent unauthorized access.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if other systems may be affected.
- Implement monitoring for future unauthorized changes to the `init.coffee` file and similar persistence mechanisms, enhancing detection capabilities to quickly identify and respond to similar threats.
