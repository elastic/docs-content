---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Hidden Local User Account Creation" prebuilt detection rule.'
---

# Potential Hidden Local User Account Creation

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Hidden Local User Account Creation

In macOS environments, the `dscl` command-line utility manages directory services, including user accounts. Adversaries may exploit this to create hidden local accounts, evading detection while maintaining persistence. The detection rule monitors for `dscl` processes attempting to set accounts as hidden, flagging suspicious activity indicative of potential misuse.

### Possible investigation steps

- Review the process details to confirm the presence of the `dscl` command with arguments related to account creation and hiding, specifically checking for `IsHidden`, `create`, and values like `true`, `1`, or `yes`.
- Identify the user account under which the `dscl` command was executed to determine if it was initiated by an authorized user or a potential adversary.
- Check the system logs for any additional suspicious activity around the time the `dscl` command was executed, such as other unauthorized account modifications or unusual login attempts.
- Investigate the newly created account details, if available, to assess its purpose and legitimacy, including checking for any associated files or processes that might indicate malicious intent.
- Correlate the event with other security alerts or anomalies on the host to determine if this activity is part of a broader attack pattern or isolated incident.

### False positive analysis

- System administrators may use the dscl command to create hidden accounts for legitimate purposes such as maintenance or automated tasks. To manage this, create exceptions for known administrator accounts or scripts that regularly perform these actions.
- Some third-party applications or management tools might use hidden accounts for functionality or security purposes. Identify these applications and whitelist their processes to prevent unnecessary alerts.
- During system setup or configuration, hidden accounts might be created as part of the initial setup process. Exclude these initial setup activities by correlating them with known installation or configuration events.
- Regular audits of user accounts and their creation processes can help distinguish between legitimate and suspicious account creation activities, allowing for more informed exception handling.
- If a specific user or group frequently triggers this rule due to their role, consider creating a role-based exception to reduce noise while maintaining security oversight.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent potential lateral movement or data exfiltration by the adversary.
- Use administrative privileges to review and remove any unauthorized hidden user accounts created using the `dscl` command. Ensure that legitimate accounts are not affected.
- Change passwords for all local accounts on the affected system to prevent unauthorized access using potentially compromised credentials.
- Conduct a thorough review of system logs and security alerts to identify any additional suspicious activities or indicators of compromise related to the hidden account creation.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if the threat is part of a larger attack campaign.
- Implement enhanced monitoring for `dscl` command usage across all macOS systems in the environment to detect and respond to similar threats promptly.
- Update and reinforce endpoint security measures, such as ensuring all systems have the latest security patches and antivirus definitions, to prevent exploitation of known vulnerabilities.
