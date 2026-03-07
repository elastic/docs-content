---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential SAP NetWeaver WebShell Creation" prebuilt detection rule.
---

# Potential SAP NetWeaver WebShell Creation

## Triage and analysis

### Investigating Potential SAP NetWeaver WebShell Creation

### Possible investigation steps

- Examine the file creation event and the associated HTTP post request logs details to identify the source of the creation.
- Examine the process tree to verify the parent-child relationship between the Java process and any suspicious child processes such as shell scripts or scripting languages (e.g., sh, bash, curl, python).
- Check the command line arguments and environment variables of the suspicious child processes to identify any potentially malicious payloads or commands being executed.
- Investigate the host's recent activity and logs for any other indicators of compromise or unusual behavior that might correlate with the suspected exploitation attempt.
- Assess the system for any unauthorized changes or new files that may have been introduced as a result of the exploitation attempt, focusing on JSP files under the IRJ root directory.


### Response and remediation

- Immediately isolate the affected host from the network to prevent further outbound connections and potential lateral movement.
- Terminate any suspicious Java processes identified in the alert, especially those making outbound connections to LDAP, RMI, or DNS ports.
- Conduct a thorough review of the affected system for any unauthorized changes or additional malicious processes, focusing on child processes like shell scripts or scripting languages.
- Restore the affected system from a known good backup if unauthorized changes or malware are detected.
- Update and patch Java and any related applications to the latest versions to mitigate known vulnerabilities.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to assess the potential impact on other systems within the network.
