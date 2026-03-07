---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Netsh Helper DLL" prebuilt detection rule.
---

# Netsh Helper DLL

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Netsh Helper DLL

Netsh, a command-line utility in Windows, allows for network configuration and diagnostics. It supports extensibility through Helper DLLs, which can be added to enhance its capabilities. However, attackers can exploit this by adding malicious DLLs, ensuring their code runs whenever netsh is executed. The detection rule monitors registry changes related to netsh DLLs, flagging unauthorized modifications that may indicate persistence tactics.

### Possible investigation steps

- Review the registry path specified in the alert to confirm the presence of any unauthorized or suspicious DLLs under "HKLM\Software\Microsoft\netsh\".
- Check the timestamp of the registry change event to determine when the modification occurred and correlate it with any other suspicious activities or events on the system.
- Investigate the origin of the DLL file by examining its properties, such as the file path, creation date, and digital signature, to assess its legitimacy.
- Analyze recent user activity and scheduled tasks to identify any potential execution of netsh.exe that could have triggered the malicious DLL.
- Cross-reference the alert with other security logs and alerts from data sources like Microsoft Defender for Endpoint or Sysmon to gather additional context and identify any related threats or indicators of compromise.

### False positive analysis

- Legitimate software installations or updates may add or modify Netsh Helper DLLs, triggering the detection rule. Users should verify if recent installations or updates coincide with the registry changes.
- Network management tools or scripts used by IT departments might legitimately extend netsh functionality. Identify and document these tools to create exceptions in the detection rule.
- Scheduled tasks or administrative scripts that configure network settings could cause expected changes. Review scheduled tasks and scripts to ensure they are authorized and adjust the rule to exclude these known activities.
- Security software or network monitoring solutions may interact with netsh for legitimate purposes. Confirm with the software vendor if their product modifies netsh settings and consider excluding these changes from the rule.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further execution of the malicious DLL and potential lateral movement.
- Terminate any suspicious processes associated with netsh.exe to halt the execution of the malicious payload.
- Remove the unauthorized Netsh Helper DLL entry from the registry path identified in the alert to eliminate the persistence mechanism.
- Conduct a thorough scan of the affected system using an updated antivirus or endpoint detection and response (EDR) tool to identify and remove any additional malicious files or artifacts.
- Review and restore any altered system configurations to their original state to ensure system integrity.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for registry changes related to Netsh Helper DLLs to detect similar threats in the future.
