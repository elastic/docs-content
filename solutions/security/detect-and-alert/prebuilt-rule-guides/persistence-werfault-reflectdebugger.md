---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Werfault ReflectDebugger Persistence" prebuilt detection rule.'
---

# Werfault ReflectDebugger Persistence

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Werfault ReflectDebugger Persistence

Werfault, the Windows Error Reporting service, can be manipulated by attackers to maintain persistence. By registering a ReflectDebugger, adversaries can execute malicious code whenever Werfault is triggered with specific parameters. The detection rule monitors registry changes in key paths associated with ReflectDebugger, alerting on unauthorized modifications indicative of potential abuse.

### Possible investigation steps

- Review the registry change event details to identify the specific path modified, focusing on the paths listed in the query: "HKLM\Software\Microsoft\Windows\Windows Error Reporting\Hangs\ReflectDebugger", "\REGISTRY\MACHINE\Software\Microsoft\Windows\Windows Error Reporting\Hangs\ReflectDebugger", or "MACHINE\Software\Microsoft\Windows\Windows Error Reporting\Hangs\ReflectDebugger".
- Check the timestamp of the registry change event to determine when the modification occurred and correlate it with other suspicious activities or events on the system around the same time.
- Investigate the user account or process responsible for the registry change to assess whether it is a legitimate action or potentially malicious. Look for unusual or unauthorized accounts making the change.
- Examine the system for any recent executions of Werfault with the "-pr" parameter, as this could indicate attempts to trigger the malicious payload.
- Search for any related alerts or logs from data sources such as Elastic Endgame, Elastic Defend, Microsoft Defender for Endpoint, SentinelOne, or Sysmon that might provide additional context or corroborate the suspicious activity.
- Assess the system for any signs of compromise or persistence mechanisms, such as unexpected startup items, scheduled tasks, or other registry modifications that could indicate a broader attack.

### False positive analysis

- Legitimate software installations or updates may modify the ReflectDebugger registry key as part of their error reporting configuration. Users can create exceptions for known software vendors by verifying the digital signature of the executable associated with the change.
- System administrators may intentionally configure the ReflectDebugger for debugging purposes. Document and whitelist these changes in the security monitoring system to prevent unnecessary alerts.
- Automated system maintenance tools might interact with the ReflectDebugger registry key. Identify and exclude these tools by correlating the registry changes with scheduled maintenance activities.
- Security software or endpoint protection solutions may alter the ReflectDebugger settings as part of their protective measures. Confirm these changes with the security vendor and add them to the exclusion list if deemed safe.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further execution of malicious code via the Werfault ReflectDebugger.
- Terminate any suspicious processes associated with Werfault that are running with the "-pr" parameter to halt potential malicious activity.
- Remove unauthorized entries from the registry path "HKLM\Software\Microsoft\Windows\Windows Error Reporting\Hangs\ReflectDebugger" to eliminate persistence mechanisms.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection tools to identify and remove any additional malware or malicious artifacts.
- Review and restore any system or application configurations that may have been altered by the attacker to their original state.
- Escalate the incident to the security operations team for further analysis and to determine if additional systems are affected.
- Implement enhanced monitoring and alerting for registry changes in the specified paths to detect and respond to similar threats in the future.
