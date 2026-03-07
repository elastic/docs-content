---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Process Started with Executable Stack" prebuilt detection rule.
---

# Process Started with Executable Stack

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Process Started with Executable Stack

In Linux environments, processes with executable stacks can pose security risks as they may allow code execution from the stack, a behavior often exploited by attackers to run arbitrary code. Adversaries might leverage this to execute malicious scripts or commands. The detection rule monitors syslog for kernel messages indicating such processes, flagging potential threats for further investigation.

### Possible investigation steps

- Review the syslog entries to identify the specific process that triggered the alert, focusing on the message field containing "started with executable stack".
- Investigate the process name and associated command-line arguments to understand the nature and purpose of the process.
- Check the process's parent process to determine if it was spawned by a legitimate application or service.
- Analyze the user account under which the process is running to assess if it aligns with expected behavior and permissions.
- Look for any recent changes or anomalies in the system that might correlate with the process start time, such as new software installations or configuration changes.
- Cross-reference the process with known threat intelligence sources to identify if it matches any known malicious patterns or indicators.

### False positive analysis

- Development tools and environments may intentionally use executable stacks for legitimate purposes, such as certain debugging or testing scenarios. Users can create exceptions for these specific tools by identifying their process names and excluding them from the detection rule.
- Some legacy applications might require executable stacks due to outdated coding practices. Users should verify the necessity of these applications and, if deemed non-threatening, add them to an exclusion list based on their process names or paths.
- Custom scripts or applications developed in-house might inadvertently use executable stacks. Conduct a review of these scripts to ensure they are safe, and if so, exclude them from monitoring by specifying their unique identifiers.
- Certain system utilities or libraries might trigger this rule during normal operations. Users should consult documentation or vendor support to confirm if these are expected behaviors and exclude them accordingly if they pose no risk.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential lateral movement by the attacker.
- Terminate the suspicious process identified with an executable stack to halt any ongoing malicious activity.
- Conduct a thorough analysis of the process and its associated files to identify any malicious payloads or scripts that may have been executed.
- Restore the system from a known good backup if any unauthorized changes or malware are detected.
- Apply security patches and updates to the operating system and applications to mitigate vulnerabilities that could be exploited by similar threats.
- Implement stack protection mechanisms such as stack canaries or non-executable stack configurations to prevent future exploitation.
- Escalate the incident to the security operations team for further investigation and to assess the need for additional security measures.
