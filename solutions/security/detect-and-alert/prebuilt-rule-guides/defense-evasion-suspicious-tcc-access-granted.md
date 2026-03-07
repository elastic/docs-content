---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious TCC Access Granted for User Folders" prebuilt detection rule.
---

# Suspicious TCC Access Granted for User Folders

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious TCC Access Granted for User Folders

The Transparency, Consent, and Control (TCC) framework is macOS's privacy protection mechanism that controls application access to sensitive resources like the Desktop, Documents, and Downloads folders. Threat actors may manipulate the TCC database to grant unauthorized access to these protected locations, enabling data theft without triggering user consent prompts. This detection rule identifies when scripting interpreters or command-line tools create multiple TCC permission grants in rapid succession, indicating potential automated TCC manipulation.

### Possible investigation steps

- Review the Effective_process.name and Effective_process.executable fields to identify which process is creating TCC permission grants and assess whether this is expected behavior.
- Examine the Tcc.service values to understand which protected folders (Desktop, Documents, Downloads) were granted access and evaluate the sensitivity of data in those locations.
- Investigate the Effective_process.parent.executable and command_line to trace how the TCC-modifying process was launched and identify the initial execution vector.
- Review the timing and count of TCC grants to determine if this is an automated batch operation characteristic of malicious activity.
- Check the TCC.db database directly using sqlite3 to review all permission grants and identify any unauthorized entries.
- Correlate with file access events to determine if the granted permissions were subsequently used to access sensitive data.
- Review the user.name associated with the activity and verify whether they would have legitimate reasons to grant these permissions.

### False positive analysis

- Legitimate applications during first launch or installation may request TCC access, but typically through standard user prompts rather than direct database modification. Verify if application installation was expected.
- Enterprise MDM solutions may configure TCC permissions during device setup or policy enforcement. Confirm with IT operations if MDM deployments were scheduled.
- Automation and scripting workflows may require TCC access for legitimate file operations. Review with the script owner to confirm legitimacy.
- System administration tasks may involve TCC manipulation for specific operational requirements. Verify with IT staff before dismissing.

### Response and remediation

- Immediately revoke the unauthorized TCC access grants by removing the malicious entries from the TCC.db database or resetting TCC permissions for the affected application.
- Terminate the suspicious process that created the TCC grants and prevent it from restarting.
- Isolate the affected macOS system to prevent potential data exfiltration using the newly granted permissions.
- Conduct a forensic review of file access events to determine if sensitive data was accessed using the unauthorized TCC permissions.
- Scan the system for additional malware, persistence mechanisms, or indicators of compromise.
- Reset TCC permissions to their default state using tccutil reset or by deleting and recreating the TCC.db database.
- Review other systems in the environment for similar TCC manipulation activity.
- Escalate to the incident response team for comprehensive investigation if data theft is suspected.

