---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Persistence via Suspicious Launch Agent or Launch Daemon" prebuilt detection rule.'
---

# Persistence via Suspicious Launch Agent or Launch Daemon

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Persistence via Suspicious Launch Agent or Launch Daemon

LaunchAgents and LaunchDaemons are the standard macOS mechanisms for starting programs automatically at user login or system boot. While essential for legitimate software, these persistence mechanisms are heavily abused by malware including RustBucket (DPRK), Shlayer, and CloudMensis. This detection rule identifies plist file creation in LaunchAgent/LaunchDaemon directories when performed by suspicious processes including scripts executing from temporary directories, unsigned binaries, or scripting interpreters like Python and osascript.

### Possible investigation steps

- Examine the file.path to identify the specific plist file created and its location (user vs system LaunchAgent/LaunchDaemon directory).
- Read the plist contents using plutil or defaults to identify the Program or ProgramArguments configured for execution.
- Analyze the process.executable to understand what created the plist file and assess whether execution from that location (temp directory, hidden folder) is suspicious.
- Check the process.name and process.code_signature fields to determine if the creating process was a scripting interpreter or unsigned binary.
- Locate the binary or script referenced in the plist and calculate its hash for threat intelligence lookups.
- Review the parent process chain to trace back to the initial execution vector that led to plist creation.
- Correlate with other file and process events to identify additional malware components that may have been deployed simultaneously.

### False positive analysis

- Legitimate software installers may create LaunchAgents/LaunchDaemons during setup, but typically from signed installer processes rather than scripts in temp directories.
- Development and testing environments may use scripting languages to create launch items. Verify with development teams if such activities are expected.
- Several legitimate signing IDs are already excluded including vim, JetBrains Toolbox, and Sublime Text.
- System utilities like cfprefsd may modify plist files during normal operations and are excluded.
- Enterprise deployment tools may use scripts to configure launch items. Document and exclude approved deployment processes.

### Response and remediation

- Immediately unload the suspicious LaunchAgent or LaunchDaemon using launchctl unload with the plist path.
- Remove the malicious plist file from the LaunchAgent or LaunchDaemon directory.
- Locate and remove the executable or script referenced in the plist's Program or ProgramArguments keys.
- Check for other persistence mechanisms that may have been deployed by the same threat actor.
- Review system logs for evidence of the persistence mechanism executing and what actions it performed.
- If the detection matches patterns of known malware families (RustBucket, Shlayer), perform comprehensive IOC searches and threat hunting.
- Reset any credentials that may have been accessed while the malicious process was running.
- Monitor for recreation of similar plist files to detect persistent access or ongoing compromise.
