---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Parent Process Detected with Suspicious Windows Process(es)" prebuilt detection rule.'
---

# Parent Process Detected with Suspicious Windows Process(es)

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Parent Process Detected with Suspicious Windows Process(es)

In Windows environments, processes are often spawned by parent processes, forming a hierarchy. Adversaries exploit this by using legitimate processes to launch malicious ones, often leveraging Living off the Land Binaries (LOLBins) to evade detection. The detection rule employs machine learning to identify clusters of processes with high malicious probability, focusing on those sharing a common parent process. This approach helps uncover stealthy attacks that traditional methods might miss, enhancing defense against tactics like masquerading.

### Possible investigation steps

- Review the parent process name associated with the suspicious process cluster to identify if it is a known legitimate process or a potential masquerading attempt.
- Examine the command line arguments and execution context of the suspicious processes to identify any use of LOLBins or unusual patterns that could indicate malicious activity.
- Check the process creation timestamps and correlate them with any known events or user activities to determine if the process execution aligns with expected behavior.
- Investigate the network activity of the suspicious processes to identify any unusual outbound connections or data exfiltration attempts.
- Analyze the user account context under which the suspicious processes were executed to determine if there is any indication of compromised credentials or privilege escalation.
- Cross-reference the detected processes with threat intelligence sources to identify any known indicators of compromise or related threat actor activity.

### False positive analysis

- Legitimate administrative tools may trigger false positives if they frequently spawn processes that resemble malicious activity. Users can create exceptions for known safe tools by whitelisting their parent process names.
- Software updates or installations often generate clusters of processes that might be flagged as suspicious. Users should monitor these activities and exclude them if they are verified as legitimate.
- Automated scripts or batch jobs that run regularly and spawn multiple processes can be mistaken for malicious clusters. Identifying these scripts and excluding their parent processes can reduce false positives.
- Security software or monitoring tools that perform regular scans or updates might mimic malicious behavior. Users should ensure these tools are recognized and excluded from the rule's scope.
- Custom business applications that are not widely recognized might be flagged. Users should document and exclude these applications if they are confirmed to be safe and necessary for operations.

### Response and remediation

- Isolate the affected system from the network to prevent further spread of the potential threat and to contain any ongoing malicious activity.
- Terminate the suspicious processes identified by the alert to stop any malicious actions they may be performing.
- Conduct a thorough review of the parent process and its associated binaries to ensure they have not been tampered with or replaced by malicious versions.
- Restore any affected files or system components from a known good backup to ensure system integrity and functionality.
- Update and patch the system to close any vulnerabilities that may have been exploited by the adversary, focusing on those related to LOLBins and masquerading techniques.
- Monitor the system and network for any signs of re-infection or related suspicious activity, using enhanced logging and alerting mechanisms.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
