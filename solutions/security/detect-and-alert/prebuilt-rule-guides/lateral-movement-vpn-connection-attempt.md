---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Virtual Private Network Connection Attempt" prebuilt detection rule.'
---

# Virtual Private Network Connection Attempt

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Virtual Private Network Connection Attempt

Virtual Private Networks (VPNs) are used to securely connect to remote networks, encrypting data and masking IP addresses. Adversaries may exploit VPNs to move laterally within a network, gaining unauthorized access to systems. The detection rule identifies suspicious VPN connection attempts on macOS by monitoring specific command executions, helping to flag potential misuse for further investigation.

### Possible investigation steps

- Review the process details to confirm the legitimacy of the VPN connection attempt by examining the process name and arguments, such as "networksetup" with "-connectpppoeservice", "scutil" with "--nc start", or "osascript" with "osascript*set VPN to service*".
- Check the user account associated with the process to determine if the activity aligns with their typical behavior or if it appears suspicious.
- Investigate the source IP address and destination network to assess if the connection is to a known and trusted network or if it is unusual for the environment.
- Analyze historical data for similar VPN connection attempts from the same user or device to identify patterns or repeated unauthorized access attempts.
- Correlate the VPN connection attempt with other security events or alerts to identify potential lateral movement or further malicious activity within the network.

### False positive analysis

- Legitimate VPN usage by IT staff or network administrators may trigger the rule. To manage this, create exceptions for known user accounts or specific times when VPN maintenance is scheduled.
- Automated scripts or applications that use macOS built-in commands for VPN connections can cause false positives. Identify these scripts and whitelist their process names or command lines.
- Frequent VPN connections from trusted devices or IP addresses might be flagged. Exclude these devices or IPs from the rule to reduce noise.
- Users who frequently travel and connect to corporate networks via VPN may trigger alerts. Consider excluding these users or implementing a separate monitoring strategy for their activities.
- Regularly review and update the exclusion list to ensure it reflects current network policies and user behaviors, minimizing unnecessary alerts.

### Response and remediation

- Immediately isolate the affected macOS device from the network to prevent further lateral movement by the adversary.
- Terminate any suspicious VPN connections identified by the detection rule to cut off unauthorized access.
- Conduct a thorough review of the affected system's VPN configuration and logs to identify any unauthorized changes or connections.
- Reset credentials and update authentication methods for VPN access to ensure that compromised credentials are not reused.
- Escalate the incident to the security operations center (SOC) for further analysis and to determine if other systems have been affected.
- Implement additional monitoring on the network for unusual VPN connection attempts or related suspicious activities to enhance detection capabilities.
- Review and update VPN access policies to ensure they align with current security best practices and limit access to only necessary users and systems.
