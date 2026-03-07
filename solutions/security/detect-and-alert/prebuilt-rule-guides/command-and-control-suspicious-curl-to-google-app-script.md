---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Curl to Google App Script Endpoint" prebuilt detection rule.
---

# Suspicious Curl to Google App Script Endpoint

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Curl to Google App Script Endpoint

Google Apps Script is a cloud-based development platform that allows users to extend Google Workspace functionality with custom scripts. Threat actors abuse this legitimate service to host malicious scripts that serve as command and control endpoints, taking advantage of the trusted domain reputation and SSL certificates. This detection rule identifies curl connections to Google Apps Script endpoints from macOS systems, which may indicate C2 communication or payload retrieval from attacker-controlled scripts.

### Possible investigation steps

- Review the process.parent.executable and process.command_line fields to understand what application or script initiated the curl request to Google Apps Script.
- Extract the full URL from process.args to identify the specific Apps Script deployment being accessed and determine if it belongs to your organization.
- Analyze the process.Ext.effective_parent.executable to trace the execution chain and identify the root cause of the suspicious activity.
- Check Google Workspace admin logs if available to review the Apps Script deployment and its contents for malicious code.
- Investigate the user.name associated with the activity to determine if the behavior aligns with their normal duties.
- Review network response data if captured to identify any commands, payloads, or exfiltrated data transmitted via the Apps Script endpoint.
- Search for similar curl to Google Apps Script activity across other endpoints to assess the scope of potential compromise.

### False positive analysis

- Legitimate business automation may use Google Apps Script for workflow integrations. Verify with the script owner and confirm the Apps Script belongs to your organization.
- MDM and management tools like Kandji may interact with Google services legitimately. These are already excluded in the query but verify if additional tools should be added.
- Marketing and analytics platforms may use Apps Script for data collection. Confirm these are sanctioned business applications.
- Development and testing activities may involve Apps Script integrations. Coordinate with development teams to understand expected activities.

### Response and remediation

- Immediately block the suspicious Google Apps Script URL at the proxy or web filter to prevent ongoing C2 communication.
- Terminate the curl process and any parent processes that initiated the suspicious activity.
- Isolate the affected macOS system from the network while conducting forensic analysis.
- Report the malicious Apps Script to Google through their abuse reporting mechanisms to initiate takedown.
- Conduct a thorough scan of the affected system for additional malware, persistence mechanisms, or exfiltrated data.
- Review authentication logs for the affected user account and reset credentials if compromise is suspected.
- Search for similar activity across the environment to identify additional affected systems.
- Implement enhanced monitoring for connections to script.google.com from unexpected applications.

