---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Polkit Policy Creation" prebuilt detection rule.
---

# Polkit Policy Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Polkit Policy Creation

Polkit, or PolicyKit, is a system service in Linux environments that manages system-wide privileges, allowing non-privileged processes to communicate with privileged ones. Adversaries may exploit Polkit by creating or modifying policy files to gain unauthorized access or maintain persistence. The detection rule monitors the creation of these files in critical directories, excluding known legitimate processes, to identify potential malicious activity.

### Possible investigation steps

- Review the file path and extension to confirm if the created file is located in one of the critical directories specified in the query, such as /etc/polkit-1/rules.d/ or /usr/share/polkit-1/actions/.
- Identify the process executable responsible for the file creation and verify if it is listed in the exclusion list of known legitimate processes. If not, this may warrant further investigation.
- Check the timestamp of the file creation event to determine if it coincides with any known maintenance or update activities, which could explain the file creation.
- Investigate the user account associated with the process that created the file to determine if it has the necessary privileges and if the activity aligns with the user's typical behavior.
- Examine any recent changes or updates to the system that might have triggered the creation of the Polkit policy file, such as software installations or configuration changes.
- Look for any related alerts or logs that might indicate a broader pattern of suspicious activity, such as unauthorized access attempts or other policy modifications.

### False positive analysis

- System package managers like dpkg, rpm, and yum may create or modify Polkit policy files during legitimate software installations or updates. To handle these, ensure that the rule excludes processes associated with these package managers as specified in the rule's exception list.
- Container management tools such as Docker and Podman might also trigger false positives when managing containerized applications. Users should verify that these executables are included in the exclusion list to prevent unnecessary alerts.
- Automation tools like Puppet and Chef can modify policy files as part of their configuration management tasks. Confirm that these processes are part of the exclusion criteria to avoid false positives.
- Snap package installations and updates can lead to the creation of policy files. Ensure that paths related to Snap are covered in the exclusion patterns to minimize false alerts.
- Virtualization software such as VirtualBox may interact with Polkit policy files. Users should check that relevant paths and executables are included in the exceptions to reduce false positives.

### Response and remediation

- Isolate the affected system from the network to prevent further unauthorized access or lateral movement by the adversary.
- Terminate any suspicious processes identified as creating or modifying Polkit policy files, especially those not listed in the known legitimate processes.
- Review and restore the integrity of the Polkit policy files by comparing them against a known good baseline or backup to ensure no unauthorized changes persist.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malicious files or processes.
- Implement additional monitoring on the affected system and similar systems to detect any further attempts to create or modify Polkit policy files.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if the threat is part of a larger attack campaign.
- Review and update access controls and permissions related to Polkit policy files to ensure only authorized processes and users can create or modify these files, reducing the risk of future exploitation.
