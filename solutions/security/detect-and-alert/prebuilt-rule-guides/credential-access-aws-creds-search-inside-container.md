---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS Credentials Searched For Inside A Container" prebuilt detection rule.
---

# AWS Credentials Searched For Inside A Container

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating AWS Credentials Searched For Inside A Container

Containers often house applications that interact with AWS services, necessitating the storage of AWS credentials. Adversaries may exploit this by using search utilities to locate these credentials, potentially leading to unauthorized access. The detection rule identifies suspicious use of search tools within containers, flagging attempts to locate AWS credentials by monitoring specific process names and arguments, thus helping to prevent credential theft and subsequent attacks.

### Possible investigation steps

- Review the process details to identify the specific search utility used (e.g., grep, find) and the arguments passed, focusing on those related to AWS credentials such as aws_access_key_id or aws_secret_access_key.
- Check the user context under which the suspicious process was executed to assess whether it aligns with expected behavior for that user or role within the container.
- Investigate the source of the container image to ensure it is from a trusted repository and has not been tampered with, which could indicate a supply chain compromise.
- Analyze recent activity logs for the container to identify any other suspicious behavior or anomalies that might correlate with the search for AWS credentials, such as unexpected network connections or file modifications.
- Review access logs for AWS services to detect any unauthorized or unusual access patterns that might suggest the use of compromised credentials.

### False positive analysis

- Routine maintenance scripts or automated processes may use search utilities to verify the presence of AWS credentials for legitimate configuration checks. To handle this, identify and whitelist these specific scripts or processes by their unique identifiers or execution paths.
- Developers or system administrators might manually search for AWS credentials during debugging or configuration tasks. Implement a policy to log and review these activities, and consider excluding known user accounts or roles from triggering alerts during specific time windows or in designated environments.
- Security audits or compliance checks often involve searching for sensitive information, including AWS credentials, to ensure proper security measures are in place. Coordinate with audit teams to schedule these activities and temporarily suppress alerts during these periods, or exclude specific audit tools from detection.
- Continuous integration and deployment (CI/CD) pipelines might include steps that search for AWS credentials to validate environment configurations. Identify these pipelines and exclude their associated processes or container environments from triggering alerts, ensuring that only authorized CI/CD tools are used.

### Response and remediation

- Immediately isolate the affected container to prevent further unauthorized access or data exfiltration. This can be done by stopping the container or disconnecting it from the network.
- Revoke any AWS credentials that were potentially exposed or accessed. This includes rotating keys and updating any services or applications that rely on these credentials.
- Conduct a thorough review of the container's file system to identify any unauthorized changes or additional malicious files that may have been introduced.
- Implement stricter access controls and monitoring on AWS credentials within containers, ensuring they are stored securely and accessed only by authorized processes.
- Escalate the incident to the cloud security team to assess the potential impact on the broader cloud environment and determine if further investigation or response is needed.
- Enhance logging and monitoring for similar activities across other containers and cloud environments to detect and respond to future attempts promptly.
- Review and update container security policies to include best practices for credential management and access control, reducing the risk of similar incidents.
