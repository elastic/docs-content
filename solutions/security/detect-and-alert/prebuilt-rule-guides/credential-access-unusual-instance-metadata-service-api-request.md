---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Instance Metadata Service (IMDS) API Request" prebuilt detection rule.'
---

# Unusual Instance Metadata Service (IMDS) API Request

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Instance Metadata Service (IMDS) API Request

The Instance Metadata Service (IMDS) API provides essential instance-specific data, including configuration details and temporary credentials, to applications running on cloud instances. Adversaries exploit this by using scripts or tools to access sensitive data, potentially leading to unauthorized access. The detection rule identifies suspicious access attempts by monitoring specific processes and network activities, excluding known legitimate paths, to flag potential misuse.

### Possible investigation steps

- Review the process details such as process.name and process.command_line to identify the tool or script used to access the IMDS API and determine if it aligns with known malicious behavior.
- Examine the process.executable and process.working_directory fields to verify if the execution path is unusual or suspicious, especially if it originates from directories like /tmp/* or /var/tmp/*.
- Check the process.parent.entity_id and process.parent.executable to understand the parent process and its legitimacy, which might provide context on how the suspicious process was initiated.
- Investigate the network event details, particularly the destination.ip field, to confirm if there was an attempted connection to the IMDS API endpoint at 169.254.169.254.
- Correlate the host.id with other security events or logs to identify any additional suspicious activities or patterns on the same host that might indicate a broader compromise.
- Assess the risk score and severity to prioritize the investigation and determine if immediate action is required to mitigate potential threats.

### False positive analysis

- Security and monitoring tools like Rapid7, Nessus, and Amazon SSM Agent may trigger false positives due to their legitimate access to the IMDS API. Users can exclude these by adding their working directories to the exception list.
- Automated scripts or processes running from known directories such as /opt/rumble/bin or /usr/share/ec2-instance-connect may also cause false positives. Exclude these directories or specific executables from the rule to prevent unnecessary alerts.
- System maintenance or configuration scripts that access the IMDS API for legitimate purposes might be flagged. Identify these scripts and add their paths or parent executables to the exclusion list to reduce noise.
- Regular network monitoring tools that attempt connections to the IMDS IP address for health checks or status updates can be excluded by specifying their process names or executable paths in the exception criteria.

### Response and remediation

- Immediately isolate the affected instance from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified in the alert that are attempting to access the IMDS API, especially those using tools like curl, wget, or python.
- Revoke any temporary credentials that may have been exposed or accessed through the IMDS API to prevent unauthorized use.
- Conduct a thorough review of the instance's security groups and IAM roles to ensure that only necessary permissions are granted and that there are no overly permissive policies.
- Escalate the incident to the security operations team for further investigation and to determine if additional instances or resources are affected.
- Implement network monitoring to detect and alert on any future attempts to access the IMDS API from unauthorized processes or locations.
- Review and update the instance's security configurations and apply any necessary patches or updates to mitigate vulnerabilities that could be exploited in similar attacks.
