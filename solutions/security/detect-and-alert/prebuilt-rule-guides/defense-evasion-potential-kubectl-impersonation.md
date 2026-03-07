---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Impersonation Attempt via Kubectl" prebuilt detection rule.'
---

# Potential Impersonation Attempt via Kubectl

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Impersonation Attempt via Kubectl

Kubectl is a command-line tool for interacting with Kubernetes clusters, allowing users to manage applications and resources. Adversaries may exploit kubectl by using specific arguments to impersonate users, gaining unauthorized access or escalating privileges. The detection rule identifies suspicious kubectl executions, focusing on arguments that suggest impersonation, such as those related to user identity and authentication, to flag potential misuse.

### Possible investigation steps

- Review the process arguments to confirm the presence of impersonation-related flags such as "--kubeconfig", "--token", "--as", "--as-group", or "--as-uid" to understand the scope of the impersonation attempt.
- Examine the parent process name and executable path to determine if the kubectl command was initiated from a suspicious location or script, such as "/tmp/*", "/var/tmp/*", "/dev/shm/*", "/root/*", or "/home/*".
- Check the user account associated with the kubectl execution to assess whether it aligns with expected usage patterns or if it indicates potential unauthorized access.
- Investigate related alerts or logs for secret access or kubeconfig file discovery to identify if there is a broader pattern of suspicious activity that could indicate a coordinated impersonation attempt.
- Analyze the network activity associated with the kubectl execution to identify any unusual connections or data transfers that may suggest unauthorized access or data exfiltration.

### False positive analysis

- Legitimate administrative tasks: System administrators may use kubectl with impersonation arguments for legitimate purposes such as testing permissions or managing resources on behalf of other users. To handle this, create exceptions for known administrative accounts or specific IP addresses.
- Automation scripts: Automated scripts or CI/CD pipelines might use impersonation arguments to perform tasks across different environments. Review and whitelist these scripts by identifying their unique execution patterns or specific user accounts.
- Development and testing environments: Developers might use impersonation features in non-production environments for testing purposes. Exclude these environments by filtering based on environment-specific identifiers or network segments.
- Security tools: Some security tools or monitoring solutions may use impersonation arguments to audit or verify access controls. Identify these tools and exclude their processes by recognizing their signatures or execution paths.
- Frequent legitimate use cases: If certain teams or departments regularly use impersonation for valid reasons, consider creating role-based exceptions to reduce noise while maintaining security oversight.

### Response and remediation

- Immediately isolate the affected Kubernetes node or cluster to prevent further unauthorized access or privilege escalation.
- Revoke any potentially compromised credentials, such as tokens or kubeconfig files, and issue new ones with updated security policies.
- Review and audit the Kubernetes RBAC (Role-Based Access Control) settings to ensure that only authorized users have the necessary permissions, and adjust roles and permissions as needed to minimize privilege escalation risks.
- Conduct a thorough investigation of the affected systems to identify any unauthorized changes or deployments made by the adversary, and roll back any malicious or suspicious configurations.
- Monitor for any further suspicious kubectl activity, especially those involving impersonation arguments, and set up alerts for any similar future attempts.
- Escalate the incident to the security operations team for a comprehensive review and to determine if additional security measures or incident response actions are required.
- Implement additional logging and monitoring for kubectl commands and Kubernetes API interactions to enhance detection capabilities for similar threats in the future.
