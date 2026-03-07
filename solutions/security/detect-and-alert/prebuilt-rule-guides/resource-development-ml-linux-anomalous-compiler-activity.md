---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Anomalous Linux Compiler Activity" prebuilt detection rule.'
---

# Anomalous Linux Compiler Activity

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Anomalous Linux Compiler Activity

Compilers transform source code into executable programs, a crucial step in software development. In Linux environments, unexpected compiler use by atypical users may signal unauthorized software changes or privilege escalation attempts. Adversaries exploit this by deploying malicious code or exploits. The detection rule leverages machine learning to identify unusual compiler activity, flagging potential threats by analyzing user behavior patterns and deviations from normal operations.

### Possible investigation steps

- Review the user account associated with the anomalous compiler activity to determine if the user typically engages in software development or has a history of using compilers.
- Check the specific compiler and version used in the activity to identify if it is a known or legitimate tool within the organization.
- Analyze the source and destination of the compiler activity, including the IP addresses and hostnames, to identify any unusual or unauthorized access patterns.
- Investigate recent changes or deployments on the system where the compiler activity was detected to identify any unauthorized software installations or modifications.
- Examine system logs and audit trails for any signs of privilege escalation attempts or other suspicious activities around the time of the compiler usage.
- Cross-reference the detected activity with known threat intelligence sources to determine if the behavior matches any known attack patterns or indicators of compromise.

### False positive analysis

- Development environments where multiple users compile code can trigger false positives. Regularly update the list of authorized users who are expected to use compilers to prevent unnecessary alerts.
- Automated build systems or continuous integration pipelines may be flagged. Exclude these systems from monitoring or adjust the rule to recognize their activity as normal.
- Educational or training sessions involving compilers might cause alerts. Temporarily adjust the rule settings or add exceptions for the duration of the training.
- Users compiling open-source software for personal use can be mistaken for threats. Implement a process for users to notify the security team of legitimate compiler use to preemptively adjust monitoring rules.
- System administrators performing maintenance or updates that involve compiling software may trigger alerts. Maintain a log of scheduled maintenance activities and adjust the rule to account for these periods.

### Response and remediation

- Isolate the affected system from the network to prevent potential lateral movement or further exploitation.
- Terminate any suspicious processes associated with the anomalous compiler activity to halt any ongoing malicious operations.
- Conduct a thorough review of recent user activity and permissions to identify unauthorized access or privilege escalation attempts.
- Remove any unauthorized or malicious software identified during the investigation to prevent further compromise.
- Restore the system from a known good backup if malicious code execution is confirmed, ensuring that the backup is free from compromise.
- Implement stricter access controls and monitoring for compiler usage, ensuring only authorized users can execute compilers.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are affected.
