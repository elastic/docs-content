---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious SolarWinds Child Process" prebuilt detection rule.'
---

# Suspicious SolarWinds Child Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious SolarWinds Child Process

SolarWinds is a widely used IT management software that operates critical network and system monitoring functions. Adversaries may exploit its trusted processes to execute unauthorized programs, leveraging its elevated privileges to bypass security controls. The detection rule identifies unusual child processes spawned by SolarWinds' core services, excluding known legitimate operations, to flag potential malicious activity.

### Possible investigation steps

- Review the details of the triggered alert to identify the specific child process name and executable path that caused the alert.
- Check the parent process details, specifically SolarWinds.BusinessLayerHost.exe or SolarWinds.BusinessLayerHostx64.exe, to confirm its legitimacy and ensure it is running from the expected directory.
- Investigate the child process's code signature to determine if it is trusted or if there are any anomalies in the signature that could indicate tampering.
- Analyze the historical activity of the suspicious child process on the host to identify any patterns or previous instances of execution that could provide context.
- Correlate the suspicious process activity with other security events or logs from the same host to identify any related malicious behavior or indicators of compromise.
- Consult threat intelligence sources to determine if the suspicious process or executable path is associated with known malware or adversary techniques.

### False positive analysis

- Legitimate SolarWinds updates or patches may trigger the rule. Ensure that the process code signature is verified as trusted and matches known update signatures.
- Custom scripts or tools integrated with SolarWinds for automation purposes might be flagged. Review these processes and add them to the exclusion list if they are verified as safe and necessary for operations.
- Third-party plugins or extensions that interact with SolarWinds could be misidentified. Validate these plugins and consider excluding them if they are from a trusted source and essential for functionality.
- Scheduled tasks or maintenance activities that involve SolarWinds processes may appear suspicious. Confirm these tasks are part of regular operations and exclude them if they are consistent with expected behavior.
- Temporary diagnostic or troubleshooting tools used by IT staff might be detected. Ensure these tools are authorized and add them to the exclusion list if they are frequently used and pose no threat.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious child processes identified that are not part of the known legitimate operations list, ensuring that no malicious programs continue to execute.
- Conduct a thorough review of the affected system's recent activity logs to identify any additional indicators of compromise or unauthorized changes.
- Restore the affected system from a known good backup to ensure that any potential malware or unauthorized changes are removed.
- Update all SolarWinds software and related components to the latest versions to patch any known vulnerabilities that could be exploited.
- Implement enhanced monitoring on the affected system and similar environments to detect any recurrence of suspicious activity, focusing on unusual child processes spawned by SolarWinds services.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if broader organizational impacts need to be addressed.
