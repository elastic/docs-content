---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Kubernetes Direct API Request via Curl or Wget" prebuilt detection rule.'
---

# Kubernetes Direct API Request via Curl or Wget

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Kubernetes Direct API Request via Curl or Wget

Kubernetes API endpoints are crucial for managing cluster resources. Adversaries may exploit tools like curl or wget to directly query these endpoints, bypassing standard clients like kubectl, to extract sensitive data such as secrets or config maps. The detection rule identifies such unauthorized access attempts by monitoring command executions that target specific API paths, flagging potential security threats.

### Possible investigation steps

- Review the process details to confirm the execution of curl or wget, focusing on the process.name and process.args fields to understand the exact command used and the specific Kubernetes API endpoint targeted.
- Check the user context under which the curl or wget command was executed, including user ID and group ID, to determine if the action was performed by a legitimate user or an unauthorized entity.
- Investigate the source IP address and host information to identify the origin of the request and assess whether it aligns with expected network activity within the Kubernetes environment.
- Examine recent authentication and authorization logs for any anomalies or failed attempts that might indicate unauthorized access attempts to the Kubernetes API.
- Correlate the alert with other security events or logs from the same timeframe to identify any related suspicious activities, such as unusual network traffic or access patterns.
- Assess the potential impact by reviewing the specific Kubernetes resources targeted, such as secrets or config maps, to determine if sensitive data might have been exposed or compromised.

### False positive analysis

- Routine monitoring scripts or health checks that use curl or wget to verify the availability of Kubernetes API endpoints may trigger this rule. To manage this, identify and whitelist the specific scripts or IP addresses that are known to perform these checks regularly.
- Automated backup processes that access Kubernetes secrets or config maps using curl or wget could be flagged. Exclude these processes by specifying their unique command patterns or execution contexts in the detection rule.
- Developers or administrators using curl or wget for legitimate troubleshooting or testing purposes might inadvertently trigger the rule. Implement user-based exceptions for known and trusted personnel who require such access for their roles.
- Integration tools or CI/CD pipelines that interact with Kubernetes APIs using curl or wget for deployment or configuration tasks may cause false positives. Create exceptions for these tools by identifying their process names or execution environments.
- Security scanners or vulnerability assessment tools that probe Kubernetes API endpoints as part of their scanning routines can be mistaken for unauthorized access attempts. Whitelist these tools by their known signatures or execution patterns to prevent false alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access to Kubernetes API endpoints.
- Revoke any potentially compromised credentials or tokens that may have been used in the unauthorized API requests.
- Conduct a thorough review of Kubernetes audit logs to identify the scope of the unauthorized access and determine if any sensitive data was exfiltrated.
- Reset and rotate all secrets and config maps that may have been accessed during the incident to ensure they are no longer valid.
- Implement network segmentation and access controls to restrict direct access to Kubernetes API endpoints, ensuring only authorized clients can communicate with the API.
- Escalate the incident to the security operations team for further investigation and to assess the need for additional security measures or incident response actions.
- Enhance monitoring and alerting for similar unauthorized access attempts by integrating additional threat intelligence and refining detection capabilities.
