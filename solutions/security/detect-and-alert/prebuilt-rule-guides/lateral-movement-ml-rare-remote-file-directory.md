---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Remote File Directory" prebuilt detection rule.'
---

# Unusual Remote File Directory

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Remote File Directory

The 'Unusual Remote File Directory' detection leverages machine learning to identify atypical file transfers in directories not commonly monitored, which may indicate lateral movement by adversaries. Attackers exploit these less scrutinized paths to evade detection, often using remote services to transfer malicious payloads. This rule flags such anomalies, aiding in early detection of potential breaches.

### Possible investigation steps

- Review the alert details to identify the specific unusual directory involved in the file transfer and note any associated file names or types.
- Check the source and destination IP addresses involved in the transfer to determine if they are known or trusted entities within the network.
- Investigate the user account associated with the file transfer to verify if the activity aligns with their typical behavior or role within the organization.
- Examine recent logs or events from the host to identify any other suspicious activities or anomalies that may correlate with the file transfer.
- Cross-reference the detected activity with known threat intelligence sources to determine if the file transfer or directory is associated with any known malicious campaigns or tactics.
- Assess the potential impact of the file transfer by evaluating the sensitivity of the data involved and the criticality of the systems affected.

### False positive analysis

- Routine administrative tasks may trigger alerts if they involve file transfers to directories not typically monitored. Users can create exceptions for known administrative activities to prevent unnecessary alerts.
- Automated backup processes might be flagged if they store files in uncommon directories. Identifying and excluding these backup operations can reduce false positives.
- Software updates or patches that deploy files to less common directories could be mistaken for suspicious activity. Users should whitelist these update processes to avoid false alerts.
- Development or testing environments often involve file transfers to non-standard directories. Users can configure exceptions for these environments to minimize false positives.
- Legitimate remote services used for file transfers, such as cloud storage synchronization, may be flagged. Users should identify and exclude these trusted services from monitoring.

### Response and remediation

- Isolate the affected host immediately to prevent further lateral movement and contain the potential threat. Disconnect it from the network to stop any ongoing malicious activity.
- Conduct a thorough analysis of the unusual directory and any files transferred to identify malicious payloads. Use endpoint detection and response (EDR) tools to scan for known malware signatures and behaviors.
- Remove any identified malicious files and artifacts from the affected directory and host. Ensure that all traces of the threat are eradicated to prevent re-infection.
- Reset credentials and review access permissions for the affected host and any associated accounts to mitigate the risk of unauthorized access. Ensure that least privilege principles are enforced.
- Monitor network traffic and logs for any signs of further lateral movement or exploitation attempts. Pay special attention to remote service connections and unusual directory access.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional hosts or systems are compromised.
- Update detection mechanisms and rules to enhance monitoring of less common directories and improve the detection of similar threats in the future.
