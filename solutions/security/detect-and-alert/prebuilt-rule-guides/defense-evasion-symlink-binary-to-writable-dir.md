---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "System Binary Symlink to Suspicious Location" prebuilt detection rule.'
---

# System Binary Symlink to Suspicious Location

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating System Binary Symlink to Suspicious Location

Symbolic links in Linux create shortcuts to files or directories, allowing flexible file management. Adversaries exploit this by linking system binaries to writable, suspicious locations, aiming to bypass security measures that monitor standard execution paths. The detection rule identifies unusual parent processes and symbolic link creation to these locations, flagging potential evasion attempts.

### Possible investigation steps

- Review the parent process executable (process.parent.executable) to determine if it is a known and legitimate process that should be creating symbolic links.
- Examine the specific system binary involved (process.args) to verify if it is commonly used in the environment and assess if its redirection to a suspicious location is justified.
- Investigate the destination path of the symbolic link (process.args) to determine if it is a writable and potentially malicious location such as /tmp, /dev/shm, or /var/tmp.
- Check for any recent or concurrent alerts or logs related to the same parent process or destination path to identify potential patterns or repeated attempts.
- Assess the user account associated with the process (if available) to determine if it has the necessary permissions and if the activity aligns with the user's typical behavior.
- Correlate with other security tools or logs to identify any additional suspicious activities or anomalies around the time of the alert.

### False positive analysis

- Routine system maintenance tasks may create symbolic links in monitored directories. Exclude known maintenance scripts or processes like mkinitcpio and dracut from triggering alerts by adding them to the exception list.
- Software installations or updates often involve creating symbolic links in writable directories. Identify and whitelist trusted installation processes or package managers to prevent unnecessary alerts.
- Development environments may frequently use symbolic links for testing purposes. Consider excluding specific user directories or development tools that are known to create such links regularly.
- Backup or synchronization tools might create symbolic links as part of their operation. Verify and exclude these tools if they are part of a legitimate and routine process.
- Custom scripts or automation tools used within the organization might trigger this rule. Review and whitelist these scripts if they are verified to be safe and necessary for business operations.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Terminate any suspicious processes identified as creating symbolic links to writable locations, especially those with uncommon parent processes.
- Remove any unauthorized symbolic links from system binaries to suspicious locations, ensuring the integrity of the original binaries.
- Conduct a thorough review of user accounts and permissions on the affected system to identify and disable any compromised accounts or unnecessary elevated privileges.
- Restore affected binaries and system files from a known good backup to ensure no tampered files remain.
- Monitor the system for any further attempts to create unauthorized symbolic links, using enhanced logging and alerting mechanisms.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
