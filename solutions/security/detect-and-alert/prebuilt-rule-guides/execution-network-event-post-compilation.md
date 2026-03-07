---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Network Connection via Recently Compiled Executable" prebuilt detection rule.'
---

# Network Connection via Recently Compiled Executable

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Network Connection via Recently Compiled Executable

In Linux environments, compiling and executing programs is routine for development. However, adversaries exploit this by compiling malicious code to establish reverse shells, enabling remote control. The detection rule identifies this threat by monitoring sequences of compilation, execution, and network activity, flagging unusual connections that deviate from typical patterns, thus indicating potential compromise.

### Possible investigation steps

- Review the process execution details to identify the compiler used (e.g., gcc, g++, cc) and examine the arguments passed during the compilation to understand the nature of the compiled code.
- Investigate the file creation event associated with the linker (ld) to determine the output executable file and its location on the system.
- Analyze the subsequent process execution to identify the newly compiled executable and verify its legitimacy by checking its hash against known malware databases.
- Examine the network connection attempt details, focusing on the destination IP address, to determine if it is associated with known malicious activity or command-and-control servers.
- Check the process name involved in the network connection attempt to ensure it is not a commonly used legitimate process, as specified in the query exclusions (e.g., simpleX, conftest, ssh, python, ispnull, pvtui).
- Correlate the timing of the compilation, execution, and network connection events to assess if they align with typical user behavior or indicate suspicious activity.

### False positive analysis

- Development activities involving frequent compilation and execution of new code can trigger false positives. To manage this, exclude specific user accounts or directories commonly used for legitimate development work.
- Automated build systems or continuous integration pipelines may compile and execute code regularly. Identify and exclude these processes or IP addresses from monitoring to prevent false alerts.
- Legitimate software updates or installations that involve compiling source code can be mistaken for malicious activity. Exclude known update processes or package managers from the rule.
- Network connections to internal or trusted IP addresses that are not part of the typical exclusion list might be flagged. Update the exclusion list to include these trusted IP ranges.
- Certain legitimate applications that compile and execute code as part of their normal operation, such as IDEs or scripting environments, should be identified and excluded from the rule to reduce noise.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified in the alert, especially those related to the recently compiled executable and any associated network connections.
- Conduct a forensic analysis of the affected system to identify any additional indicators of compromise, such as unauthorized user accounts or scheduled tasks.
- Remove any malicious executables or scripts identified during the investigation from the system to prevent re-execution.
- Reset credentials for any accounts that may have been compromised, focusing on those with elevated privileges.
- Update and patch the affected system to close any vulnerabilities that may have been exploited by the attacker.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
