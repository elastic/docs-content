---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Data Exfiltration Through Curl" prebuilt detection rule.'
---

# Potential Data Exfiltration Through Curl

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Data Exfiltration Through Curl

Curl is a command-line tool used for transferring data with URLs, commonly employed for legitimate data exchange tasks. However, adversaries can exploit curl to exfiltrate sensitive data by uploading compressed files to remote servers. The detection rule identifies suspicious curl usage by monitoring for specific command patterns and arguments indicative of data uploads, flagging abnormal activities for further investigation.

### Possible investigation steps

- Review the process command line to confirm the presence of suspicious arguments such as "-F", "-T", "-d", or "--data*" and check for any compressed file extensions like .zip, .gz, or .tgz being uploaded to an external server.
- Investigate the parent process of the curl command to understand the context in which curl was executed, including the parent executable and its purpose.
- Examine network logs to identify the destination IP address or domain to which the data was being uploaded, and assess whether it is a known or suspicious entity.
- Check for any recent file creation or modification events on the host that match the compressed file types mentioned in the query, which could indicate data collection prior to exfiltration.
- Correlate this event with other security alerts or logs from the same host to identify any patterns of behavior that might suggest a broader compromise or data exfiltration attempt.

### False positive analysis

- Legitimate data transfers using curl for system backups or data synchronization can trigger the rule. To manage this, identify and whitelist specific processes or scripts that are known to perform these tasks regularly.
- Automated system updates or software installations that use curl to download and upload data might be flagged. Exclude these processes by verifying their source and adding them to an exception list if they are from trusted vendors.
- Internal data transfers within a secure network that use curl for efficiency can be mistaken for exfiltration. Monitor the destination IP addresses and exclude those that are internal or known safe endpoints.
- Developers or system administrators using curl for testing or development purposes may inadvertently trigger the rule. Educate these users on the potential alerts and establish a process for them to notify security teams of their activities to prevent unnecessary investigations.
- Scheduled tasks or cron jobs that use curl for routine data uploads should be reviewed and, if deemed safe, added to an exception list to avoid repeated false positives.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further data exfiltration and contain the threat.
- Terminate any suspicious curl processes identified by the detection rule to stop ongoing data transfers.
- Conduct a forensic analysis of the affected system to identify any additional malicious activities or compromised data.
- Change credentials and access keys that may have been exposed or used during the incident to prevent unauthorized access.
- Notify the security operations team and relevant stakeholders about the incident for awareness and further action.
- Review and update firewall and network security rules to block unauthorized outbound traffic, especially to suspicious or unknown external servers.
- Implement enhanced monitoring and logging for curl usage and similar data transfer tools to detect and respond to future exfiltration attempts promptly.
