---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Privilege Escalation via Enlightenment" prebuilt detection rule.'
---

# Potential Privilege Escalation via Enlightenment

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Privilege Escalation via Enlightenment

Enlightenment, a Linux window manager, can be exploited for privilege escalation due to a flaw in its setuid root configuration. Attackers may exploit this by manipulating pathnames, gaining unauthorized root access. The detection rule identifies suspicious execution of 'enlightenment_sys' with specific arguments and subsequent UID changes to root, flagging potential exploitation attempts.

### Possible investigation steps

- Review the alert details to confirm the presence of the process "enlightenment_sys" with the specified arguments ("/bin/mount/", "-o", "noexec", "nosuid", "nodev", "uid=*") on a Linux host.
- Check the process execution timeline to verify if the suspicious "enlightenment_sys" execution was followed by a UID change to root (user.id == "0") within a 5-second window.
- Investigate the host.id and process.parent.entity_id to identify the parent process and determine if it was initiated by a legitimate user or service.
- Examine the system logs around the time of the alert to identify any other unusual activities or related processes that might indicate a broader attack or exploitation attempt.
- Assess the affected system for any unauthorized changes or signs of compromise, focusing on privilege escalation indicators and potential persistence mechanisms.
- Review user access logs and permissions to determine if the user associated with the process had legitimate reasons to execute "enlightenment_sys" with elevated privileges.
- Consider isolating the affected system to prevent further exploitation and begin remediation steps, such as applying patches or configuration changes to mitigate the vulnerability.

### False positive analysis

- Legitimate administrative tasks using enlightenment_sys may trigger the rule. Review the context of the execution, such as the user and the specific arguments used, to determine if the activity is authorized.
- Automated scripts or system maintenance processes that involve enlightenment_sys with similar arguments might be flagged. Identify these scripts and consider excluding them by specifying their process hashes or paths in the detection rule.
- System updates or package installations that temporarily change UID to root could be misinterpreted as exploitation attempts. Monitor these activities and whitelist known update processes to prevent false alerts.
- Custom user applications that interact with enlightenment_sys for legitimate purposes may cause false positives. Evaluate these applications and, if deemed safe, add them to an exception list based on their unique identifiers.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement.
- Terminate any suspicious processes related to 'enlightenment_sys' that are running with elevated privileges to stop ongoing exploitation.
- Conduct a thorough review of system logs to identify any unauthorized changes or access patterns, focusing on UID changes to root.
- Revoke any unauthorized access or privileges granted during the exploitation, ensuring that only legitimate users have root access.
- Apply the latest security patches and updates to the Enlightenment package, specifically upgrading to version 0.25.4 or later to mitigate the vulnerability.
- Implement file integrity monitoring to detect unauthorized changes to critical system files and configurations in the future.
- Escalate the incident to the security operations team for further investigation and to assess the potential impact on other systems within the network.
