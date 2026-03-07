---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "RDP (Remote Desktop Protocol) from the Internet" prebuilt detection rule.
---

# RDP (Remote Desktop Protocol) from the Internet

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating RDP (Remote Desktop Protocol) from the Internet

RDP allows administrators to remotely manage systems, but exposing it to the internet poses security risks. Adversaries exploit RDP for unauthorized access, often using it as an entry point for attacks. The detection rule identifies suspicious RDP traffic by monitoring TCP connections on port 3389 from external IPs, flagging potential threats for further investigation.

### Possible investigation steps

- Review the source IP address flagged in the alert to determine if it is known or associated with any previous malicious activity. Check threat intelligence sources for any reported malicious behavior.
- Analyze the destination IP address to confirm it belongs to your internal network (10.0.0.0/8, 172.16.0.0/12, or 192.168.0.0/16) and identify the specific system targeted by the RDP connection.
- Examine network logs for any unusual or unexpected RDP traffic patterns from the source IP, such as repeated connection attempts or connections at odd hours, which may indicate brute force attempts or unauthorized access.
- Check for any recent changes or updates to firewall rules or security policies that might have inadvertently exposed RDP to the internet.
- Investigate the user accounts involved in the RDP session to ensure they are legitimate and have not been compromised. Look for any signs of unauthorized access or privilege escalation.
- Correlate the RDP traffic with other security events or alerts to identify any potential lateral movement or further malicious activity within the network.

### False positive analysis

- Internal testing or maintenance activities may trigger the rule if RDP is temporarily exposed to the internet. To manage this, create exceptions for known internal IP addresses or scheduled maintenance windows.
- Legitimate third-party vendors or partners accessing systems via RDP for support purposes can be mistaken for threats. Establish a list of trusted external IP addresses and exclude them from the rule.
- Misconfigured network devices or security tools might inadvertently expose RDP to the internet, leading to false positives. Regularly audit network configurations and update the rule to exclude known benign sources.
- Cloud-based services or remote work solutions that use RDP over the internet can be flagged. Identify and whitelist these services' IP ranges to prevent unnecessary alerts.

### Response and remediation

- Immediately block the external IP address identified in the alert from accessing the network to prevent further unauthorized RDP connections.
- Isolate the affected system from the network to contain any potential compromise and prevent lateral movement by the threat actor.
- Conduct a thorough review of the affected system for signs of compromise, such as unauthorized user accounts, changes in system configurations, or the presence of malware.
- Reset credentials for any accounts that were accessed or potentially compromised during the incident to prevent unauthorized access.
- Apply security patches and updates to the affected system and any other systems with RDP enabled to mitigate known vulnerabilities.
- Implement network segmentation to restrict RDP access to only trusted internal IP addresses and consider using a VPN for secure remote access.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are affected.
