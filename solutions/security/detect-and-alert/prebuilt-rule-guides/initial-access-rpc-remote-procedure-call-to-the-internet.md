---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "RPC (Remote Procedure Call) to the Internet" prebuilt detection rule.
---

# RPC (Remote Procedure Call) to the Internet

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating RPC (Remote Procedure Call) to the Internet

RPC enables remote management and resource sharing across networks, crucial for system administration. However, when exposed to the Internet, it becomes a target for attackers seeking initial access or backdoor entry. The detection rule identifies suspicious RPC traffic from internal IPs to external networks, flagging potential exploitation attempts by monitoring specific ports and IP ranges.

### Possible investigation steps

- Review the source IP address from the alert to identify the internal system initiating the RPC traffic. Check if this IP belongs to a known or authorized device within the network.
- Examine the destination IP address to determine if it is a known or suspicious external entity. Use threat intelligence sources to assess if the IP has been associated with malicious activity.
- Analyze the network traffic logs for the specific event.dataset values (network_traffic.flow or zeek.dce_rpc) to gather more context about the nature and volume of the RPC traffic.
- Investigate the destination port, specifically port 135, to confirm if the traffic is indeed RPC-related and assess if there are any legitimate reasons for this communication.
- Check for any recent changes or anomalies in the network configuration or system settings of the source IP that might explain the unexpected RPC traffic.
- Correlate this alert with other security events or logs to identify any patterns or additional indicators of compromise that might suggest a broader attack campaign.

### False positive analysis

- Internal testing environments may generate RPC traffic to external IPs for legitimate purposes. Identify and document these environments, then create exceptions in the detection rule to prevent unnecessary alerts.
- Cloud-based services or applications that require RPC communication for integration or management might trigger false positives. Review these services and whitelist their IP addresses if they are verified as non-threatening.
- VPN or remote access solutions that use RPC for secure connections can be mistaken for suspicious activity. Ensure that the IP ranges of these solutions are excluded from the rule to avoid false alerts.
- Automated backup or synchronization tools that use RPC to communicate with external servers could be flagged. Verify these tools and add their destination IPs to an exception list if they are part of routine operations.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Conduct a thorough analysis of the affected system to identify any unauthorized changes or installed backdoors, focusing on processes and services related to RPC.
- Revoke any compromised credentials and enforce a password reset for all accounts that may have been accessed or used during the incident.
- Apply necessary patches and updates to the affected system and any other systems with similar vulnerabilities to mitigate the risk of exploitation.
- Monitor network traffic for any signs of lateral movement or additional suspicious activity, particularly focusing on RPC-related traffic.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced logging and monitoring for RPC traffic to detect and respond to similar threats more effectively in the future.
