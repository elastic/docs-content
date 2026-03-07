---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Process Injection - Prevented - Elastic Endgame" prebuilt detection rule.
---

# Process Injection - Prevented - Elastic Endgame

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Process Injection - Prevented - Elastic Endgame

Elastic Endgame is a security solution that prevents malicious activities like process injection, a technique often used by adversaries to execute code within the address space of another process, enabling privilege escalation. This detection rule identifies attempts by monitoring alerts for specific kernel shellcode events, indicating potential injection attempts, and helps mitigate threats by leveraging prevention capabilities.

### Possible investigation steps

- Review the alert details to confirm the presence of event.kind:alert and event.module:endgame, ensuring the alert is related to Elastic Endgame's prevention capabilities.
- Examine the event.action and endgame.event_subtype_full fields for kernel_shellcode_event to identify the specific type of process injection attempt.
- Investigate the source process and target process involved in the injection attempt to understand the context and potential impact on the system.
- Check for any associated alerts or logs around the same timeframe to identify if this is part of a larger attack pattern or isolated incident.
- Assess the risk score and severity to prioritize the investigation and determine if immediate action is required to mitigate potential threats.
- Consult the MITRE ATT&CK framework for additional context on the T1055 Process Injection technique to understand common methods and potential mitigations.

### False positive analysis

- Legitimate software updates or installations may trigger kernel shellcode events. Users can create exceptions for known update processes by identifying their unique process identifiers or paths.
- Security tools or monitoring software that perform deep system scans might mimic process injection behavior. Exclude these tools by specifying their executable names or hashes in the exception list.
- Custom scripts or automation tools that interact with system processes could be flagged. Review these scripts and whitelist them if they are verified as safe and necessary for operations.
- Development environments or debugging tools that inject code for testing purposes may cause alerts. Establish exceptions for these environments by defining rules based on the development tools' signatures or process names.
- Virtualization software that uses process injection techniques for managing virtual machines can be mistakenly identified. Add these applications to the exclusion list by recognizing their specific process attributes.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Terminate any suspicious processes identified by the alert, particularly those associated with the kernel shellcode event, to halt ongoing malicious actions.
- Conduct a thorough analysis of the affected system to identify any additional indicators of compromise or secondary payloads that may have been deployed.
- Restore the affected system from a known good backup to ensure any injected code or malicious modifications are removed.
- Apply security patches and updates to the operating system and all installed software to close any vulnerabilities that may have been exploited.
- Monitor the network and systems for any signs of similar process injection attempts, using enhanced logging and alerting based on the identified threat indicators.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
