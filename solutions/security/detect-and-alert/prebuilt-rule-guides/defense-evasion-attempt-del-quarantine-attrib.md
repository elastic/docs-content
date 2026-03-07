---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Quarantine Attrib Removed by Unsigned or Untrusted Process" prebuilt detection rule.
---

# Quarantine Attrib Removed by Unsigned or Untrusted Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Quarantine Attrib Removed by Unsigned or Untrusted Process

In macOS, files downloaded from the internet are tagged with a quarantine attribute, which is checked by Gatekeeper to ensure safety before execution. Adversaries may remove this attribute to bypass security checks, allowing potentially harmful applications to run unchecked. The detection rule identifies such actions by monitoring for the removal of this attribute by processes that are either unsigned or untrusted, flagging unusual activity that deviates from expected behavior.

### Possible investigation steps

- Review the process executable path that triggered the alert to determine if it is a known or expected application on the system. Check if it matches any legitimate software that might not be properly signed.
- Investigate the parent process of the flagged executable to understand the context of its execution. This can help identify if the process was spawned by a legitimate application or a potentially malicious one.
- Examine the file path from which the quarantine attribute was removed to assess if it is a common location for downloaded files or if it appears suspicious.
- Check the system for any recent downloads or installations that might correlate with the time of the alert to identify potential sources of the file.
- Look into the user account under which the process was executed to determine if it aligns with expected user behavior or if it might indicate unauthorized access.
- Search for any other alerts or logs related to the same process or file path to identify patterns or repeated attempts to bypass security measures.

### False positive analysis

- System processes or legitimate applications may occasionally remove the quarantine attribute as part of their normal operation. Users can create exceptions for known safe processes by adding them to the exclusion list in the detection rule.
- Software updates or installations from trusted vendors might trigger the rule if they are not properly signed. Verify the legitimacy of the software and consider adding the specific executable path to the exclusion list if it is deemed safe.
- Custom scripts or automation tools used within an organization might remove the quarantine attribute as part of their workflow. Review these scripts to ensure they are secure and add their paths to the exclusion list to prevent false positives.
- Temporary files or directories, such as those in /private/var/folders, are already excluded to reduce noise. Ensure that any additional temporary paths used by trusted applications are similarly excluded if they are known to cause false positives.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent potential lateral movement or further compromise.
- Terminate any untrusted or unsigned processes identified in the alert that are responsible for removing the quarantine attribute.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any malicious software.
- Restore any affected files from a known good backup if they have been altered or compromised.
- Review system logs and the specific file paths involved in the alert to identify any additional unauthorized changes or suspicious activity.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement additional monitoring and alerting for similar activities on other macOS systems to enhance detection and response capabilities.
