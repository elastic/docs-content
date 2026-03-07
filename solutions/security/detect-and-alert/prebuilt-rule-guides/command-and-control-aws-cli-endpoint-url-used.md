---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "AWS CLI Command with Custom Endpoint URL" prebuilt detection rule.
---

# AWS CLI Command with Custom Endpoint URL

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating AWS CLI Command with Custom Endpoint URL

The AWS CLI allows users to interact with AWS services via command-line, offering flexibility in managing cloud resources. The `--endpoint-url` option lets users specify alternative endpoints, which can be exploited by adversaries to reroute requests to malicious servers, bypassing security controls. The detection rule identifies such misuse by monitoring for the `--endpoint-url` argument in process logs, flagging potential unauthorized activities.

### Possible investigation steps

- Review the process logs to identify the specific command line that triggered the alert, focusing on the presence of the --endpoint-url argument.
- Investigate the custom endpoint URL specified in the command to determine if it is a known malicious or unauthorized domain.
- Check the user account associated with the process to assess if it has a history of suspicious activity or if it has been compromised.
- Analyze network logs to trace any outbound connections to the custom endpoint URL and evaluate the data being transmitted.
- Correlate the event with other security alerts or logs to identify any patterns or additional indicators of compromise related to the same user or endpoint.
- Verify if the AWS credentials used in the command have been exposed or misused in other contexts, potentially indicating credential theft or abuse.

### False positive analysis

- Internal testing environments may use custom endpoint URLs for development purposes. To manage this, create exceptions for known internal IP addresses or domain names associated with these environments.
- Organizations using AWS CLI with custom endpoints for legitimate third-party integrations might trigger this rule. Identify and whitelist these specific integrations by their endpoint URLs to prevent false positives.
- Automated scripts or tools that interact with AWS services through custom endpoints for monitoring or backup purposes can be flagged. Review and document these scripts, then exclude them from detection by process name or specific endpoint URL.
- Some organizations may use proxy servers that require custom endpoint URLs for AWS CLI operations. Verify these configurations and exclude the associated endpoint URLs from the detection rule.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Review process logs and network traffic to identify any data that may have been redirected to unauthorized endpoints and assess the extent of potential data exposure.
- Revoke any AWS credentials or access keys used on the affected system to prevent further misuse and rotate them with new credentials.
- Conduct a thorough investigation to determine if any other systems have been compromised or if similar unauthorized endpoint usage has occurred elsewhere in the network.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional containment or remediation actions are necessary.
- Implement network-level controls to block known malicious endpoints and enhance monitoring for unusual AWS CLI usage patterns across the environment.
- Update security policies and endpoint protection configurations to detect and alert on the use of custom endpoint URLs in AWS CLI commands, ensuring rapid response to future incidents.
