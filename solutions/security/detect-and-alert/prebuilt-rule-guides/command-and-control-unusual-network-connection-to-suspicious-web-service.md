---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Network Connection to Suspicious Web Service" prebuilt detection rule.'
---

# Unusual Network Connection to Suspicious Web Service

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Network Connection to Suspicious Web Service

In macOS environments, network connections to web services are routine for data sharing and collaboration. However, adversaries exploit these services for command and control by disguising malicious traffic as legitimate. The detection rule identifies unusual outbound connections to known suspicious domains, flagging potential misuse by monitoring specific domain patterns and connection events, thus aiding in early threat detection.

### Possible investigation steps

- Review the destination domain and process executable from the alert to determine if it matches any expected web service communication.
- Check the event.category and event.type fields to confirm the nature of the network connection and ensure it aligns with the expected behavior of a macOS system.
- Investigate the source host identified by host.os.type to gather information about its recent activities, installed applications, and any potential indicators of compromise.
- Analyze network traffic logs for the source host to identify any other unusual or suspicious outbound connections that may indicate a broader compromise.
- Correlate the alert with other security events or alerts from the same host or network segment to identify patterns or related incidents.
- Consult threat intelligence sources to gather additional context on the flagged domain and assess its reputation and history of malicious activity.

### False positive analysis

- Frequent access to legitimate cloud storage services like Google Drive or Dropbox for routine file sharing can trigger false positives. Users can create exceptions for specific domains or IP addresses known to be safe and frequently accessed by their organization.
- Automated backup services that use domains such as OneDrive or SharePoint may be flagged. To mitigate this, identify and whitelist the specific services or applications that are part of regular backup operations.
- Collaboration tools like Slack or Discord, used for legitimate communication, might be mistakenly flagged. Users should review and whitelist these domains if they are part of standard business operations.
- URL shorteners like bit.ly or tinyurl.com used in marketing or communication campaigns can cause false alerts. Establish a list of trusted shortener services and exclude them from monitoring if they are regularly used by the organization.
- Development and testing environments using services like ngrok or localtunnel for temporary public URLs can be misidentified. Ensure these environments are documented and excluded from the rule if they are part of normal development workflows.

### Response and remediation

- Immediately isolate the affected macOS device from the network to prevent further communication with the suspicious domains.
- Conduct a thorough review of the network logs to identify any data exfiltration attempts or additional suspicious connections originating from the isolated device.
- Remove any unauthorized or suspicious applications or scripts found on the device that may be facilitating the outbound connections.
- Update the device's security software and perform a full system scan to detect and remove any malware or unauthorized software.
- Reset credentials and review access permissions for the affected user accounts to prevent unauthorized access.
- Monitor the network for any further attempts to connect to the flagged domains and ensure that alerts are configured to notify security teams of any recurrence.
- Escalate the incident to the security operations center (SOC) or relevant cybersecurity team for further investigation and to determine if the threat is part of a larger attack campaign.
