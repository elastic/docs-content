---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "UAC Bypass via ICMLuaUtil Elevated COM Interface" prebuilt detection rule.'
---

# UAC Bypass via ICMLuaUtil Elevated COM Interface

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating UAC Bypass via ICMLuaUtil Elevated COM Interface

The ICMLuaUtil Elevated COM Interface is a Windows component that facilitates User Account Control (UAC) operations, allowing certain processes to execute with elevated privileges. Adversaries exploit this by invoking the interface to bypass UAC, executing malicious code stealthily. The detection rule identifies such attempts by monitoring processes initiated by `dllhost.exe` with specific arguments, excluding legitimate processes like `WerFault.exe`, thus flagging potential privilege escalation activities.

### Possible investigation steps

- Review the process tree to identify the parent and child processes of the flagged `dllhost.exe` instance to understand the context of its execution.
- Examine the command-line arguments of the `dllhost.exe` process to confirm the presence of the suspicious `/Processid:{3E5FC7F9-9A51-4367-9063-A120244FBEC7}` or `/Processid:{D2E7041B-2927-42FB-8E9F-7CE93B6DC937}` arguments.
- Check for any recent changes or installations on the system that might have introduced the suspicious behavior, focusing on software that might interact with UAC settings.
- Investigate the user account under which the `dllhost.exe` process was executed to determine if it has been compromised or if it has elevated privileges.
- Correlate the event with other security logs or alerts from data sources like Sysmon or Microsoft Defender for Endpoint to identify any related suspicious activities or patterns.
- Assess the network activity of the affected system around the time of the alert to detect any potential data exfiltration or communication with known malicious IP addresses.

### False positive analysis

- Legitimate software updates or installations may trigger the rule if they use the ICMLuaUtil Elevated COM Interface for necessary elevation. Users can monitor the specific software involved and create exceptions for trusted applications.
- System maintenance tasks initiated by IT administrators might use similar processes for legitimate purposes. Identifying these tasks and excluding them from the rule can reduce false positives.
- Certain enterprise applications may require elevated privileges and use the same COM interface. Regularly review and whitelist these applications to prevent unnecessary alerts.
- Automated scripts or tools used for system management that invoke the interface should be evaluated. If deemed safe, they can be added to an exclusion list to avoid repeated false positives.
- Regularly update the list of excluded processes to reflect changes in the organization's software environment, ensuring that only non-threatening behaviors are excluded.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Terminate any suspicious processes initiated by `dllhost.exe` with the specified arguments to stop the execution of potentially malicious code.
- Conduct a thorough review of the affected system to identify any unauthorized changes or additional malicious files, and remove them.
- Restore the system from a known good backup if any critical system files or configurations have been altered.
- Update and patch the operating system and all installed software to mitigate any known vulnerabilities that could be exploited for UAC bypass.
- Implement application whitelisting to prevent unauthorized applications from executing, focusing on blocking the execution of `dllhost.exe` with suspicious arguments.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to assess the potential impact on the broader network.
