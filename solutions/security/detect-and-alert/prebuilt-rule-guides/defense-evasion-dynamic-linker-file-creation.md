---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Dynamic Linker Creation" prebuilt detection rule.
---

# Dynamic Linker Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Dynamic Linker Creation or Modification

The dynamic linker in Linux systems is crucial for loading shared libraries needed by programs at runtime. Adversaries may exploit this by altering linker configuration files to hijack program execution, enabling persistence or evasion. The detection rule identifies suspicious creation or renaming of these files, excluding benign processes and extensions, to flag potential threats.

### Possible investigation steps

- Review the file path involved in the alert to determine if it matches any of the critical dynamic linker configuration files such as /etc/ld.so.preload, /etc/ld.so.conf.d/*, or /etc/ld.so.conf.
- Identify the process that triggered the alert by examining the process.executable field and verify if it is listed as a benign process in the exclusion list. If not, investigate the legitimacy of the process.
- Check the file extension and file.Ext.original.extension fields to ensure the file is not a temporary or expected system file, such as those with extensions like swp, swpx, swx, or dpkg-new.
- Investigate the process.name field to determine if the process is a known system utility like java, sed, or perl, and assess if its usage in this context is typical or suspicious.
- Gather additional context by reviewing recent system logs and other security alerts to identify any related or preceding suspicious activities that might indicate a broader attack or compromise.

### False positive analysis

- Package management operations can trigger false positives when legitimate package managers like dpkg, rpm, or yum modify linker configuration files. To handle this, ensure these processes are included in the exclusion list to prevent unnecessary alerts.
- System updates or software installations often involve temporary file modifications with extensions like swp or dpkg-new. Exclude these extensions to reduce false positives.
- Automated system management tools such as Puppet or Chef may modify linker files as part of their configuration management tasks. Add these tools to the exclusion list to avoid false alerts.
- Virtualization and containerization platforms like Docker or VMware may alter linker configurations during normal operations. Verify these processes and exclude them if they are part of routine system behavior.
- Custom scripts or applications that use common names like sed or perl might be flagged if they interact with linker files. Review these scripts and consider excluding them if they are verified as safe.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Review and restore the original dynamic linker configuration files from a known good backup to ensure the integrity of the system's execution flow.
- Conduct a thorough scan of the affected system using updated antivirus and anti-malware tools to identify and remove any additional malicious software or scripts.
- Analyze system logs and the process execution history to identify the source of the unauthorized changes and determine if any other systems may be compromised.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to assess the potential impact on the organization.
- Implement additional monitoring on the affected system and similar systems to detect any future attempts to modify dynamic linker configuration files.
- Review and update access controls and permissions to ensure that only authorized personnel have the ability to modify critical system files, reducing the risk of similar incidents in the future.
