---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "IPv4/IPv6 Forwarding Activity" prebuilt detection rule.
---

# IPv4/IPv6 Forwarding Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating IPv4/IPv6 Forwarding Activity

IPv4/IPv6 forwarding allows a Linux system to route traffic between network interfaces, facilitating network communication. While essential for legitimate network operations, adversaries can exploit this capability to pivot across networks, exfiltrate data, or maintain control channels. The detection rule identifies suspicious command executions that enable IP forwarding, focusing on specific command patterns and processes, thus highlighting potential misuse.

### Possible investigation steps

- Review the process command line details to understand the context in which IP forwarding was enabled, focusing on the specific command patterns identified in the alert.
- Identify the parent process of the suspicious command execution using the process.parent.executable field to determine if it was initiated by a legitimate or potentially malicious process.
- Check the user account associated with the process execution to assess if the action was performed by an authorized user or if there are signs of compromised credentials.
- Investigate recent network activity on the host to identify any unusual traffic patterns or connections that could indicate data exfiltration or lateral movement.
- Correlate the alert with other security events or logs from the same host or network segment to identify any related suspicious activities or patterns.
- Assess the system's current configuration and network topology to determine if enabling IP forwarding could have been part of a legitimate administrative task or if it poses a security risk.

### False positive analysis

- Routine administrative tasks may trigger the rule when system administrators enable IP forwarding for legitimate network configuration purposes. To manage this, create exceptions for known administrative scripts or processes that regularly perform these actions.
- Automated scripts or configuration management tools like Ansible or Puppet might execute commands that match the rule's criteria. Identify these tools and exclude their processes from the rule to prevent false alerts.
- Network testing or troubleshooting activities often require temporary enabling of IP forwarding. Document and exclude these activities when performed by trusted users or during scheduled maintenance windows.
- Virtualization or container orchestration platforms may enable IP forwarding as part of their normal operations. Recognize these platforms and adjust the rule to ignore their specific processes or command patterns.
- Security tools or network monitoring solutions might also enable IP forwarding for analysis purposes. Verify these tools and exclude their processes to avoid unnecessary alerts.

### Response and remediation

- Immediately isolate the affected Linux system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified by the detection rule, particularly those enabling IP forwarding, to halt potential lateral movement or data exfiltration.
- Conduct a thorough review of network traffic logs to identify any unusual or unauthorized connections that may indicate command and control activity.
- Revert any unauthorized changes to system configurations, specifically those related to IP forwarding settings, to restore the system to its secure state.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are compromised.
- Implement network segmentation to limit the ability of attackers to pivot between networks in the future.
- Enhance monitoring and alerting for similar suspicious activities by tuning detection systems to recognize patterns associated with IP forwarding misuse.
