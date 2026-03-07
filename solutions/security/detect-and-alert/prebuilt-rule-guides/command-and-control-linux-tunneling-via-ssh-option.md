---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Linux Tunneling and/or Port Forwarding via SSH Option" prebuilt detection rule.
---

# Potential Linux Tunneling and/or Port Forwarding via SSH Option

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Linux Tunneling and/or Port Forwarding via SSH Option

SSH is a secure protocol used for encrypted communication over networks, often employed for remote administration. Adversaries exploit SSH options like port forwarding to create tunnels, facilitating covert data exfiltration or unauthorized access. The detection rule identifies suspicious SSH commands indicative of tunneling by monitoring specific SSH options, helping to flag potential misuse for further investigation.

### Possible investigation steps

- Review the process command line details to identify the specific SSH options used, such as ProxyCommand, LocalForward, RemoteForward, DynamicForward, Tunnel, GatewayPorts, ExitOnForwardFailure, or ProxyJump, to understand the nature of the potential tunneling or port forwarding.
- Examine the user account associated with the SSH process to determine if the activity aligns with their typical behavior or if it appears suspicious.
- Check the source and destination IP addresses involved in the SSH connection to identify any unusual or unauthorized endpoints that may indicate malicious activity.
- Investigate the timing and frequency of the SSH connections to assess whether they coincide with known business operations or if they suggest unauthorized access patterns.
- Correlate the event with other security logs or alerts from the same host or network segment to identify any additional indicators of compromise or related suspicious activities.

### False positive analysis

- Legitimate administrative tasks using SSH options like ProxyCommand or LocalForward can trigger the rule. To manage this, create exceptions for known administrative scripts or users frequently using these options for valid purposes.
- Automated backup or synchronization processes that use SSH tunneling for secure data transfer may be flagged. Identify these processes and exclude them by specifying the associated process names or user accounts.
- Development or testing environments where developers use SSH tunneling for accessing remote services might cause alerts. Implement exceptions for specific IP addresses or user groups associated with these environments.
- Monitoring or logging tools that utilize SSH for secure data collection can be mistaken for malicious activity. Whitelist these tools by their process names or command-line patterns to prevent false positives.
- Internal network services that rely on SSH port forwarding for legitimate communication should be reviewed and excluded based on their known behavior and usage patterns.

### Response and remediation

- Immediately isolate the affected Linux system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious SSH sessions identified by the detection rule to halt potential tunneling or port forwarding activities.
- Conduct a thorough review of SSH configuration files and logs on the affected system to identify unauthorized changes or access patterns.
- Reset credentials for any accounts that were used in the suspicious SSH activity to prevent further unauthorized access.
- Implement network segmentation to limit SSH access to only necessary systems and services, reducing the risk of lateral movement.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are compromised.
- Enhance monitoring and logging of SSH activities across the network to detect similar threats in the future, ensuring alerts are promptly reviewed and acted upon.

