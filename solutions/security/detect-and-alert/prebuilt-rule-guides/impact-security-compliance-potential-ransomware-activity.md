---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Deprecated - M365 Security Compliance Potential Ransomware Activity" prebuilt detection rule.'
---

# Deprecated - M365 Security Compliance Potential Ransomware Activity

## Triage and analysis

### Investigating Deprecated - M365 Security Compliance Potential Ransomware Activity

Microsoft 365's cloud services can be exploited by adversaries to distribute ransomware by uploading infected files. This detection rule leverages Microsoft Cloud App Security to identify suspicious uploads, focusing on successful events flagged as potential ransomware activity. By monitoring specific event datasets and actions, it helps security analysts pinpoint and mitigate ransomware threats, aligning with MITRE ATT&CK's impact tactics.

### Possible investigation steps

- Identify the affected user account and review their recent file activity in Microsoft 365 for signs of mass file encryption, renaming with unusual extensions, or rapid file modifications.
- Examine the file names, extensions, and metadata of the flagged uploads to determine if they match known ransomware patterns (e.g., `.encrypted`, `.locked`, or ransom note files like `README.txt` or `DECRYPT_INSTRUCTIONS.html`).
- Correlate this alert with other security events from the same user or source IP, such as impossible travel, failed login attempts, or suspicious inbox rules, to identify potential account compromise.
- Check whether the affected user's endpoint shows signs of ransomware execution, such as high CPU usage, mass file system changes, or known ransomware process names.
- Review SharePoint or OneDrive file version history to determine the scope of encrypted or modified files and whether recovery via version rollback is possible.
- Contact the user to verify whether the activity is legitimate or if their account or device may have been compromised.

### False positive analysis

- Legitimate file uploads by trusted users may trigger alerts if the files are mistakenly flagged as ransomware. To manage this, create exceptions for specific users or groups who frequently upload large volumes of files.
- Automated backup processes that upload encrypted files to the cloud can be misidentified as ransomware activity. Exclude these processes by identifying and whitelisting the associated service accounts or IP addresses.
- Certain file types or extensions commonly used in business operations might be flagged. Review and adjust the detection rule to exclude these file types if they are consistently identified as false positives.
- Collaborative tools that sync files across devices may cause multiple uploads that appear suspicious. Monitor and exclude these tools by recognizing their typical behavior patterns and adjusting the rule settings accordingly.

### Response and remediation

- Immediately isolate the affected user account to prevent further uploads and potential spread of ransomware within the cloud environment.
- Quarantine the uploaded files flagged as potential ransomware to prevent access and further distribution.
- Conduct a thorough scan of the affected user's devices and cloud storage for additional signs of ransomware or other malicious activity.
- Notify the security operations team to initiate a deeper investigation into the source and scope of the ransomware activity.
- Restore any affected files from secure backups, ensuring that the backups are clean and free from ransomware.
- Review and update access controls and permissions for the affected user and related accounts to minimize the risk of future incidents.
- Escalate the incident to senior security management and, if necessary, involve legal or compliance teams to assess any regulatory implications.
