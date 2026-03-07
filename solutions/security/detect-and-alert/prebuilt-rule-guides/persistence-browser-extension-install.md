---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Browser Extension Install" prebuilt detection rule.'
---

# Browser Extension Install

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Browser Extension Install
Browser extensions enhance functionality in web browsers but can be exploited by adversaries to gain persistence or execute malicious activities. Attackers may disguise harmful extensions as legitimate or use compromised systems to install them. The detection rule identifies suspicious extension installations by monitoring file creation events in typical extension directories, filtering out known safe processes, and focusing on Windows environments.

### Possible investigation steps

- Review the file creation event details to identify the specific browser extension file (e.g., .xpi or .crx) and its path to determine if it aligns with known malicious patterns or locations.
- Check the process that initiated the file creation event, especially if it is not a known safe process like firefox.exe, to assess if it is a legitimate application or potentially malicious.
- Investigate the user account associated with the file creation event to determine if the activity is expected or if the account may have been compromised.
- Examine recent system activity and logs for any signs of social engineering attempts or unauthorized access that could have led to the installation of the extension.
- Cross-reference the extension file name and path with threat intelligence sources to identify if it is associated with known malicious browser extensions.
- If applicable, review the browser's extension management interface to verify the presence and legitimacy of the installed extension.

### False positive analysis

- Language pack installations for Firefox can trigger false positives. Exclude files named "langpack-*@firefox.mozilla.org.xpi" from detection to prevent unnecessary alerts.
- Dictionary add-ons for Firefox may also be flagged. Add exceptions for files named "*@dictionaries.addons.mozilla.org.xpi" to reduce false positives.
- Regular updates or installations of legitimate browser extensions from trusted sources can be mistaken for malicious activity. Maintain a list of trusted processes and paths to exclude from monitoring.
- User-initiated installations from official browser stores might be flagged. Educate users on safe installation practices and consider excluding known safe processes like "firefox.exe" when associated with legitimate extension paths.
- Frequent installations in enterprise environments due to software deployment tools can cause alerts. Coordinate with IT to identify and exclude these routine activities from detection.

### Response and remediation

- Isolate the affected system from the network to prevent further spread or communication with potential command and control servers.
- Terminate any suspicious processes associated with the unauthorized browser extension installation, such as unknown or unexpected instances of browser processes.
- Remove the malicious browser extension by deleting the associated files from the extension directories identified in the alert.
- Conduct a full antivirus and anti-malware scan on the affected system to identify and remove any additional threats or remnants of the malicious extension.
- Review and reset browser settings to default to ensure no residual configurations or settings are left by the malicious extension.
- Escalate the incident to the security operations team for further investigation and to determine if additional systems are affected.
- Implement application whitelisting to prevent unauthorized browser extensions from being installed in the future, focusing on the directories and file types identified in the detection query.
