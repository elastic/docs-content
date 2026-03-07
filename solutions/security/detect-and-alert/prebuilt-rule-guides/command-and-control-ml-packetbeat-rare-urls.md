---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Web Request" prebuilt detection rule.
---

# Unusual Web Request

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Web Request
The 'Unusual Web Request' detection leverages machine learning to identify rare URLs that deviate from typical web activity, potentially signaling malicious actions like initial access or data exfiltration. Adversaries exploit trusted sites by embedding uncommon URLs for payload delivery or command-and-control. This rule flags such anomalies, aiding in early threat detection and response.

### Possible investigation steps

- Review the alert details to identify the specific rare URL that triggered the detection and note any associated IP addresses or domains.
- Check historical logs to determine if the rare URL has been accessed previously and identify any patterns or trends in its usage.
- Investigate the source of the request by examining the user agent, referrer, and originating IP address to assess whether it aligns with known legitimate traffic or appears suspicious.
- Analyze the destination of the URL to determine if it is associated with known malicious activity or if it has been flagged in threat intelligence databases.
- Correlate the unusual web request with other security events or alerts to identify potential connections to broader attack campaigns or ongoing threats.
- Assess the impacted systems or users to determine if there are any signs of compromise, such as unexpected processes, network connections, or data exfiltration attempts.
- Consider reaching out to the user or system owner to verify if the access to the rare URL was intentional and legitimate, providing additional context for the investigation.

### False positive analysis

- Web scraping tools and bots can trigger false positives by making requests to uncommon URLs as part of routine internet background traffic.
- Legitimate web scanning or enumeration activities by security teams may be flagged; these should be reviewed and whitelisted if verified as non-threatening.
- Automated processes or scripts that access rare URLs for legitimate business purposes can be excluded by identifying and documenting these activities.
- Frequent access to uncommon URLs by trusted internal applications or services should be monitored and added to exception lists to prevent unnecessary alerts.
- Regularly review and update the list of excluded URLs to ensure it reflects current legitimate activities and does not inadvertently allow malicious traffic.

### Response and remediation

- Isolate the affected system from the network to prevent further communication with the suspicious URL and potential data exfiltration.
- Conduct a thorough scan of the isolated system using updated antivirus and anti-malware tools to identify and remove any malicious payloads or software.
- Review and block the identified unusual URL at the network perimeter to prevent other systems from accessing it.
- Analyze network logs to identify any other systems that may have communicated with the suspicious URL and apply similar containment measures.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if the threat is part of a larger attack campaign.
- Implement enhanced monitoring for similar unusual web requests across the network to detect and respond to potential threats more quickly in the future.
- Review and update firewall and intrusion detection/prevention system (IDS/IPS) rules to better detect and block uncommon URLs associated with command-and-control activities.
