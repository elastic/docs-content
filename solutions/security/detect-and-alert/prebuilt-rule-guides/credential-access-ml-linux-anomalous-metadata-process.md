---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Linux Process Calling the Metadata Service" prebuilt detection rule.
---

# Unusual Linux Process Calling the Metadata Service

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Linux Process Calling the Metadata Service

In cloud environments, the metadata service provides essential instance-specific data, including credentials and configuration scripts. Adversaries may exploit this service by using atypical processes to access sensitive information, potentially leading to credential theft. The detection rule leverages machine learning to identify anomalous process behavior, flagging unusual access patterns indicative of malicious intent.

### Possible investigation steps

- Review the process name and command line arguments associated with the alert to identify any unusual or suspicious activity.
- Check the user account under which the process is running to determine if it has legitimate access to the metadata service.
- Investigate the process's parent process to understand the context of how it was initiated and whether it aligns with expected behavior.
- Analyze network logs to verify if the process made any outbound connections to the metadata service and assess the volume and frequency of these requests.
- Cross-reference the process and user information with recent changes or deployments in the environment to rule out any legitimate use cases.
- Examine system logs for any other suspicious activities or anomalies around the time the alert was triggered, such as unauthorized access attempts or privilege escalations.

### False positive analysis

- Routine system updates or maintenance scripts may access the metadata service, triggering false positives. Users can create exceptions for known update processes to prevent unnecessary alerts.
- Automated backup or monitoring tools might interact with the metadata service as part of their normal operations. Identify these tools and whitelist their processes to reduce false alarms.
- Custom scripts developed in-house for configuration management might access the metadata service. Review these scripts and add them to an exception list if they are verified as non-threatening.
- Cloud management agents provided by the cloud service provider may access the metadata service for legitimate purposes. Verify these agents and exclude them from the detection rule to avoid false positives.
- Development or testing environments often have processes that mimic production behavior, including metadata service access. Ensure these environments are accounted for in the rule configuration to minimize false alerts.

### Response and remediation

- Isolate the affected instance immediately to prevent further unauthorized access to the metadata service and potential lateral movement within the network.
- Terminate the unusual process accessing the metadata service to stop any ongoing data exfiltration or credential harvesting.
- Conduct a thorough review of access logs and process execution history on the affected instance to identify any additional unauthorized activities or compromised credentials.
- Rotate all credentials and secrets that may have been exposed through the metadata service to mitigate the risk of credential theft and unauthorized access.
- Implement network segmentation and access controls to restrict access to the metadata service, ensuring only authorized processes and users can interact with it.
- Escalate the incident to the security operations team for further investigation and to determine if additional instances or services have been compromised.
- Update and enhance monitoring rules to detect similar anomalous behaviors in the future, focusing on unusual process activities and access patterns to the metadata service.
