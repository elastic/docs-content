---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Script Execution via Microsoft HTML Application" prebuilt detection rule.
---

# Script Execution via Microsoft HTML Application

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Script Execution via Microsoft HTML Application

Microsoft HTML Applications (HTA) allow scripts to run in a trusted environment, often using utilities like `rundll32.exe` or `mshta.exe`. Adversaries exploit this by executing malicious scripts under the guise of legitimate processes, bypassing defenses. The detection rule identifies suspicious script execution patterns, such as unusual command lines or execution from common download locations, to flag potential abuse.

### Possible investigation steps

- Review the process command line details to identify any suspicious patterns or indicators of malicious activity, such as the presence of script execution commands like "eval", "GetObject", or "WScript.Shell".
- Check the parent process executable path to determine if the process was spawned by a known legitimate application or if it deviates from expected behavior, especially if it is not from the specified exceptions like Citrix, Microsoft Office, or Quokka.Works GTInstaller.
- Investigate the origin of the HTA file, particularly if it was executed from common download locations like the Downloads folder or temporary archive extraction paths, to assess if it was downloaded from the internet or extracted from an archive.
- Analyze the process arguments and count to identify any unusual or unexpected parameters that could indicate malicious intent, especially if the process name is "mshta.exe" and the command line does not include typical HTA or HTM file references.
- Correlate the event with other security logs and alerts from data sources like Sysmon, SentinelOne, or Microsoft Defender for Endpoint to gather additional context and determine if this activity is part of a broader attack pattern.

### False positive analysis

- Execution of legitimate scripts by enterprise applications like Citrix, Microsoft Office, or Quokka.Works GTInstaller can trigger false positives. Users can mitigate this by adding these applications to the exclusion list in the detection rule.
- Scripts executed by mshta.exe that do not involve malicious intent, such as internal web applications or administrative scripts, may be flagged. Users should review these scripts and, if deemed safe, exclude them based on specific command line patterns or parent processes.
- HTA files downloaded from trusted internal sources or vendors might be mistakenly identified as threats. Users can create exceptions for these sources by specifying trusted download paths or file hashes.
- Temporary files created by legitimate software installations or updates in user temp directories can be misinterpreted as malicious. Users should monitor these activities and exclude known safe processes or directories from the detection rule.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further spread of the malicious script or unauthorized access.
- Terminate any suspicious processes identified by the detection rule, specifically those involving `rundll32.exe` or `mshta.exe` with unusual command lines.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any malicious files or scripts.
- Review and analyze the command lines and scripts executed to understand the scope and intent of the attack, and identify any additional compromised systems.
- Restore the affected system from a known good backup if malicious activity is confirmed and cannot be fully remediated.
- Implement network segmentation to limit the ability of similar threats to propagate across the network in the future.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems or data have been compromised.
