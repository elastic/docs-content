---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Google Calendar C2 via Script Interpreter" prebuilt detection rule.'
---

# Google Calendar C2 via Script Interpreter

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Google Calendar C2 via Script Interpreter

Threat actors increasingly abuse legitimate cloud services to establish covert command and control channels that blend with normal traffic and bypass traditional network security controls. Google Calendar has been weaponized as a C2 mechanism where attackers store encoded commands in calendar event descriptions, which malware then polls and executes. This detection rule identifies script interpreters connecting to Google Calendar API endpoints, which may indicate this living-off-the-land technique.

### Possible investigation steps

- Review the process.name and process.executable fields to identify which script interpreter is making the Google Calendar API connection and assess whether it is expected for the user or application context.
- Examine the process.command_line and process.args fields to understand what script or code is being executed that initiated the calendar connection.
- Check the process.parent.executable and process.parent.command_line to trace the process lineage and identify how the script interpreter was launched.
- Investigate the Google Workspace audit logs for the associated user account to review calendar events that may contain encoded commands or suspicious content.
- Review network connection details including dns.question.name and destination.ip to understand the specific Google API endpoints being accessed.
- Correlate with authentication events to identify which user account or service account OAuth tokens are being used for the calendar access.
- Search for similar activity across other endpoints to determine if this is an isolated incident or part of a broader campaign.

### False positive analysis

- Legitimate productivity applications may integrate with Google Calendar for scheduling and automation purposes. Verify the application's purpose and whether it is approved by IT.
- Custom automation scripts built by employees may access Google Calendar API for workflow automation. Review with the script owner to confirm legitimacy.
- Development and testing environments may trigger this detection when building calendar integrations. Document known development activities and create targeted exceptions.
- Third-party calendar sync applications may use script interpreters to interface with Google Calendar. Verify these are sanctioned applications.

### Response and remediation

- Immediately terminate the suspicious script interpreter process to stop any ongoing C2 communication.
- Revoke OAuth tokens and API credentials associated with the compromised Google account to prevent further unauthorized access.
- Review Google Workspace admin console for any unauthorized calendar events or modifications that may contain malicious content.
- Isolate the affected macOS system from the network while conducting forensic analysis.
- Perform a comprehensive scan for additional malware, persistence mechanisms, or lateral movement indicators.
- Reset the affected user's credentials and enable multi-factor authentication if not already in place.
- Implement application allowlisting to prevent unauthorized script interpreters from executing.
- Escalate to the security operations team for further investigation into potential data exfiltration or broader compromise.
