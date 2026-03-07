---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Privilege Escalation via CAP_CHOWN/CAP_FOWNER Capabilities" prebuilt detection rule.
---

# Privilege Escalation via CAP_CHOWN/CAP_FOWNER Capabilities

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Privilege Escalation via CAP_CHOWN/CAP_FOWNER Capabilities

In Linux, CAP_CHOWN and CAP_FOWNER are capabilities that allow processes to change file ownership and bypass file permission checks, respectively. Adversaries exploit these to gain unauthorized access to sensitive files, such as password or configuration files. The detection rule identifies suspicious processes with these capabilities that alter ownership of critical files, signaling potential privilege escalation attempts.

### Possible investigation steps

- Review the process details, including process.name and process.command_line, to understand the context of the executed process and its intended function.
- Check the user.id associated with the process to determine if the process was executed by a non-root user, which could indicate unauthorized privilege escalation attempts.
- Investigate the file.path that had its ownership changed to assess the potential impact, focusing on critical files like /etc/passwd, /etc/shadow, /etc/sudoers, and /root/.ssh/*.
- Analyze the sequence of events by examining the host.id and process.pid to identify any related processes or activities that occurred within the maxspan=1s timeframe.
- Correlate the event with other logs or alerts from the same host to identify any patterns or additional suspicious activities that might indicate a broader attack or compromise.

### False positive analysis

- System administration scripts or automated processes may legitimately use CAP_CHOWN or CAP_FOWNER capabilities to manage file permissions or ownership. Review and whitelist these processes if they are verified as non-malicious.
- Backup or restoration operations often require changing file ownership and permissions. Identify and exclude these operations from triggering alerts by specifying known backup tools or scripts.
- Software installation or update processes might alter file ownership as part of their normal operation. Monitor and exclude these processes if they are part of a trusted software management system.
- Development or testing environments may have scripts that modify file ownership for testing purposes. Ensure these environments are properly segmented and exclude known development scripts from detection.
- Custom user scripts that require elevated permissions for legitimate tasks should be reviewed and, if deemed safe, added to an exception list to prevent false positives.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified with CAP_CHOWN or CAP_FOWNER capabilities that are altering file ownership, especially those targeting critical files like /etc/passwd or /etc/shadow.
- Revert any unauthorized changes to file ownership or permissions on critical files to their original state to restore system integrity.
- Conduct a thorough review of user accounts and privileges on the affected system to identify and disable any unauthorized accounts or privilege escalations.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are compromised.
- Implement additional monitoring on the affected host and similar systems to detect any further attempts to exploit CAP_CHOWN or CAP_FOWNER capabilities.
- Review and update security policies and configurations to restrict the assignment of CAP_CHOWN and CAP_FOWNER capabilities to only trusted and necessary processes.
