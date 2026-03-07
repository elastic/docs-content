---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Process Spawned by a Host" prebuilt detection rule.'
---

# Unusual Process Spawned by a Host

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Process Spawned by a Host

The detection rule leverages machine learning to identify atypical processes on Windows systems, focusing on those that deviate from normal behavior. Adversaries often exploit legitimate system tools, known as LOLbins, to evade detection. This rule uses the ProblemChild ML model to flag processes that are both statistically unusual and potentially malicious, enhancing detection of stealthy attacks that bypass traditional methods.

### Possible investigation steps

- Review the process details flagged by the ProblemChild ML model, including the process name, path, and command line arguments, to understand its nature and potential purpose.
- Check the parent process of the flagged process to determine if it was spawned by a legitimate application or a known LOLbin, which might indicate a Living off the Land attack.
- Investigate the host's historical activity to assess whether this process or similar ones have been executed previously, focusing on any patterns of unusual behavior.
- Correlate the process activity with user logins and network connections to identify any suspicious user behavior or external communications that coincide with the process execution.
- Examine the system's security logs for any related alerts or anomalies around the time the process was detected, which might provide additional context or evidence of malicious activity.

### False positive analysis

- Routine administrative tasks may trigger false positives if they involve unusual processes or tools not commonly used on the host. Users can create exceptions for these known tasks to prevent unnecessary alerts.
- Software updates or installations can spawn processes that are atypical but benign. Identifying and excluding these processes during known maintenance windows can reduce false positives.
- Custom scripts or automation tools that mimic LOLbins behavior might be flagged. Users should document and whitelist these scripts if they are verified as safe and necessary for operations.
- Legitimate third-party applications that use system binaries in uncommon ways may be misclassified. Regularly review and update the list of approved applications to ensure they are not mistakenly flagged.
- Temporary spikes in unusual processes due to legitimate business activities, such as end-of-quarter reporting, can be managed by adjusting the detection thresholds or temporarily disabling the rule during these periods.

### Response and remediation

- Isolate the affected host from the network to prevent further spread or communication with potential command and control servers.
- Terminate the suspicious process identified by the ProblemChild ML model to halt any ongoing malicious activity.
- Conduct a thorough review of the process's parent and child processes to identify any additional malicious activity or persistence mechanisms.
- Remove any identified LOLbins or unauthorized tools used by the adversary from the system to prevent further exploitation.
- Restore the affected system from a known good backup if any system integrity issues are detected.
- Update endpoint protection and monitoring tools to ensure they can detect similar threats in the future, focusing on the specific techniques used in this incident.
- Escalate the incident to the security operations center (SOC) or incident response team for further analysis and to determine if additional systems are affected.
