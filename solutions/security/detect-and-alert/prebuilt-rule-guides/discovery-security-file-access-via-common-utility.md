---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Security File Access via Common Utilities" prebuilt detection rule.
---

# Security File Access via Common Utilities

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Security File Access via Common Utilities

In Linux environments, common utilities like `cat`, `grep`, and `less` are essential for file manipulation and viewing. Adversaries exploit these tools to access sensitive security files, aiming to gather system and security configuration data. The detection rule identifies suspicious use of these utilities by monitoring process execution patterns and arguments, flagging attempts to access critical security files, thus helping to thwart potential reconnaissance activities.

### Possible investigation steps

- Review the process execution details to identify the specific utility used (e.g., cat, grep, less) and the exact file path accessed, as indicated by the process.name and process.args fields.
- Check the user account associated with the process execution to determine if the access was performed by a legitimate user or a potentially compromised account.
- Investigate the timing and frequency of the access attempt to assess whether it aligns with normal user behavior or indicates suspicious activity.
- Correlate the alert with other security events or logs from the same host to identify any preceding or subsequent suspicious activities, such as unauthorized logins or privilege escalation attempts.
- Examine the host's recent changes or updates to security configurations or user permissions that might explain the access attempt.
- If possible, contact the user or system owner to verify whether the access was intentional and authorized, providing additional context for the investigation.

### False positive analysis

- System administrators or automated scripts may frequently access security files for legitimate maintenance or configuration purposes. To handle this, create exceptions for known administrative accounts or specific scripts that regularly perform these actions.
- Security monitoring tools or compliance checks might trigger the rule when scanning security files. Identify these tools and exclude their processes from the rule to prevent unnecessary alerts.
- Backup processes that involve copying or reading security files can be mistaken for suspicious activity. Exclude backup software processes or scheduled tasks that are known to perform these operations.
- Developers or DevOps personnel accessing configuration files for application deployment or troubleshooting might trigger the rule. Establish a list of trusted users or roles and exclude their access patterns from detection.
- Regular system updates or package management operations may involve accessing security-related files. Recognize these update processes and exclude them to avoid false positives during routine maintenance.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified by the detection rule to halt potential reconnaissance activities.
- Conduct a thorough review of the accessed files to determine if any sensitive information was exposed or altered.
- Change credentials and access tokens for any compromised accounts, especially those related to AWS, GCP, or Azure, to prevent unauthorized access.
- Implement stricter access controls and permissions on sensitive security files to limit exposure to only necessary users and processes.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on the broader network.
- Enhance monitoring and logging for similar activities to improve detection and response times for future incidents.
