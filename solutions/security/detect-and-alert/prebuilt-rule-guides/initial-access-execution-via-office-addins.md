---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Execution via Microsoft Office Add-Ins" prebuilt detection rule.
---

# Suspicious Execution via Microsoft Office Add-Ins

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Execution via Microsoft Office Add-Ins

Microsoft Office Add-Ins enhance productivity by integrating additional features into Office applications. However, adversaries can exploit this by embedding malicious code within add-ins, often delivered through phishing. The detection rule identifies unusual execution patterns, such as Office apps launching add-ins from suspicious paths or with atypical parent processes, signaling potential threats. It filters out known benign activities to minimize false positives, focusing on genuine anomalies indicative of malicious intent.

### Possible investigation steps

- Review the process name and arguments to confirm if the execution involves a Microsoft Office application launching an add-in from a suspicious path, as indicated by the process.name and process.args fields.
- Check the parent process name to determine if the Office application was launched by an unusual or potentially malicious parent process, such as cmd.exe or powershell.exe, using the process.parent.name field.
- Investigate the file path from which the add-in was executed to assess if it matches any of the suspicious paths listed in the query, such as the Temp or Downloads directories, using the process.args field.
- Examine the host's recent activity logs to identify any related events or patterns that might indicate a broader attack or compromise, focusing on the host.os.type and event.type fields.
- Correlate the alert with any recent phishing attempts or suspicious emails received by the user to determine if the execution is part of a phishing campaign, leveraging the MITRE ATT&CK tactic and technique information provided.
- Verify if the execution is a false positive by checking against the known benign activities excluded in the query, such as specific VSTOInstaller.exe paths or arguments, to rule out legitimate software installations or updates.

### False positive analysis

- Logitech software installations can trigger false positives when VSTO files are executed by Logitech's PlugInInstallerUtility. To mitigate this, exclude processes with paths related to Logitech installations from the detection rule.
- The VSTOInstaller.exe process may be flagged when uninstalling applications. Exclude processes with the /Uninstall argument to prevent these false positives.
- Rundll32.exe executing with specific arguments related to MSI temporary files can be benign. Exclude these specific rundll32.exe executions to avoid false alerts.
- Sidekick.vsto installations from the specified URL can be legitimate. Exclude this specific VSTOInstaller.exe process with the Sidekick.vsto argument to reduce false positives.

### Response and remediation

- Isolate the affected system from the network to prevent further spread of the potential threat and to contain any ongoing malicious activity.
- Terminate any suspicious processes identified by the detection rule, such as those involving unusual parent processes or originating from suspicious paths.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any malicious add-ins or related malware.
- Review and clean up any unauthorized or suspicious Office add-ins from the affected applications to ensure no malicious code remains.
- Restore the system from a known good backup if the integrity of the system is compromised and cannot be assured through cleaning alone.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement additional monitoring and alerting for similar suspicious activities to enhance detection and response capabilities for future incidents.
