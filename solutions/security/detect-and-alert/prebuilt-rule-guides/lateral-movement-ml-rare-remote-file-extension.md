---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Remote File Extension" prebuilt detection rule.
---

# Unusual Remote File Extension

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Remote File Extension

The detection of unusual remote file extensions leverages machine learning to identify anomalies in file transfers, which may suggest lateral movement by adversaries. Attackers often exploit remote services to transfer files with uncommon extensions, bypassing standard security measures. This rule flags such anomalies, aiding in early detection of potential threats by correlating rare file extensions with known lateral movement tactics.

### Possible investigation steps

- Review the alert details to identify the specific file extension and the source and destination of the file transfer.
- Check the historical data for the identified file extension to determine if it has been used previously in legitimate activities or if it is indeed rare.
- Investigate the source host to identify any recent changes or suspicious activities, such as new user accounts or unusual login patterns.
- Examine the destination host for any signs of compromise or unauthorized access, focusing on recent file modifications or unexpected processes.
- Correlate the file transfer event with other security alerts or logs to identify potential patterns of lateral movement or exploitation of remote services.
- Consult threat intelligence sources to determine if the rare file extension is associated with known malware or adversary tactics.

### False positive analysis

- Common internal file transfers with rare extensions may trigger false positives. Review and whitelist known benign file extensions used by internal applications or processes.
- Automated backup or synchronization tools might use uncommon file extensions. Identify these tools and create exceptions for their typical file extensions to prevent unnecessary alerts.
- Development environments often generate files with unique extensions. Collaborate with development teams to understand these patterns and exclude them from detection if they are verified as non-threatening.
- Security tools or scripts that transfer diagnostic or log files with unusual extensions can be mistaken for lateral movement. Document these tools and adjust the rule to ignore their specific file extensions.
- Regularly review and update the list of excluded extensions to ensure it reflects current operational practices and does not inadvertently allow malicious activity.

### Response and remediation

- Isolate the affected host immediately to prevent further lateral movement and contain the potential threat.
- Review and terminate any suspicious remote sessions or connections identified on the host to cut off unauthorized access.
- Conduct a thorough scan of the affected system for malware or unauthorized software that may have been transferred using the unusual file extension.
- Restore the affected system from a known good backup if any malicious activity or compromise is confirmed.
- Update and patch all software and systems on the affected host to close any vulnerabilities that may have been exploited.
- Monitor network traffic for any further unusual file transfers or connections, focusing on rare file extensions and remote service exploitation patterns.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
