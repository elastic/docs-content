---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Communication App Child Process" prebuilt detection rule.
---

# Suspicious Communication App Child Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Communication App Child Process

Communication apps like Slack, WebEx, and Teams are integral to modern workflows, facilitating collaboration. However, adversaries can exploit these apps by spawning unauthorized child processes, potentially masquerading as legitimate ones or exploiting vulnerabilities to execute malicious code. The detection rule identifies such anomalies by monitoring child processes of these apps, ensuring they are trusted and signed by recognized entities. This helps in identifying potential threats that deviate from expected behavior, thus safeguarding against unauthorized access and execution.

### Possible investigation steps

- Review the process details, including the parent process name and executable path, to confirm if the child process is expected or unusual for the communication app in question.
- Check the code signature of the suspicious child process to determine if it is trusted and signed by a recognized entity, as specified in the query.
- Investigate the command line arguments of the child process to identify any potentially malicious or unexpected commands being executed.
- Correlate the event with other logs or alerts to identify any related suspicious activities or patterns, such as repeated unauthorized child process executions.
- Assess the user account associated with the process to determine if it has been compromised or is exhibiting unusual behavior.
- Examine the network activity of the affected system to identify any suspicious outbound connections that may indicate data exfiltration or communication with a command and control server.

### False positive analysis

- Legitimate software updates or installations may trigger the rule if they spawn child processes from communication apps. Users can create exceptions for known update processes by verifying their code signatures and paths.
- Custom scripts or automation tools that interact with communication apps might be flagged. Users should ensure these scripts are signed and located in trusted directories, then add them to the exception list.
- Certain administrative tasks, such as using command-line tools like cmd.exe or powershell.exe, may be mistakenly identified as suspicious. Users can whitelist specific command lines or arguments that are regularly used in their environment.
- Some third-party integrations with communication apps may generate child processes that are not inherently malicious. Users should verify the legitimacy of these integrations and add them to the trusted list if they are deemed safe.
- Regularly review and update the list of trusted code signatures and executable paths to ensure that legitimate processes are not inadvertently flagged as suspicious.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or execution of malicious code.
- Terminate any suspicious child processes identified by the detection rule that are not signed by recognized entities or are executing from unexpected locations.
- Conduct a thorough review of the affected communication app's logs and configurations to identify any unauthorized changes or access patterns.
- Restore the affected system from a known good backup if malicious activity is confirmed, ensuring that the backup is free from compromise.
- Update the communication app and all related software to the latest versions to patch any known vulnerabilities that may have been exploited.
- Implement application whitelisting to ensure only trusted and signed applications can execute, reducing the risk of similar threats.
- Escalate the incident to the security operations center (SOC) or relevant security team for further investigation and to assess the potential impact on other systems.
