---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unknown Execution of Binary with RWX Memory Region" prebuilt detection rule.
---

# Unknown Execution of Binary with RWX Memory Region

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unknown Execution of Binary with RWX Memory Region

In Linux environments, the `mprotect()` system call is crucial for managing memory permissions, allowing processes to modify access rights of memory pages. Adversaries exploit this by granting read, write, and execute (RWX) permissions to inject and execute malicious code. The detection rule identifies suspicious RWX memory allocations by monitoring `mprotect()` calls, excluding known safe binaries, thus highlighting potential threats.

### Possible investigation steps

- Review the process details associated with the alert, focusing on the process.executable and process.name fields to identify the binary that triggered the alert.
- Investigate the command line arguments and parent process of the suspicious binary to understand its origin and purpose.
- Check the process's hash against known threat intelligence databases to determine if it is associated with any known malicious activity.
- Analyze the network activity of the process to identify any suspicious connections or data exfiltration attempts.
- Examine the user account under which the process is running to assess if it has been compromised or is being used for unauthorized activities.
- Review recent system logs and audit records for any other anomalies or related suspicious activities around the time of the alert.

### False positive analysis

- Known safe binaries like Node.js, Java, and Apache may trigger the rule due to their legitimate use of RWX memory regions. These are already excluded in the rule, but additional similar applications might need to be added to the exclusion list.
- Custom or in-house developed applications that require RWX permissions for legitimate functionality can also cause false positives. Identify these applications and add them to the exclusion list to prevent unnecessary alerts.
- Development environments or testing frameworks that dynamically generate and execute code might be flagged. Consider excluding these environments if they are known and trusted within your organization.
- Security tools or monitoring software that perform memory analysis or manipulation could be mistakenly identified. Verify their behavior and exclude them if they are part of your security infrastructure.
- Regularly review and update the exclusion list to ensure it reflects the current environment and any new applications that are introduced.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential lateral movement or data exfiltration by the malicious code.
- Terminate the suspicious process identified by the detection rule to halt any ongoing malicious activity.
- Conduct a forensic analysis of the affected system to identify the source and scope of the compromise, focusing on the unknown binary and its origin.
- Remove any malicious binaries or scripts identified during the forensic analysis to prevent further execution.
- Apply security patches and updates to the affected system to address any vulnerabilities that may have been exploited.
- Restore the system from a known good backup if the integrity of the system is in question and ensure all security patches are applied post-restoration.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
