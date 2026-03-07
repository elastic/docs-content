---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Python Path File (pth) Creation" prebuilt detection rule.'
---

# Python Path File (pth) Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Python Path File (pth) Creation

Python Path Files (.pth) are used to automatically execute code when the Python interpreter starts, making them a potential target for adversaries seeking persistence. Attackers can exploit .pth files by placing malicious code in directories where Python packages reside, ensuring execution each time Python runs. The detection rule monitors the creation and renaming of .pth files in key directories, excluding legitimate processes, to identify unauthorized modifications indicative of malicious activity.

### Possible investigation steps

- Review the file path where the .pth file was created or renamed to determine if it is within a legitimate Python package directory, as specified in the query paths.
- Identify the process executable responsible for the creation or renaming of the .pth file and verify if it is listed as an excluded legitimate process in the query.
- Investigate the parent process of the identified executable to understand the context of the .pth file creation and assess if it aligns with expected behavior.
- Check the timestamp of the .pth file creation or renaming event to correlate with any known scheduled tasks or user activities.
- Examine the contents of the .pth file to identify any suspicious or unauthorized code that could indicate malicious intent.
- Review recent system logs and user activity around the time of the event to identify any anomalies or unauthorized access attempts.

### False positive analysis

- Legitimate package installations or updates using package managers like pip or poetry can trigger false positives. To handle this, ensure that the process executables for these package managers are included in the exclusion list.
- Automated scripts or CI/CD pipelines that manage Python environments might create or rename .pth files. Identify these scripts and add their executables to the exclusion list to prevent unnecessary alerts.
- System updates or maintenance tasks that involve Python package directories can also result in false positives. Monitor these activities and temporarily adjust the rule or add specific system maintenance processes to the exclusion list.
- Custom Python applications that manage dependencies or configurations through .pth files may cause alerts. Review these applications and consider adding their specific paths or executables to the exclusion criteria.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further execution of potentially malicious code.
- Identify and terminate any suspicious processes associated with the creation or modification of .pth files, especially those not matching the legitimate process list.
- Remove any unauthorized .pth files from the identified directories to eliminate the persistence mechanism.
- Conduct a thorough review of recent changes to the Python environment and installed packages to identify any malicious or unauthorized modifications.
- Restore affected systems from a known good backup if malicious activity is confirmed and cannot be fully remediated.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and alerting for future unauthorized .pth file modifications to quickly detect similar threats.
