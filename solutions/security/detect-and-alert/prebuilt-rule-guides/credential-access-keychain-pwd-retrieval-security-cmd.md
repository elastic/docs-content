---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Keychain Password Retrieval via Command Line" prebuilt detection rule.'
---

# Keychain Password Retrieval via Command Line

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Keychain Password Retrieval via Command Line

Keychain is macOS's secure storage system for managing user credentials, including passwords and certificates. Adversaries may exploit command-line tools to extract sensitive data from Keychain, targeting browsers like Chrome and Safari. The detection rule identifies suspicious command executions involving Keychain access, focusing on specific arguments and excluding legitimate applications, to flag potential credential theft attempts.

### Possible investigation steps

- Review the process execution details to confirm the presence of the 'security' command with arguments '-wa' or '-ga' and 'find-generic-password' or 'find-internet-password', as these indicate attempts to access Keychain data.
- Examine the command line for references to browsers such as Chrome, Safari, or others specified in the rule to determine if the target was browser-related credentials.
- Investigate the parent process of the suspicious command to ensure it is not a legitimate application, specifically checking that it is not the Keeper Password Manager, as this is excluded in the rule.
- Check the user account associated with the process execution to determine if the activity aligns with expected behavior for that user or if it suggests unauthorized access.
- Review recent login and access logs for the system to identify any unusual or unauthorized access patterns that could correlate with the suspicious Keychain access attempt.
- Assess the system for any additional indicators of compromise or related suspicious activities that might suggest a broader security incident.

### False positive analysis

- Legitimate password managers like Keeper Password Manager may trigger the rule due to their access to Keychain for managing user credentials. To handle this, ensure that the process parent executable path for such applications is added to the exclusion list.
- System maintenance or administrative scripts that access Keychain for legitimate purposes might be flagged. Review these scripts and, if verified as safe, add their specific command patterns to the exception list.
- Development or testing tools that interact with browsers and require Keychain access could cause false positives. Identify these tools and exclude their specific process names or command-line arguments if they are part of regular operations.
- Automated backup or synchronization services that access browser credentials stored in Keychain may be mistakenly identified. Confirm these services' legitimacy and exclude their associated processes from the detection rule.

### Response and remediation

- Immediately isolate the affected macOS system from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious processes identified by the detection rule, particularly those involving the 'security' command with the specified arguments targeting browsers.
- Conduct a thorough review of the system's keychain access logs to identify any unauthorized access attempts and determine the scope of the compromise.
- Change all potentially compromised credentials stored in the keychain, including browser passwords and Wi-Fi credentials, and ensure they are updated across all relevant services.
- Implement additional monitoring on the affected system and similar endpoints to detect any further attempts to access keychain data using command-line tools.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to assess the need for broader organizational response measures.
- Review and update endpoint security configurations to restrict unauthorized access to keychain data and enhance logging for keychain-related activities.
