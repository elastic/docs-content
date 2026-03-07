---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Pluggable Authentication Module (PAM) Version Discovery" prebuilt detection rule.
---

# Pluggable Authentication Module (PAM) Version Discovery

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Pluggable Authentication Module (PAM) Version Discovery

Pluggable Authentication Modules (PAM) provide a flexible mechanism for authenticating users on Linux systems. Adversaries may exploit PAM by discovering its version to identify vulnerabilities or backdoor the authentication process with malicious modules. The detection rule identifies suspicious processes querying PAM-related packages, indicating potential reconnaissance or tampering attempts, thus alerting security teams to possible threats.

### Possible investigation steps

- Review the process details to confirm the presence of suspicious activity, focusing on processes with names "dpkg", "dpkg-query", or "rpm" and their arguments "libpam-modules" or "pam".
- Check the user account associated with the process to determine if it is a legitimate user or potentially compromised.
- Investigate the parent process to understand the origin of the command execution and assess if it aligns with normal user behavior.
- Analyze recent login attempts and authentication logs to identify any unusual patterns or failed attempts that may indicate unauthorized access attempts.
- Correlate this activity with other alerts or logs from the same host to identify if there are additional indicators of compromise or related suspicious activities.

### False positive analysis

- Routine system updates or package management activities may trigger the rule when legitimate processes like dpkg or rpm query PAM-related packages. To manage this, consider creating exceptions for known maintenance windows or trusted administrative scripts.
- Automated configuration management tools, such as Ansible or Puppet, might execute commands that match the rule's criteria. Identify these tools and exclude their processes from triggering alerts by specifying their execution context.
- Security compliance checks or vulnerability assessments often involve querying system packages, including PAM. If these are regularly scheduled and verified, whitelist the associated processes to prevent unnecessary alerts.
- Developers or system administrators testing PAM configurations might inadvertently trigger the rule. Establish a protocol for notifying the security team of such activities in advance, allowing for temporary exceptions during testing periods.
- Custom scripts used for system monitoring or auditing may include commands that match the rule. Review these scripts and, if deemed safe, add them to an exclusion list to reduce false positives.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious processes identified by the detection rule, specifically those involving 'dpkg', 'dpkg-query', or 'rpm' with arguments related to PAM.
- Conduct a thorough review of PAM configuration files and modules on the affected system to identify and remove any unauthorized or malicious modifications.
- Restore any compromised PAM modules from a known good backup to ensure the integrity of the authentication process.
- Monitor for any additional suspicious activity on the affected system and related systems, focusing on unusual authentication attempts or process executions.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for PAM-related activities across the network to detect similar threats in the future.
