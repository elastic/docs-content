---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Binary Executed from Shared Memory Directory" prebuilt detection rule.
---

# Binary Executed from Shared Memory Directory

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Binary Executed from Shared Memory Directory

Shared memory directories in Linux, such as /dev/shm and /run/shm, are designed for efficient inter-process communication. However, adversaries exploit these directories to execute binaries stealthily, often as root, bypassing traditional security measures. The detection rule identifies such anomalies by monitoring for root-executed binaries in these directories, excluding known legitimate processes, thus flagging potential backdoor activities.

### Possible investigation steps

- Review the process executable path to confirm it resides in a shared memory directory such as /dev/shm, /run/shm, /var/run, or /var/lock, and verify it is not part of the known exclusions like /var/run/docker or /var/run/utsns.
- Investigate the parent process of the suspicious executable to understand the context of its execution, focusing on the command line used, especially if it does not match the exclusion pattern /usr/bin/runc init.
- Check the process's creation time and correlate it with any other suspicious activities or alerts around the same timeframe to identify potential patterns or related incidents.
- Analyze the binary file in question for any known malicious signatures or unusual characteristics using tools like file integrity checkers or antivirus solutions.
- Review system logs and audit logs for any unauthorized access or privilege escalation attempts that might have led to the execution of the binary as root.
- Investigate the user account activity associated with user.id "0" to ensure there are no signs of compromise or misuse of root privileges.
- If possible, isolate the affected system to prevent further potential malicious activity while the investigation is ongoing.

### False positive analysis

- Docker-related processes can trigger false positives when binaries are executed from shared memory directories. To mitigate this, exclude paths like /var/run/docker/* from the detection rule.
- Processes related to container orchestration tools such as Kubernetes might also cause false positives. Exclude paths like /var/run/utsns/* and /var/run/s6/* to prevent these.
- Cloudera services may execute binaries from shared memory directories as part of their normal operations. Exclude /var/run/cloudera-scm-agent/* to avoid false alerts.
- Argo workflows might execute binaries in these directories. Exclude /var/run/argo/argoexec to reduce false positives.
- Legitimate use of /usr/bin/runc init as a parent process can be excluded to prevent unnecessary alerts.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further unauthorized access or lateral movement by the threat actor.
- Terminate any suspicious processes running from the shared memory directories (/dev/shm, /run/shm, /var/run, /var/lock) to halt potential malicious activity.
- Conduct a thorough review of the system's process tree and logs to identify any additional malicious binaries or scripts that may have been executed or are scheduled to run.
- Remove any unauthorized binaries or scripts found in the shared memory directories and other critical system paths to eliminate persistence mechanisms.
- Restore the system from a known good backup if the integrity of the system is compromised and cannot be assured through manual remediation.
- Implement enhanced monitoring and alerting for any future execution of binaries from shared memory directories, ensuring that legitimate processes are whitelisted appropriately.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
