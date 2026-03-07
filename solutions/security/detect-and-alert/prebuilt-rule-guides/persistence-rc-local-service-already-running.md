---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Execution of rc.local Script" prebuilt detection rule.
---

# Potential Execution of rc.local Script

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Execution of rc.local Script

The `/etc/rc.local` script is a legacy Linux initialization script executed at the end of the boot process. While not enabled by default, attackers can exploit it to persistently run malicious commands upon system reboot. The detection rule identifies potential misuse by monitoring for the `already_running` event action linked to `rc-local.service`, indicating the script's execution, thus alerting to possible persistence tactics.

### Possible investigation steps

- Review the system logs to identify any recent changes or modifications to the /etc/rc.local file, focusing on timestamps and user accounts involved in the changes.
- Examine the contents of the /etc/rc.local file to identify any suspicious or unauthorized commands or scripts that may have been added.
- Investigate the process tree and parent processes associated with the rc-local.service to determine if there are any unusual or unexpected parent processes that could indicate compromise.
- Check for any other persistence mechanisms or indicators of compromise on the system, such as unauthorized user accounts or scheduled tasks, to assess the broader impact of the potential threat.
- Correlate the event with other security alerts or logs from the same host to identify any patterns or related activities that could provide additional context or evidence of malicious behavior.

### False positive analysis

- System maintenance scripts: Some Linux distributions or administrators may use the rc.local script for legitimate system maintenance tasks. Review the script's content to verify its purpose and consider excluding these known benign scripts from triggering alerts.
- Custom startup configurations: Organizations might have custom startup configurations that utilize rc.local for non-malicious purposes. Document these configurations and create exceptions in the detection rule to prevent unnecessary alerts.
- Legacy applications: Certain legacy applications might rely on rc.local for initialization. Identify these applications and assess their necessity. If deemed safe, exclude their execution from the rule to reduce false positives.
- Testing environments: In testing or development environments, rc.local might be used for various non-threatening experiments. Clearly label these environments and adjust the rule to ignore alerts originating from them.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further execution of potentially malicious scripts and limit the attacker's access.
- Review the contents of the `/etc/rc.local` file on the affected system to identify any unauthorized or suspicious commands or scripts. Remove any malicious entries found.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection tools to identify and remove any additional malware or persistence mechanisms.
- Restore the system from a known good backup if the integrity of the system is in question and if malicious activity is confirmed.
- Implement monitoring for changes to the `/etc/rc.local` file and other critical system files to detect unauthorized modifications in the future.
- Escalate the incident to the security operations team for further investigation and to determine if other systems may be affected.
- Review and update security policies and configurations to disable the execution of the `/etc/rc.local` script by default on all systems, unless explicitly required for legitimate purposes.
