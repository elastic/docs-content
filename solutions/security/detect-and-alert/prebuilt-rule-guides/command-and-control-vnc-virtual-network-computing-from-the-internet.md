---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "VNC (Virtual Network Computing) from the Internet" prebuilt detection rule.'
---

# VNC (Virtual Network Computing) from the Internet

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating VNC (Virtual Network Computing) from the Internet

VNC allows remote control of systems, facilitating maintenance and resource sharing. However, when exposed to the Internet, it becomes a target for attackers seeking unauthorized access. Adversaries exploit VNC for initial access or as a backdoor. The detection rule identifies suspicious VNC traffic by monitoring specific TCP ports and filtering out trusted IP ranges, flagging potential threats for further investigation.

### Possible investigation steps

- Review the source IP address of the alert to determine if it is from an untrusted or suspicious location, as the rule filters out known trusted IP ranges.
- Check the destination IP address to confirm it belongs to an internal network (10.0.0.0/8, 172.16.0.0/12, or 192.168.0.0/16) and verify if the system is authorized to receive VNC traffic.
- Analyze the network traffic logs for the specified TCP ports (5800-5810) to identify any unusual patterns or repeated access attempts that could indicate malicious activity.
- Investigate the context of the event by correlating it with other security alerts or logs to determine if there are signs of a broader attack or compromise.
- Assess the risk and impact of the potential threat by evaluating the criticality of the affected system and any sensitive data it may contain.

### False positive analysis

- Internal testing or maintenance activities may trigger the rule if VNC is used for legitimate purposes within a controlled environment. To manage this, create exceptions for known internal IP addresses that frequently use VNC for authorized tasks.
- Automated systems or scripts that utilize VNC for routine operations might be flagged. Identify these systems and exclude their IP addresses from the rule to prevent unnecessary alerts.
- Remote workers using VPNs that route traffic through public IPs could be mistakenly identified as threats. Ensure that VPN IP ranges are included in the trusted IP list to avoid false positives.
- Misconfigured network devices that inadvertently expose VNC ports to the Internet can cause alerts. Regularly audit network configurations to ensure VNC ports are not exposed and adjust the rule to exclude known safe configurations.
- Third-party service providers accessing systems via VNC for support purposes might be flagged. Establish a list of trusted IPs for these providers and update the rule to exclude them from detection.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any active VNC sessions originating from untrusted IP addresses to cut off potential attacker access.
- Conduct a thorough review of system logs and network traffic to identify any unauthorized changes or data access that may have occurred during the VNC session.
- Reset credentials for any accounts that were accessed or could have been compromised during the unauthorized VNC session.
- Apply security patches and updates to the VNC software and any other potentially vulnerable applications on the affected system.
- Implement network segmentation to ensure that VNC services are only accessible from trusted internal networks and not exposed to the Internet.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems may be affected.
