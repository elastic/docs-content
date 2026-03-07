---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Network Connection to Suspicious Top Level Domain" prebuilt detection rule.'
---

# Unusual Network Connection to Suspicious Top Level Domain

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Network Connection to Suspicious Top Level Domain

In macOS environments, network connections are essential for communication and data exchange. Adversaries exploit this by connecting to suspicious top-level domains (TLDs) for command and control activities. The detection rule identifies unusual outbound connections to these TLDs, signaling potential threats. By monitoring specific domains, it helps detect and mitigate malicious activities early.

### Possible investigation steps

- Review the destination domain involved in the alert to determine if it is associated with known malicious activities or if it has been flagged in threat intelligence databases.
- Analyze the network traffic details related to the connection, including the source IP address and the volume of data transferred, to assess the nature and intent of the communication.
- Check the host system's recent activity logs for any unusual processes or applications that initiated the network connection, focusing on the event.type "start" to identify the triggering process.
- Investigate the user account associated with the host to determine if there have been any unauthorized access attempts or anomalies in user behavior.
- Correlate the alert with other security events or alerts from the same host or network segment to identify potential patterns or coordinated activities.
- Consult with threat intelligence sources or security forums to gather additional context on the specific top-level domain and its potential use in command and control operations.

### False positive analysis

- Legitimate business domains may use TLDs like .online or .store for marketing purposes. Review the domain's reputation and business context before marking it as a threat.
- Personal or small business websites might use TLDs such as .fun or .life. Verify the domain ownership and usage to determine if it is a false positive.
- Some educational or community projects might use TLDs like .club or .space. Check the domain's content and purpose to assess its legitimacy.
- Exclude known safe domains by adding them to an allowlist in your monitoring tool to prevent repeated false positives.
- Regularly update the allowlist based on user feedback and network behavior analysis to ensure it remains accurate and effective.

### Response and remediation

- Immediately isolate the affected macOS device from the network to prevent further communication with the suspicious domain.
- Conduct a thorough review of the network logs to identify any additional devices that may have communicated with the same suspicious domains and isolate them if necessary.
- Use endpoint security tools to perform a full malware scan on the affected device to identify and remove any malicious software.
- Reset credentials and review access permissions for any accounts that were active on the affected device to prevent unauthorized access.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if the threat is part of a larger attack campaign.
- Implement network-level blocking of the identified suspicious domains to prevent future connections from any device within the network.
- Review and update firewall and intrusion detection/prevention system (IDS/IPS) rules to enhance detection and blocking of similar threats in the future.
