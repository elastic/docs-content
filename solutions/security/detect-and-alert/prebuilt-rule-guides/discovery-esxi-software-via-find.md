---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "ESXI Discovery via Find" prebuilt detection rule.
---

# ESXI Discovery via Find

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating ESXI Discovery via Find

VMware ESXi is a hypervisor used to deploy and manage virtual machines. Adversaries may exploit the 'find' command on Linux systems to locate VM-related files, potentially to gather information or manipulate configurations. The detection rule identifies suspicious 'find' command executions targeting VMware paths, excluding legitimate processes, to flag potential reconnaissance activities.

### Possible investigation steps

- Review the process execution details to confirm the 'find' command was executed with arguments targeting VMware paths such as "/etc/vmware/*", "/usr/lib/vmware/*", or "/vmfs/*".
- Check the parent process of the 'find' command to ensure it is not "/usr/lib/vmware/viewagent/bin/uninstall_viewagent.sh", which is excluded from the rule as a legitimate process.
- Investigate the user account associated with the 'find' command execution to determine if it is a known and authorized user for VMware management tasks.
- Examine recent login and access logs for the user account to identify any unusual or unauthorized access patterns.
- Correlate this event with other security alerts or logs to identify if there are additional signs of reconnaissance or unauthorized activity on the system.
- Assess the system's current state and configuration to ensure no unauthorized changes have been made to VMware-related files or settings.

### False positive analysis

- Legitimate administrative tasks may trigger the rule if system administrators use the 'find' command to audit or manage VMware-related files. To handle this, create exceptions for known administrative scripts or user accounts that regularly perform these tasks.
- Automated backup or monitoring scripts that scan VMware directories can also cause false positives. Identify these scripts and exclude their parent processes from the detection rule.
- Software updates or maintenance activities involving VMware components might execute the 'find' command in a non-threatening manner. Consider scheduling these activities during known maintenance windows and temporarily adjusting the rule to prevent unnecessary alerts.
- If the 'find' command is part of a legitimate software installation or uninstallation process, such as the VMware View Agent uninstallation, ensure these processes are whitelisted by adding their parent executable paths to the exception list.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious 'find' processes identified in the alert to halt potential reconnaissance activities.
- Conduct a thorough review of the system's recent command history and logs to identify any unauthorized access or changes made to VM-related files.
- Restore any altered or deleted VM-related files from a known good backup to ensure system integrity.
- Update and patch the VMware ESXi and related software to the latest versions to mitigate any known vulnerabilities.
- Implement stricter access controls and monitoring on VMware-related directories to prevent unauthorized access in the future.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
