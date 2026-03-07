---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential THC Tool Downloaded" prebuilt detection rule.'
---

# Potential THC Tool Downloaded

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential THC Tool Downloaded

The Hacker's Choice is a suite of hacker tools that are frequently used by threat actors. One common tool is SSH-IT, which is an autonomous worm that exploits SSH connections to propagate across networks. It hijacks outgoing SSH sessions, allowing adversaries to move laterally within a compromised environment. Attackers often use tools like curl or wget to download the worm from specific URLs. The detection rule identifies these download attempts by monitoring process activities on Linux systems, focusing on command-line arguments that match known malicious URLs, thereby alerting security teams to potential threats.

### Possible investigation steps

- Review the alert details to identify the specific process name (either curl or wget) and the URL involved in the download attempt to confirm it matches one of the known malicious URLs listed in the query.
- Check the process execution context, including the user account under which the process was executed, to determine if it was initiated by a legitimate user or potentially compromised account.
- Investigate the source IP address and hostname of the affected Linux system to understand its role within the network and assess the potential impact of lateral movement.
- Examine the system's SSH logs to identify any unusual or unauthorized SSH connections that may indicate further compromise or lateral movement attempts.
- Analyze the network traffic logs for any outbound connections to the identified malicious URLs to confirm whether the download attempt was successful and if any additional payloads were retrieved.
- Review historical alerts and logs for any previous similar activities on the same host or user account to identify patterns or repeated attempts that may indicate a persistent threat.

### False positive analysis

- Legitimate administrative tasks using curl or wget to download files from the internet may trigger the rule. To manage this, security teams can create exceptions for specific URLs or IP addresses known to be safe and frequently accessed by administrators.
- Automated scripts or cron jobs that use curl or wget to download updates or configuration files from trusted internal or external sources might be flagged. Users can whitelist these scripts or the specific URLs they access to prevent unnecessary alerts.
- Development or testing environments where developers frequently download open-source tools or libraries using curl or wget could generate false positives. Implementing a policy to exclude these environments from the rule or setting up a separate monitoring profile for them can help reduce noise.
- Security tools or monitoring solutions that use curl or wget for health checks or data collection might be mistakenly identified. Identifying these tools and excluding their known benign activities from the rule can help maintain focus on genuine threats.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further lateral movement by the SSH-IT worm.
- Terminate any suspicious processes identified as using curl or wget with the malicious URLs to stop the download and execution of the worm.
- Conduct a thorough scan of the isolated host using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any instances of the SSH-IT worm.
- Review and reset credentials for any SSH accounts that may have been compromised, ensuring the use of strong, unique passwords and considering the implementation of multi-factor authentication (MFA).
- Analyze network logs and SSH access logs to identify any lateral movement or unauthorized access attempts, and take steps to secure any other potentially compromised systems.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Update firewall and intrusion detection/prevention system (IDS/IPS) rules to block the known malicious URLs and monitor for any future attempts to access them.
