---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Authorization Plugin Modification" prebuilt detection rule.'
---

# Authorization Plugin Modification

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Authorization Plugin Modification

Authorization plugins in macOS extend authentication capabilities, enabling features like third-party multi-factor authentication. Adversaries may exploit these plugins to maintain persistence or capture credentials by modifying or adding unauthorized plugins. The detection rule identifies suspicious modifications by monitoring changes in specific plugin directories, excluding known legitimate plugins and trusted processes, thus highlighting potential unauthorized activities.

### Possible investigation steps

- Review the file path of the modified plugin to determine if it is located in the /Library/Security/SecurityAgentPlugins/ directory and verify if it is not among the known legitimate plugins like KandjiPassport.bundle or TeamViewerAuthPlugin.bundle.
- Examine the process name associated with the modification event to ensure it is not 'shove' with a trusted code signature, as these are excluded from the detection rule.
- Investigate the history of the modified plugin file to identify when it was created or last modified and by which user or process, to assess if the change aligns with expected administrative activities.
- Check for any recent user logon events that might correlate with the timing of the plugin modification to identify potential unauthorized access attempts.
- Analyze any associated network activity or connections from the host around the time of the modification to detect possible data exfiltration or communication with external command and control servers.
- Review system logs for any other suspicious activities or anomalies that occurred around the same time as the plugin modification to gather additional context on the potential threat.

### False positive analysis

- Known legitimate plugins such as KandjiPassport.bundle and TeamViewerAuthPlugin.bundle may trigger alerts if they are updated or modified. Users can handle these by ensuring these plugins are included in the exclusion list within the detection rule.
- Trusted processes like those signed by a verified code signature, such as the process named 'shove', might be flagged if they interact with the plugin directories. Users should verify the code signature and add these processes to the trusted list to prevent false positives.
- System updates or legitimate software installations may cause temporary changes in the plugin directories. Users should monitor for these events and temporarily adjust the detection rule to exclude these known activities during the update period.
- Custom or in-house developed plugins that are not widely recognized may be flagged. Users should ensure these plugins are properly documented and added to the exclusion list if they are verified as safe and necessary for business operations.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent potential lateral movement or further unauthorized access.
- Review and terminate any suspicious processes associated with unauthorized plugins, especially those not signed by a trusted code signature.
- Remove any unauthorized or suspicious plugins from the /Library/Security/SecurityAgentPlugins/ directory to eliminate persistence mechanisms.
- Conduct a thorough credential audit for any accounts that may have been compromised, and enforce a password reset for affected users.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Implement additional monitoring on the affected system and similar endpoints to detect any further unauthorized plugin modifications.
- Review and update security policies to ensure only authorized personnel can modify or add authorization plugins, and consider implementing stricter access controls.
