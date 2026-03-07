---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential Process Name Stomping with Prctl" prebuilt detection rule.
---

# Potential Process Name Stomping with Prctl

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Process Name Stomping with Prctl

The `prctl` syscall in Linux allows processes to modify their attributes, including renaming themselves. This capability can be exploited by attackers to disguise malicious processes, making them harder to identify. The detection rule monitors for `prctl` invocations with specific arguments indicative of name changes, especially when linked to suspicious directories, thus flagging potential evasion attempts.

### Possible investigation steps

- Review the process details associated with the alert, focusing on the executable path to determine if it matches any suspicious directories listed in the query, such as "/tmp/*" or "/var/tmp/*".
- Examine the process tree to identify the parent process and any child processes spawned by the suspicious process, which may provide context on how the process was initiated and its potential impact.
- Check the command line arguments and environment variables of the process to gather additional context on its intended function and any anomalies.
- Investigate the user account under which the process is running to determine if it aligns with expected behavior or if it indicates potential compromise.
- Correlate the alert with other security events or logs, such as file modifications or network connections, to identify any related malicious activity or patterns.
- Assess the historical activity of the process executable and its associated files to determine if this behavior is new or part of a recurring pattern.

### False positive analysis

- System maintenance scripts may invoke prctl to rename processes for legitimate reasons. Review scheduled tasks and maintenance scripts in directories like /etc/cron.* and /etc/init.d to identify benign uses.
- Development environments often use prctl for testing purposes. Exclude known development directories such as /home/developer or /tmp/dev from the rule to reduce noise.
- Some monitoring or logging tools might use prctl to rename their processes for clarity. Identify these tools and add their executable paths to an exception list.
- Custom scripts or applications that manage process names for operational reasons should be documented. Exclude these scripts by specifying their paths in the rule configuration.
- Regularly review and update the exception list to ensure it reflects the current environment and does not inadvertently exclude new threats.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further malicious activity or lateral movement.
- Terminate any suspicious processes identified by the detection rule, especially those with altered names in critical directories.
- Conduct a thorough review of the affected system's process tree and file system to identify any additional signs of compromise or persistence mechanisms.
- Restore any altered or suspicious files from a known good backup to ensure system integrity.
- Update and patch the affected system to close any vulnerabilities that may have been exploited by the attacker.
- Monitor the network for any signs of similar activity or attempts to use the `prctl` syscall with the `PR_SET_NAME` argument in other systems.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if broader organizational impacts exist.
