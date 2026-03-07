---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Git Hook Child Process" prebuilt detection rule.
---

# Git Hook Child Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Git Hook Child Process

Git hooks are scripts that automate tasks during Git operations like commits or pushes. Adversaries may exploit these hooks to execute unauthorized commands, masking malicious activities under legitimate processes. The detection rule identifies unusual child processes spawned by Git hooks, focusing on atypical scripts or executables in suspicious directories, signaling potential misuse.

### Possible investigation steps

- Review the process tree to understand the parent-child relationship, focusing on the parent process names listed in the query, such as "pre-commit" or "post-update", to determine the context of the spawned child process.
- Examine the command line arguments and environment variables of the suspicious child process to identify any potentially malicious or unauthorized commands being executed.
- Check the file paths of the executables involved, especially those in unusual directories like "/tmp/*" or "/var/tmp/*", to assess if they are legitimate or potentially harmful.
- Investigate the user account under which the suspicious process is running to determine if it has been compromised or is being used in an unauthorized manner.
- Correlate the event with other security logs or alerts from the same host to identify any patterns or additional indicators of compromise.
- Review recent Git activity on the repository to identify any unauthorized changes or suspicious commits that might indicate tampering with Git hooks.

### False positive analysis

- Legitimate development scripts: Developers may use scripts in directories like /tmp or /var/tmp for testing purposes. To handle this, create exceptions for known scripts or directories used by trusted developers.
- Custom shell usage: Developers might use shells like bash or zsh for legitimate automation tasks. Identify and whitelist these specific shell scripts if they are part of regular development workflows.
- Temporary file execution: Some applications may temporarily execute files from directories like /dev/shm or /run. Monitor these applications and exclude them if they are verified as non-threatening.
- Non-standard interpreters: Developers might use interpreters like php or perl for legitimate tasks. Review and whitelist these processes if they are part of approved development activities.
- System maintenance scripts: Scheduled tasks or maintenance scripts might run from /etc/cron.* or /etc/init.d. Verify these scripts and exclude them if they are part of routine system operations.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or execution of malicious commands.
- Terminate any suspicious processes identified by the detection rule, especially those originating from unusual directories or involving unexpected scripts or executables.
- Conduct a thorough review of the Git hooks on the affected system to identify and remove any unauthorized or malicious scripts.
- Restore any modified or deleted files from a known good backup to ensure system integrity and continuity of operations.
- Implement stricter access controls and permissions for Git repositories and associated directories to prevent unauthorized modifications to Git hooks.
- Monitor the affected system and related network activity closely for any signs of persistence or further compromise, using enhanced logging and alerting mechanisms.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems or data have been affected.
