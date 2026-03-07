---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Modification of Environment Variable via Unsigned or Untrusted Parent" prebuilt detection rule.'
---

# Modification of Environment Variable via Unsigned or Untrusted Parent

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Modification of Environment Variable via Unsigned or Untrusted Parent

Environment variables in macOS are crucial for configuring system and application behavior. Adversaries may exploit these by using the `launchctl` command to alter variables, enabling malicious payload execution or bypassing restrictions. The detection rule identifies suspicious modifications initiated by untrusted or unsigned parent processes, focusing on atypical environment variables and excluding known safe executables, thus highlighting potential threats.

### Possible investigation steps

- Review the process tree to identify the parent process of the `launchctl` command, focusing on whether the parent process is unsigned or untrusted, as indicated by the absence or lack of trust in the `process.parent.code_signature`.
- Examine the command-line arguments used with `launchctl`, specifically looking for the `setenv` command and any unusual or suspicious environment variables that are not part of the known safe list (e.g., ANT_HOME, DBUS_LAUNCHD_SESSION_BUS_SOCKET).
- Check the execution path of the parent process to determine if it matches any known safe executables, such as those listed in the exclusion criteria (e.g., /Applications/IntelliJ IDEA CE.app/Contents/jbr/Contents/Home/lib/jspawnhelper).
- Investigate the user account under which the `launchctl` command was executed to determine if it aligns with expected behavior or if it might indicate a compromised account.
- Correlate this event with other security alerts or logs from the same host to identify any patterns or additional indicators of compromise that might suggest a broader attack or intrusion attempt.

### False positive analysis

- Development tools like IntelliJ IDEA may trigger false positives when using the jspawnhelper executable. To mitigate this, add the executable path to the exclusion list if it is a known and trusted application in your environment.
- NoMachine software can cause false positives due to its use of nxserver.bin. If this software is regularly used and trusted, consider excluding its executable path from the detection rule.
- The kr tool located at /usr/local/bin/kr might be flagged as a false positive. If this tool is part of your standard operations, ensure its path is excluded to prevent unnecessary alerts.
- Review any other unsigned or untrusted parent processes that are part of legitimate software installations or operations. If they are verified as safe, add them to the exclusion list to reduce false positives.
- Regularly update the list of known safe executables and environment variables to reflect changes in your software inventory, ensuring that legitimate processes are not mistakenly flagged.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent potential lateral movement or further exploitation.
- Terminate any suspicious processes associated with the untrusted or unsigned parent process that initiated the `launchctl` command to halt any ongoing malicious activity.
- Conduct a thorough review of the environment variables modified by the `launchctl` command to identify any unauthorized changes and revert them to their original state.
- Analyze the parent process that triggered the alert to determine its origin and purpose, and remove any malicious or unauthorized software identified during this analysis.
- Restore the system from a known good backup if any critical system components or configurations have been compromised.
- Implement additional monitoring and logging for `launchctl` usage and environment variable modifications to detect similar threats in the future.
- Escalate the incident to the security operations team for further investigation and to assess the need for broader organizational response measures.
