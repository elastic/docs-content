---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Web Config File Access" prebuilt detection rule.
---

# Unusual Web Config File Access

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Web Config File Access
Web.config files are crucial in Windows environments, storing sensitive data like database credentials and encryption keys. Adversaries target these files to extract information for attacks such as forging malicious requests or accessing databases. The detection rule identifies suspicious access patterns by monitoring file access events in specific directories, helping analysts spot potential credential theft or server exploitation attempts.

### Possible investigation steps

- Investigate the user account associated with the access event to verify if the account has legitimate reasons to access the web.config file or if it might be compromised.
- Analyze recent activity from the same user or IP address to identify any other suspicious behavior or access patterns that could indicate a broader security incident.
- Review system logs and network traffic around the time of the alert to identify any related anomalies or signs of exploitation attempts, such as unusual database queries or web server requests.

### False positive analysis

- Routine administrative tasks by IT personnel may trigger alerts when accessing web.config files for legitimate configuration updates. To manage this, create exceptions for known administrative accounts or scheduled maintenance windows.
- Automated backup processes that access web.config files can be mistaken for suspicious activity. Identify and exclude these processes by their specific user accounts or service names.
- Web application updates or deployments often involve accessing web.config files. Exclude these activities by correlating them with known deployment tools or scripts.
- Security scanning tools that check web.config files for vulnerabilities might generate false positives. Whitelist these tools by their process names or IP addresses to prevent unnecessary alerts.
- Monitoring or logging solutions that periodically read web.config files for audit purposes can be excluded by identifying their specific access patterns and excluding them from the rule.

### Response and remediation

- Immediately isolate the affected server to prevent further unauthorized access and potential lateral movement within the network.
- Conduct a thorough review of the web.config file to identify any unauthorized changes or access patterns, focusing on exposed credentials and keys.
- Rotate all credentials and keys found within the web.config file, including database connection strings and encryption keys, to mitigate the risk of credential theft.
- Implement additional monitoring and logging for access to web.config files across all servers to detect future unauthorized access attempts.
- Escalate the incident to the security operations center (SOC) for further investigation and correlation with other potential indicators of compromise.
- Review and update firewall rules and access controls to ensure that only authorized users and applications can access sensitive directories containing web.config files.
- Conduct a post-incident analysis to identify gaps in security controls and enhance detection capabilities for similar threats in the future.

