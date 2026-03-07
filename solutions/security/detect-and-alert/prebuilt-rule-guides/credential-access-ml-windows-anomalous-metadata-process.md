---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Windows Process Calling the Metadata Service" prebuilt detection rule.
---

# Unusual Windows Process Calling the Metadata Service

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Windows Process Calling the Metadata Service

In cloud environments, the metadata service provides essential instance information, including credentials and configuration data. Adversaries may exploit this by using atypical Windows processes to access the service, aiming to extract sensitive information. The detection rule leverages machine learning to identify anomalies in process behavior, flagging potential credential access attempts by unusual processes.

### Possible investigation steps

- Review the process name and command line arguments associated with the alert to identify any unusual or suspicious activity.
- Check the parent process of the flagged process to understand the context of how it was initiated and assess if it aligns with expected behavior.
- Investigate the user account under which the process was executed to determine if it has legitimate access to the metadata service or if it has been compromised.
- Analyze network logs to identify any outbound connections to the metadata service from the flagged process, noting any unusual patterns or destinations.
- Cross-reference the process and user activity with recent changes or deployments in the environment to rule out false positives related to legitimate administrative actions.
- Consult threat intelligence sources to see if the process or command line arguments have been associated with known malicious activity or campaigns.

### False positive analysis

- Routine system updates or maintenance scripts may trigger the rule. Review the process details and verify if they align with scheduled maintenance activities. If confirmed, consider adding these processes to an exception list.
- Legitimate software or security tools that access the metadata service for configuration purposes might be flagged. Identify these tools and create exceptions for their known processes to prevent future alerts.
- Automated backup or monitoring solutions that interact with the metadata service could be misidentified as threats. Validate these processes and exclude them if they are part of authorized operations.
- Custom scripts developed in-house for cloud management tasks may access the metadata service. Ensure these scripts are documented and, if safe, add them to the list of exceptions to reduce false positives.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate the unusual process accessing the metadata service to stop any ongoing credential harvesting attempts.
- Conduct a thorough review of the system's event logs and process history to identify any additional indicators of compromise or related malicious activity.
- Change all credentials that may have been exposed or accessed through the metadata service to mitigate the risk of unauthorized access.
- Implement network segmentation to limit access to the metadata service, ensuring only authorized processes and users can interact with it.
- Escalate the incident to the security operations center (SOC) for further analysis and to determine if the threat is part of a larger attack campaign.
- Update and enhance endpoint detection and response (EDR) solutions to improve monitoring and alerting for similar anomalous process behaviors in the future.
