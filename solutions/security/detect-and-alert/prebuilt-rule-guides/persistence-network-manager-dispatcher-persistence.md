---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "NetworkManager Dispatcher Script Creation" prebuilt detection rule.
---

# NetworkManager Dispatcher Script Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating NetworkManager Dispatcher Script Creation

NetworkManager dispatcher scripts are executed on Linux systems when network interfaces change state, allowing for automated responses to network events. Adversaries can exploit this by creating scripts that execute malicious code, ensuring persistence and evasion. The detection rule identifies unauthorized script creation by monitoring file creation events in the dispatcher directory, excluding known legitimate processes and file types, thus highlighting potential abuse.

### Possible investigation steps

- Review the file creation event details to identify the specific script created in the /etc/NetworkManager/dispatcher.d/ directory, noting the file path and name.
- Examine the process that created the script by checking the process.executable field to determine if it is an unexpected or suspicious process not listed in the known legitimate processes.
- Investigate the contents of the newly created script to identify any potentially malicious code or commands that could indicate an attempt to maintain persistence or execute unauthorized actions.
- Check the system's recent network events and changes to see if the script has been triggered and executed, which could provide further context on its intended use.
- Correlate the event with other security alerts or logs from the same host to identify any related suspicious activities or patterns that could indicate a broader attack or compromise.

### False positive analysis

- Package management tools like dpkg, rpm, and yum may trigger false positives when they create or modify dispatcher scripts during software installations or updates. To handle these, ensure that the process executables for these tools are included in the exclusion list within the detection rule.
- Automated system management tools such as Puppet, Chef, and Ansible can also cause false positives when they deploy or update configurations. Verify that the executables for these tools are part of the exclusion criteria to prevent unnecessary alerts.
- Temporary files created by text editors like Vim may be mistakenly flagged. These files typically have extensions like swp or swpx. Ensure these extensions are included in the exclusion list to avoid false positives.
- Custom scripts or applications that are known to create or modify dispatcher scripts for legitimate purposes should be reviewed. If deemed safe, add their process executables to the exclusion list to prevent them from being flagged.
- Consider monitoring the frequency and context of script creation events. If certain scripts are frequently created by known processes, evaluate the need to adjust the rule to reduce noise while maintaining security efficacy.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further execution of potentially malicious scripts and limit the attacker's ability to maintain persistence.
- Review and remove any unauthorized scripts found in the /etc/NetworkManager/dispatcher.d/ directory to eliminate the immediate threat.
- Conduct a thorough examination of the system for additional signs of compromise, such as unexpected processes or network connections, to identify any further malicious activity.
- Restore any affected systems from a known good backup to ensure the removal of any persistent threats that may have been established.
- Implement stricter access controls and monitoring on the /etc/NetworkManager/dispatcher.d/ directory to prevent unauthorized script creation in the future.
- Escalate the incident to the security operations team for further investigation and to determine if the threat is part of a larger attack campaign.
- Update and enhance endpoint detection and response (EDR) solutions to improve detection capabilities for similar threats, leveraging the MITRE ATT&CK framework for guidance on persistence and execution techniques.
