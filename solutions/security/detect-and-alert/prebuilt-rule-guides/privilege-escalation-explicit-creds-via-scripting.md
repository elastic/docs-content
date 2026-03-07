---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Execution with Explicit Credentials via Scripting" prebuilt detection rule.'
---

# Execution with Explicit Credentials via Scripting

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Execution with Explicit Credentials via Scripting

In macOS environments, the `security_authtrampoline` process is used to execute programs with elevated privileges via scripting interpreters. Adversaries may exploit this by using explicit credentials to run unauthorized scripts, gaining root access. The detection rule identifies such activities by monitoring the initiation of `security_authtrampoline` through common scripting languages, flagging potential privilege escalation attempts.

### Possible investigation steps

- Review the process details to confirm the parent process name matches one of the specified scripting interpreters (e.g., osascript, bash, python) to verify the context of the alert.
- Examine the command line arguments of the security_authtrampoline process to identify the script or program being executed and assess its legitimacy.
- Investigate the user account associated with the process to determine if the credentials used are valid and expected for executing such scripts.
- Check the historical activity of the involved user account and associated processes to identify any patterns of unusual or unauthorized behavior.
- Correlate the alert with other security events or logs from the same host to identify any additional indicators of compromise or related suspicious activities.
- Assess the system for any signs of compromise or unauthorized changes, such as unexpected new files, altered configurations, or additional unauthorized processes running.

### False positive analysis

- Legitimate administrative tasks using scripting languages may trigger this rule. Users should review the context of the script execution to determine if it aligns with expected administrative activities.
- Automated scripts or scheduled tasks that require elevated privileges might be flagged. Consider creating exceptions for known scripts by specifying their hash or path in the monitoring system.
- Development or testing environments where developers frequently use scripting languages to test applications with elevated privileges can cause false positives. Implement a policy to exclude these environments from the rule or adjust the risk score to reflect the lower threat level.
- Security tools or software updates that use scripting interpreters to perform legitimate actions with elevated privileges may be mistakenly identified. Verify the source and purpose of such processes and whitelist them if they are deemed safe.
- User-initiated scripts for personal productivity that require elevated access could be misinterpreted as threats. Educate users on safe scripting practices and establish a process for them to report and document legitimate use cases for exclusion.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent further unauthorized access or lateral movement.
- Terminate the `security_authtrampoline` process if it is still running to stop any ongoing unauthorized activities.
- Review and revoke any compromised credentials used in the execution of the unauthorized script to prevent further misuse.
- Conduct a thorough examination of the system for any additional unauthorized scripts or malware that may have been deployed using the compromised credentials.
- Restore the system from a known good backup if any unauthorized changes or persistent threats are detected.
- Implement stricter access controls and monitoring for the use of scripting interpreters and the `security_authtrampoline` process to prevent similar privilege escalation attempts.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on other systems within the network.
