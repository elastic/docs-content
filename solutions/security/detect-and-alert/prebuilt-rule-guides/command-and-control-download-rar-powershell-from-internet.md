---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Roshal Archive (RAR) or PowerShell File Downloaded from the Internet" prebuilt detection rule.'
---

# Roshal Archive (RAR) or PowerShell File Downloaded from the Internet

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Roshal Archive (RAR) or PowerShell File Downloaded from the Internet

RAR files and PowerShell scripts are powerful tools in IT environments, used for data compression and task automation, respectively. However, adversaries exploit these for malicious purposes, such as downloading encrypted tools to evade detection. The detection rule identifies unusual downloads of these files from external sources, flagging potential threats by monitoring network traffic and excluding trusted internal IP ranges.

### Possible investigation steps

- Review the network traffic logs to identify the internal host that initiated the download, focusing on the source IP addresses within the ranges 10.0.0.0/8, 172.16.0.0/12, or 192.168.0.0/16.
- Examine the destination IP address of the download to determine if it is associated with known malicious activity or if it is an unusual external IP not typically accessed by the organization.
- Analyze the downloaded file's URL extension or path to confirm if it matches .ps1 or .rar, and assess whether this is expected behavior for the identified host or user.
- Check the internal host's recent activity for any signs of lateral movement or further suspicious downloads, which could indicate a broader compromise.
- Investigate the user account associated with the internal host to verify if the download aligns with their typical usage patterns and permissions.
- Utilize threat intelligence sources to gather additional context on the downloaded file or the external IP address to assess potential risks or known threats.

### False positive analysis

- Internal software updates or legitimate administrative scripts may trigger the rule. To manage this, create exceptions for known internal update servers or trusted administrative IP addresses.
- Automated backup processes that use RAR files for compression can be mistaken for threats. Exclude IP addresses or domains associated with these backup services from the rule.
- Development environments often download scripts for testing purposes. Identify and exclude IP ranges or specific hosts associated with development activities to prevent false positives.
- Security tools that download threat intelligence or updates in RAR format might be flagged. Whitelist the IP addresses of these security tools to avoid unnecessary alerts.
- Regularly review and update the list of trusted internal IP ranges to ensure that legitimate traffic is not incorrectly flagged as suspicious.

### Response and remediation

- Isolate the affected host from the network immediately to prevent further lateral movement or data exfiltration.
- Conduct a thorough scan of the isolated host using updated antivirus and anti-malware tools to identify and remove any malicious files or scripts.
- Review and analyze network logs to identify any other potentially compromised systems or unusual outbound connections that may indicate further compromise.
- Reset credentials and access tokens for the affected host and any other systems that may have been accessed using the compromised host.
- Restore the affected system from a known good backup if malware removal is not feasible or if the system's integrity is in question.
- Implement network segmentation to limit the ability of threats to move laterally within the network in the future.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to ensure comprehensive remediation and recovery efforts.

## Threat intel

This activity has been observed in FIN7 campaigns.
