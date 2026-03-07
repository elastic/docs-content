---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious Curl from macOS Application" prebuilt detection rule.'
---

# Suspicious Curl from macOS Application

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Curl from macOS Application

Trojanized macOS applications often use curl to download second-stage payloads from attacker-controlled infrastructure. By leveraging curl instead of direct downloads, these malicious applications can bypass Gatekeeper quarantine checks and evade built-in macOS security mechanisms. This detection rule identifies when applications from the /Applications directory spawn curl to connect to raw IP addresses, which is highly indicative of malicious payload retrieval activity.

### Possible investigation steps

- Review the process.Ext.effective_parent.executable field to identify which application spawned the curl process and assess whether this application is expected to make network downloads.
- Examine the process.args fields to extract the destination IP address and URL path being accessed, and research these indicators in threat intelligence databases.
- Analyze the process.parent.command_line to understand the full context of how curl was invoked, including any output file paths that may indicate where payloads were written.
- Check the code signature of the parent application using the process.code_signature fields to determine if it is validly signed and if the signature matches known good versions.
- Investigate the origin of the suspicious application by reviewing installation logs, download history, and any recent DMG or PKG files that may have delivered the trojanized application.
- Search for any files created on disk around the time of the curl execution to identify downloaded payloads that may have been staged for execution.
- Correlate with other events on the same host to identify if the downloaded payload was subsequently executed.

### False positive analysis

- Some legitimate applications may use curl for software updates or telemetry data collection. Verify the destination IP against the application vendor's known infrastructure.
- Development tools and IDEs may download dependencies or packages via curl during normal operations. Review the context and confirm with development teams.
- Homebrew and package managers may spawn curl from application contexts during installations. Verify if package management activities were expected.
- Add verified legitimate applications to the exclusion list in the query after confirming their behavior is expected.

### Response and remediation

- Immediately quarantine the suspicious application by moving it to a secure location and removing it from /Applications to prevent further execution.
- Block the destination IP address at the network perimeter and on endpoint firewalls to prevent additional downloads.
- Search the file system for any payloads that may have been downloaded and quarantine them for analysis.
- Conduct a full malware scan on the affected system to identify any persistence mechanisms or additional malware components.
- Report the trojanized application to Apple Security and relevant threat intelligence sharing platforms.
- Review other systems in the environment for the same trojanized application to determine the scope of potential compromise.
- Investigate the delivery mechanism to understand how the trojanized application was installed and prevent future infections.
