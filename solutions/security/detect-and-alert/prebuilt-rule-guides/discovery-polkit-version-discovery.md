---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Polkit Version Discovery" prebuilt detection rule.
---

# Polkit Version Discovery

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Polkit Version Discovery

Polkit, a system service in Linux, manages system-wide privileges, enabling non-privileged processes to communicate with privileged ones. Adversaries may exploit Polkit by discovering its version to identify vulnerabilities or misconfigurations. The detection rule identifies suspicious activities by monitoring specific command executions related to Polkit version checks, signaling potential reconnaissance efforts by attackers.

### Possible investigation steps

- Review the process execution details to confirm the command used for Polkit version discovery, focusing on the process name and arguments such as "dnf", "rpm", "apt", or "pkaction".
- Check the user account associated with the process execution to determine if it is a legitimate user or potentially compromised.
- Investigate the host from which the command was executed to assess if it has a history of suspicious activities or if it is a high-value target.
- Correlate the event with other logs or alerts to identify if there are additional indicators of compromise or related reconnaissance activities.
- Evaluate the necessity and frequency of Polkit version checks in the environment to determine if this behavior is expected or anomalous.

### False positive analysis

- Routine system updates or package management activities may trigger the rule when administrators use package managers like dnf, rpm, or apt to check for updates or verify installed packages. To mitigate this, create exceptions for known administrative scripts or user accounts that regularly perform these actions.
- Automated system monitoring tools that check software versions for compliance or inventory purposes might also cause false positives. Identify these tools and exclude their processes from triggering the rule.
- Developers or system administrators testing Polkit configurations or updates might execute version checks as part of their workflow. Consider excluding specific user accounts or process paths associated with development and testing environments.
- Security audits or vulnerability assessments conducted by internal teams may involve version checks as part of their procedures. Coordinate with these teams to whitelist their activities during scheduled assessments.

### Response and remediation

- Isolate the affected system from the network to prevent potential lateral movement by the attacker.
- Terminate any suspicious processes identified in the alert, such as those involving the execution of Polkit version discovery commands.
- Conduct a thorough review of system logs and command history to identify any unauthorized access or further malicious activities.
- Apply any available security patches or updates to the Polkit service to address known vulnerabilities.
- Implement stricter access controls and monitoring on systems running Polkit to prevent unauthorized version checks and other reconnaissance activities.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Enhance detection capabilities by configuring alerts for similar reconnaissance activities across the network to ensure early detection of potential threats.
