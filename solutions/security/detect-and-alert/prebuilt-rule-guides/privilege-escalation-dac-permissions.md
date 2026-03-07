---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Privilege Escalation via Linux DAC permissions" prebuilt detection rule.'
---

# Potential Privilege Escalation via Linux DAC permissions

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Privilege Escalation via Linux DAC permissions

Linux Discretionary Access Control (DAC) allows file owners to set permissions, potentially leading to privilege escalation if misconfigured. Adversaries exploit DAC by using processes with capabilities like CAP_DAC_OVERRIDE to bypass permission checks. The detection rule identifies suspicious processes accessing sensitive files, excluding benign activities, to flag potential misuse of DAC permissions.

### Possible investigation steps

- Review the process command line to identify the specific command executed and determine if it involves sensitive files like sudoers, passwd, shadow, or directories under /root/.
- Check the user ID associated with the process to verify if it is a non-root user attempting to access or modify sensitive files.
- Investigate the process name and executable path to ensure it is not part of the excluded benign processes or paths, such as tar, getent, or /usr/lib/*/lxc/rootfs/*.
- Analyze the parent process name to determine if it is a known benign parent like dpkg or gnome-shell, which might indicate a legitimate operation.
- Examine the process thread capabilities, specifically CAP_DAC_OVERRIDE or CAP_DAC_READ_SEARCH, to understand the level of access the process has and assess if it aligns with expected behavior for the user or application.
- Correlate the event with other logs or alerts to identify any patterns or sequences of activities that might indicate a broader attack or misconfiguration issue.

### False positive analysis

- Processes like "tar", "getent", "su", and others listed in the rule are known to perform legitimate operations on sensitive files. Exclude these processes from triggering alerts by adding them to the exception list in the detection rule.
- System management tools such as "dpkg" and "podman" may access sensitive files during routine operations. Consider excluding these tools if they are part of regular system maintenance activities.
- Processes running under user ID "0" (root) are often legitimate and necessary for system operations. Ensure that these are excluded from alerts to avoid unnecessary noise.
- Executables located in paths like /usr/lib/*/lxc/rootfs/* are typically part of containerized environments and may not pose a threat. Exclude these paths if they are part of your standard infrastructure.
- Parent processes such as "java" or those with names ending in "postinst" may be involved in legitimate software installations or updates. Review and exclude these if they are part of expected system behavior.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified by the detection rule, especially those with CAP_DAC_OVERRIDE or CAP_DAC_READ_SEARCH capabilities accessing sensitive files.
- Conduct a thorough review of the affected system's user accounts and permissions to identify and revoke any unauthorized privilege escalations.
- Restore any modified or compromised sensitive files, such as /etc/passwd or /etc/shadow, from a known good backup.
- Implement additional monitoring on the affected system to detect any further attempts at privilege escalation or unauthorized access.
- Escalate the incident to the security operations team for a comprehensive investigation to determine the root cause and potential impact.
- Apply security patches and updates to the affected system to mitigate any known vulnerabilities that could be exploited for privilege escalation.
