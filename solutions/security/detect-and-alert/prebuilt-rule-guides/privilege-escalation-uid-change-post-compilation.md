---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Privilege Escalation via Recently Compiled Executable" prebuilt detection rule.'
---

# Potential Privilege Escalation via Recently Compiled Executable

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Privilege Escalation via Recently Compiled Executable

In Linux environments, compiling and executing programs is a routine operation. However, adversaries can exploit this by compiling malicious code to escalate privileges. This detection rule identifies suspicious sequences where a non-root user compiles and executes a program, followed by a UID change to root, indicating potential privilege escalation attempts. By monitoring these patterns, the rule helps in identifying and mitigating exploitation risks.

### Possible investigation steps

- Review the alert details to identify the specific non-root user involved in the compilation and execution sequence. Check the user.id field to gather more information about the user's activities and permissions.
- Examine the process.args field from the initial compilation event to understand the source code or script being compiled. This can provide insights into whether the code has malicious intent.
- Investigate the file.name field associated with the creation event to determine the nature of the executable file created. Check its location and any associated metadata for anomalies.
- Analyze the process.name field from the execution event to identify the program that was run. Cross-reference this with known malicious binaries or scripts.
- Check the process.name field in the UID change event to identify the process responsible for the privilege escalation. Determine if this process is known to exploit vulnerabilities for privilege escalation.
- Review system logs and other security tools for any additional suspicious activities or anomalies around the time of the alert to gather more context on the potential threat.
- Assess the system for any signs of compromise or unauthorized changes, such as new user accounts, altered configurations, or unexpected network connections, to evaluate the impact and scope of the incident.

### False positive analysis

- Development activities by legitimate users can trigger this rule when compiling and testing new software. To manage this, consider creating exceptions for specific users or groups known to perform regular development tasks.
- Automated build systems or continuous integration pipelines may compile and execute code as part of their normal operation. Exclude these systems by identifying their user accounts or host identifiers.
- System administrators performing maintenance or updates might compile and execute programs, leading to false positives. Implement exceptions for these users or specific maintenance windows.
- Educational environments where students frequently compile and execute code for learning purposes can generate alerts. Exclude these activities by setting up exceptions for student user accounts or specific lab environments.
- Security testing and research activities that involve compiling and executing exploit code in a controlled manner can be mistaken for malicious behavior. Exclude these activities by identifying the user accounts or systems involved in such testing.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or lateral movement.
- Terminate any suspicious processes identified in the alert, especially those associated with the compiled executable and any processes running with elevated privileges.
- Revert any unauthorized changes to user permissions, particularly any UID changes to root, to restore the system to its secure state.
- Conduct a thorough review of the affected system for additional indicators of compromise, such as unauthorized file modifications or new user accounts, and remove any malicious artifacts.
- Apply relevant security patches and updates to the system to address any vulnerabilities that may have been exploited for privilege escalation.
- Monitor the affected system and network for any signs of recurring or related suspicious activity, using enhanced logging and alerting mechanisms.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems may be affected, ensuring comprehensive remediation across the environment.
