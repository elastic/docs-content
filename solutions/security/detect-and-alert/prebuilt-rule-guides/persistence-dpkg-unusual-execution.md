---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual DPKG Execution" prebuilt detection rule.
---

# Unusual DPKG Execution

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual DPKG Execution

DPKG is a core utility in Debian-based Linux systems for managing software packages. While essential for legitimate software management, adversaries can exploit DPKG to install or manipulate packages for malicious purposes, potentially gaining persistence or executing unauthorized code. The detection rule identifies anomalies by flagging DPKG executions initiated by unexpected processes, which may indicate unauthorized package management activities.

### Possible investigation steps

- Review the process details to identify the unexpected process that initiated the DPKG execution. Pay attention to the process.executable field to understand which script or binary was executed.
- Examine the process.parent.name and process.parent.executable fields to determine the parent process that launched the DPKG command. This can provide insights into whether the execution was part of a legitimate process chain or potentially malicious.
- Investigate the process.session_leader.name and process.group_leader.name fields to understand the broader context of the session and group leaders involved in the execution. This can help identify if the execution was part of a larger, coordinated activity.
- Check the system logs and any available audit logs around the time of the alert to gather additional context on the activities occurring on the system. Look for any other suspicious or related events.
- Assess the system for any unauthorized or unexpected package installations or modifications that may have occurred as a result of the DPKG execution. This can help determine if the system has been compromised.

### False positive analysis

- System maintenance scripts may trigger the rule if they execute DPKG commands outside of typical package management processes. To handle this, identify and whitelist these scripts by adding their parent process names or executables to the exception list.
- Automated software update tools, other than the ones specified in the rule, might cause false positives. Review the tools used in your environment and consider adding their executables to the exclusion criteria if they are verified as safe.
- Custom administrative scripts that manage packages could be flagged. Ensure these scripts are reviewed for legitimacy and then exclude their process names or paths from the rule to prevent unnecessary alerts.
- Development or testing environments where package manipulation is frequent might generate alerts. In such cases, consider creating environment-specific exceptions to reduce noise while maintaining security in production systems.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized package installations or potential lateral movement by the adversary.
- Terminate any suspicious processes identified as executing the DPKG command from unexpected sources to halt any ongoing malicious activities.
- Conduct a thorough review of recently installed or modified packages on the affected system to identify and remove any unauthorized or malicious software.
- Restore the system from a known good backup if malicious packages have been installed and cannot be safely removed without compromising system integrity.
- Update and patch the affected system to ensure all software is up-to-date, reducing the risk of exploitation through known vulnerabilities.
- Implement stricter access controls and monitoring on package management utilities to prevent unauthorized use, ensuring only trusted processes can execute DPKG commands.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on other systems within the network.
