---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Git Hook Created or Modified" prebuilt detection rule.'
---

# Git Hook Created or Modified

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Git Hook Created or Modified

Git hooks are scripts that automate tasks by executing before or after Git events like commits or pushes. While beneficial for developers, adversaries can exploit them to execute malicious code, maintaining persistence on a system. The detection rule identifies suspicious creation or modification of Git hooks on Linux, excluding benign processes, to flag potential abuse.

### Possible investigation steps

- Review the file path to confirm the location of the modified or created Git hook file and determine if it aligns with known repositories or projects on the system.
- Identify the process executable responsible for the creation or modification of the Git hook file and verify if it is a known and legitimate process, excluding those listed in the query.
- Check the timestamp of the event to correlate with any known user activities or scheduled tasks that might explain the modification or creation of the Git hook.
- Investigate the user account associated with the process that triggered the alert to determine if the activity aligns with their typical behavior or if it appears suspicious.
- Examine the contents of the modified or newly created Git hook file to identify any potentially malicious code or unexpected changes.
- Cross-reference the event with other security logs or alerts to identify any related suspicious activities or patterns that might indicate a broader attack or compromise.

### False positive analysis

- System package managers like dpkg, rpm, and yum can trigger false positives when they create or modify Git hooks during package installations or updates. To manage this, ensure these executables are included in the exclusion list within the detection rule.
- Automated deployment tools such as Puppet and Chef may modify Git hooks as part of their configuration management processes. Exclude these tools by adding their executables to the exception list to prevent false alerts.
- Continuous integration and deployment systems like Jenkins or GitLab runners might modify Git hooks as part of their build processes. Identify and exclude these processes by adding their specific executables or paths to the exclusion criteria.
- Custom scripts or internal tools that are known to modify Git hooks for legitimate purposes should be identified and their executables added to the exclusion list to avoid unnecessary alerts.
- Consider excluding specific directories or paths that are known to be used by trusted applications or processes for Git hook modifications, ensuring these are not flagged as suspicious.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential lateral movement or further execution of malicious code.
- Terminate any suspicious processes associated with the creation or modification of Git hooks that are not part of the known benign processes listed in the detection rule.
- Conduct a thorough review of the modified or newly created Git hook scripts to identify and remove any malicious code or unauthorized changes.
- Restore any affected Git repositories from a known good backup to ensure integrity and remove any persistence mechanisms.
- Implement file integrity monitoring on the .git/hooks directory to detect unauthorized changes in the future.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Review and update access controls and permissions for Git repositories to limit the ability to modify hook scripts to only trusted users.
