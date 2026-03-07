---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Curl SOCKS Proxy Activity from Unusual Parent" prebuilt detection rule.'
---

# Curl SOCKS Proxy Activity from Unusual Parent

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Curl SOCKS Proxy Activity from Unusual Parent

Curl is a versatile command-line tool used for transferring data with URLs, often employed for legitimate data retrieval. However, adversaries can exploit its SOCKS proxy capabilities to bypass network restrictions, facilitating covert data exfiltration or communication with command and control servers. The detection rule identifies suspicious curl executions initiated by atypical parent processes, such as those from temporary directories or shell environments, combined with SOCKS proxy arguments, indicating potential misuse.

### Possible investigation steps

- Review the parent process details to understand the context of the curl execution, focusing on unusual directories like /dev/shm, /tmp, or shell environments such as bash or zsh.
- Examine the command-line arguments used with curl, specifically looking for SOCKS proxy options like --socks5-hostname or -x, to determine the intent and destination of the network request.
- Investigate the environment variables set for the process, such as http_proxy or HTTPS_PROXY, to identify any proxy configurations that might indicate an attempt to bypass network restrictions.
- Check the user account associated with the process execution to determine if it aligns with expected behavior or if it might be compromised.
- Analyze network logs to trace the destination IP addresses or domains contacted via the SOCKS proxy to assess if they are known malicious or suspicious entities.
- Correlate this activity with other alerts or logs from the same host to identify any patterns or additional indicators of compromise.

### False positive analysis

- Development environments may frequently use curl with SOCKS proxy options for legitimate testing purposes. To manage this, consider excluding specific development directories or user accounts from the rule.
- Automated scripts or cron jobs running from shell environments might use curl with SOCKS proxies for routine data retrieval. Identify these scripts and exclude their parent processes or specific arguments from triggering the rule.
- System administrators might use curl with SOCKS proxies for network diagnostics or maintenance tasks. Document these activities and create exceptions for known administrative accounts or specific command patterns.
- Web applications hosted in directories like /var/www/html may use curl for backend operations involving SOCKS proxies. Review these applications and whitelist their specific processes or arguments if they are verified as non-threatening.
- Temporary directories such as /tmp or /dev/shm might be used by legitimate software for transient operations involving curl. Monitor these occurrences and exclude known benign software from the rule.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further data exfiltration or communication with command and control servers.
- Terminate any suspicious curl processes identified by the detection rule to halt potential malicious activity.
- Conduct a forensic analysis of the affected system to identify any additional indicators of compromise, such as unauthorized file modifications or additional malicious processes.
- Review and clean up any unauthorized or suspicious files in temporary directories or other unusual locations, such as /dev/shm, /tmp, or /var/tmp, to remove potential threats.
- Reset credentials and review access logs for any accounts that may have been compromised or used in conjunction with the detected activity.
- Implement network monitoring to detect and block any further attempts to use SOCKS proxy connections from unauthorized sources.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if broader organizational impacts exist.
