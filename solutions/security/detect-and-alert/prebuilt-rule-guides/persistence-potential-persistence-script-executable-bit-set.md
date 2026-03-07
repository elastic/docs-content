---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Executable Bit Set for Potential Persistence Script" prebuilt detection rule.
---

# Executable Bit Set for Potential Persistence Script

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Executable Bit Set for Potential Persistence Script

In Linux environments, scripts with executable permissions can be used to automate tasks, including system start-up processes. Adversaries exploit this by setting executable bits on scripts in directories typically used for persistence, allowing malicious code to run automatically. The detection rule identifies such activities by monitoring for changes in executable permissions in these directories, signaling potential unauthorized persistence attempts.

### Possible investigation steps

- Review the process details to identify the specific script or file that had its executable bit set, focusing on the process.args field to determine the exact file path.
- Examine the process.parent.executable field to understand the parent process that initiated the permission change, which can provide context on whether the action was part of a legitimate process or potentially malicious activity.
- Check the user account associated with the process to determine if the action was performed by a legitimate user or a compromised account.
- Investigate the history of the file in question, including recent modifications and the creation date, to assess if it aligns with known system changes or updates.
- Analyze the contents of the script or file to identify any suspicious or unauthorized code that could indicate malicious intent.
- Correlate this event with other recent alerts or logs from the same host to identify patterns or additional indicators of compromise that may suggest a broader persistence mechanism.

### False positive analysis

- System administrators or automated scripts may legitimately change executable permissions in directories like /etc/init.d or /etc/cron* for maintenance or updates. To handle these, create exceptions for known administrative scripts or processes that regularly perform these actions.
- Software installations or updates might trigger this rule when they modify startup scripts or configuration files. Users can mitigate this by excluding processes originating from trusted package managers or installation paths, such as /var/lib/dpkg.
- Custom user scripts in home directories, especially in /home/*/.config/autostart, may be flagged if users set them to run at startup. To reduce false positives, maintain a whitelist of user scripts that are known and approved for startup execution.
- Security tools or monitoring solutions might adjust permissions as part of their operations. Identify these tools and exclude their processes from triggering the rule to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent potential lateral movement by the adversary.
- Terminate any suspicious processes identified in the alert that are associated with unauthorized script execution.
- Remove or disable the executable permissions on the identified scripts to prevent further unauthorized execution.
- Conduct a thorough review of the affected directories to identify and remove any additional unauthorized scripts or files.
- Restore any modified system files or configurations from a known good backup to ensure system integrity.
- Monitor the system for any signs of re-infection or further unauthorized changes, focusing on the directories and processes highlighted in the alert.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
