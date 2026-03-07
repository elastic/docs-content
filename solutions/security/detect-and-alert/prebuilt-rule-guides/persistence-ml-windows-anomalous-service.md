---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Windows Service" prebuilt detection rule.
---

# Unusual Windows Service

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Windows Service

Windows services are crucial for running background processes and applications. Adversaries exploit this by creating or modifying services to maintain persistence or execute unauthorized actions. The 'Unusual Windows Service' detection rule leverages machine learning to identify atypical services, flagging potential threats by comparing against known service patterns, thus aiding in early threat detection and response.

### Possible investigation steps

- Review the details of the detected unusual Windows service, including the service name, path, and any associated executables, to determine if it aligns with known legitimate services or appears suspicious.
- Check the creation and modification timestamps of the service to identify if it was recently added or altered, which could indicate unauthorized activity.
- Investigate the user account under which the service is running to assess if it has the necessary permissions and if the account has been compromised or misused.
- Cross-reference the service with known threat intelligence databases to see if it matches any known malware or persistence mechanisms.
- Analyze the network activity and connections associated with the service to identify any unusual or unauthorized communication patterns.
- Examine the host's event logs for any related entries that could provide additional context or evidence of malicious activity, such as failed login attempts or privilege escalation events.

### False positive analysis

- Legitimate software installations or updates may create new services that are flagged as unusual. Users should verify the source and purpose of the service before excluding it.
- Custom in-house applications often run unique services that can trigger alerts. Document these services and create exceptions to prevent future false positives.
- IT administrative tools might install services for management purposes. Confirm these tools are authorized and add them to an exception list if they are frequently flagged.
- Temporary services used for troubleshooting or testing can be mistaken for threats. Ensure these are removed after use or excluded if they are part of regular operations.
- Scheduled tasks that create services for specific operations might be flagged. Review these tasks and exclude them if they are part of normal business processes.

### Response and remediation

- Immediately isolate the affected host from the network to prevent potential lateral movement or data exfiltration by the unauthorized service.
- Terminate the unusual Windows service identified by the alert to stop any ongoing malicious activity.
- Conduct a thorough analysis of the service's executable and associated files to determine if they are malicious. Use endpoint detection and response (EDR) tools to assist in this analysis.
- Remove any malicious files or executables associated with the service from the system to ensure complete eradication of the threat.
- Restore the affected system from a known good backup if the service has caused significant changes or damage to the system.
- Monitor the system and network for any signs of re-infection or similar unusual service activity, using enhanced logging and alerting mechanisms.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to assess the need for broader organizational response measures.
