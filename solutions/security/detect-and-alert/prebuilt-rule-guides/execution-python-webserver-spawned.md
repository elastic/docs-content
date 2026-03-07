---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Web Server Spawned via Python" prebuilt detection rule.'
---

# Web Server Spawned via Python

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Web Server Spawned via Python

Python's built-in HTTP server module allows quick web server deployment, often used for testing or file sharing. Adversaries exploit this to exfiltrate data or facilitate lateral movement within networks. The detection rule identifies processes starting a Python-based server, focusing on command patterns and shell usage, to flag potential misuse on Linux systems.

### Possible investigation steps

- Review the process details to confirm the presence of a Python-based web server by checking the process name and arguments, specifically looking for "python" with "http.server" or "SimpleHTTPServer".
- Investigate the user account associated with the process to determine if it is a known or expected user for running such services.
- Examine the command line used to start the process for any unusual or suspicious patterns, especially if it involves shell usage like "bash" or "sh" with the command line containing "python -m http.server".
- Check the network activity from the host to identify any unusual outbound connections or data transfers that could indicate data exfiltration.
- Correlate the event with other logs or alerts from the same host to identify any preceding or subsequent suspicious activities that might suggest lateral movement or further exploitation attempts.
- Assess the host's security posture and recent changes to determine if there are any vulnerabilities or misconfigurations that could have been exploited to spawn the web server.

### False positive analysis

- Development and testing environments often use Python's HTTP server for legitimate purposes such as serving static files or testing web applications. To manage this, create exceptions for known development servers by excluding specific hostnames or IP addresses.
- Automated scripts or cron jobs may start a Python web server for routine tasks like file distribution within a controlled environment. Identify these scripts and exclude their execution paths or user accounts from the detection rule.
- Educational or training sessions might involve participants using Python's HTTP server to learn web technologies. Exclude these activities by setting time-based exceptions during scheduled training periods.
- System administrators might use Python's HTTP server for quick file transfers or troubleshooting. Document these use cases and exclude the associated user accounts or process command lines from triggering alerts.
- Internal tools or utilities developed in-house may rely on Python's HTTP server for functionality. Review these tools and exclude their specific command patterns or execution contexts from the detection rule.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further data exfiltration or lateral movement.
- Terminate the suspicious Python process identified by the detection rule to stop the unauthorized web server.
- Conduct a forensic analysis of the affected system to identify any data that may have been accessed or exfiltrated and to determine the initial access vector.
- Review and secure any exposed credentials or sensitive data that may have been compromised during the incident.
- Apply patches and updates to the affected system and any related software to mitigate vulnerabilities that may have been exploited.
- Implement network segmentation to limit the ability of unauthorized processes to communicate across the network.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to ensure comprehensive remediation and recovery actions are taken.
