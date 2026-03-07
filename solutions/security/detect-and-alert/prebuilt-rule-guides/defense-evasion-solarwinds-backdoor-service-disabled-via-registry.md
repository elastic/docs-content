---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "SolarWinds Process Disabling Services via Registry" prebuilt detection rule.'
---

# SolarWinds Process Disabling Services via Registry

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating SolarWinds Process Disabling Services via Registry

SolarWinds software is integral for network management, often requiring deep system access. Adversaries may exploit this by altering registry settings to disable critical services, evading detection. The detection rule identifies changes to service start types by specific SolarWinds processes, flagging potential misuse aimed at disabling security defenses. This proactive monitoring helps mitigate risks associated with unauthorized registry modifications.

### Possible investigation steps

- Review the process name involved in the alert to confirm it matches one of the specified SolarWinds processes, such as "SolarWinds.BusinessLayerHost*.exe" or "NetFlowService*.exe".
- Examine the registry path in the alert to ensure it corresponds to the critical service start type locations, such as "HKLM\\SYSTEM\\*ControlSet*\\Services\\*\\Start".
- Check the registry data value to verify if it has been set to "4" (disabled), indicating a potential attempt to disable a service.
- Investigate the timeline of the registry change event to identify any preceding or subsequent suspicious activities on the host.
- Correlate the alert with other security logs or alerts from data sources like Sysmon or Microsoft Defender for Endpoint to identify any related malicious activities or patterns.
- Assess the impacted service to determine its role in security operations and evaluate the potential impact of it being disabled.
- Contact the system owner or administrator to verify if the registry change was authorized or part of a legitimate maintenance activity.

### False positive analysis

- Routine updates or maintenance by SolarWinds software may trigger registry changes. Verify if the process corresponds to a scheduled update or maintenance task and consider excluding these specific processes during known maintenance windows.
- Legitimate configuration changes by IT administrators using SolarWinds tools can appear as registry modifications. Confirm with the IT team if the changes align with authorized configuration activities and create exceptions for these known activities.
- Automated scripts or tools that utilize SolarWinds processes for legitimate network management tasks might cause false positives. Review the scripts or tools in use and whitelist them if they are verified as safe and necessary for operations.
- Temporary service modifications for troubleshooting purposes by SolarWinds processes can be mistaken for malicious activity. Ensure that any troubleshooting activities are documented and create temporary exceptions during these periods.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized registry modifications and potential lateral movement by the adversary.
- Terminate any suspicious SolarWinds processes identified in the alert, such as "SolarWinds.BusinessLayerHost*.exe" or "NetFlowService*.exe", to halt any ongoing malicious activity.
- Restore the registry settings for the affected services to their original state, ensuring that critical security services are re-enabled and configured to start automatically.
- Conduct a thorough review of the affected system for additional signs of compromise, including unauthorized user accounts, scheduled tasks, or other persistence mechanisms.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine the scope of the breach.
- Implement enhanced monitoring on the affected system and similar environments to detect any future unauthorized registry changes, leveraging data sources like Sysmon and Microsoft Defender for Endpoint.
- Review and update access controls and permissions for SolarWinds processes to limit their ability to modify critical system settings, reducing the risk of future exploitation.
