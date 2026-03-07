---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Dylib Injection via Process Environment Variables" prebuilt detection rule.
---

# Dylib Injection via Process Environment Variables

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Dylib Injection via Process Environment Variables

Dynamic library injection using DYLD_INSERT_LIBRARIES or LD_PRELOAD environment variables is a powerful technique that allows code to be loaded into a process's address space at runtime. While this capability exists for legitimate debugging and development purposes, threat actors abuse it to hook application functionality, steal credentials, intercept keystrokes, or execute malicious code within trusted processes. This detection rule identifies processes started with these injection environment variables set to non-empty values.

### Possible investigation steps

- Review the process.env_vars field to identify the specific dylib being injected via DYLD_INSERT_LIBRARIES or LD_PRELOAD and determine its file path.
- Locate the injected dylib file on the file system using the path from the environment variable and calculate its hash for threat intelligence lookups.
- Analyze the process.executable and process.name fields to identify the target application being hijacked and assess whether dylib injection makes sense for its normal operation.
- Examine the process.parent.executable and process.command_line to understand how the process with injection was launched and trace back to the initial execution vector.
- Review the code signature of the injected dylib using codesign or similar tools to determine if it is signed, and by whom.
- Check for file creation events to determine when the malicious dylib was placed on the system and how it was delivered.
- Correlate with other security events on the same host to identify if the injection is part of a larger attack chain, such as credential theft or keylogging.

### False positive analysis

- Xcode and iOS Simulator use DYLD_INSERT_LIBRARIES for debugging and testing purposes during application development. These paths are already excluded in the query.
- Security research and reverse engineering tools may use library injection for analysis. Verify with security teams if such activities are expected.
- Some legitimate applications use library injection for specific functionality. Document these applications and create targeted exceptions after verification.
- Homebrew and development environments may occasionally use these environment variables. Confirm with development teams before creating exclusions.

### Response and remediation

- Immediately terminate the process using malicious dylib injection to stop any ongoing malicious activity such as credential theft or keylogging.
- Quarantine the injected dylib file for forensic analysis and malware reverse engineering.
- Remove the malicious dylib from the system and ensure it cannot be reloaded through persistence mechanisms.
- Investigate how the dylib was placed on the system and remediate the initial access or delivery mechanism.
- Review System Integrity Protection (SIP) status on the affected system, as SIP should normally prevent DYLD injection into protected system processes.
- Scan the system for additional indicators of compromise, persistence mechanisms, or lateral movement.
- Reset any credentials that may have been exposed through the injection, particularly if the target application handles sensitive authentication data.
- Escalate to the incident response team for comprehensive analysis if the injection indicates active compromise.

