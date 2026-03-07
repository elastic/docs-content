---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Microsoft IIS Connection Strings Decryption" prebuilt detection rule.'
---

# Microsoft IIS Connection Strings Decryption

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Microsoft IIS Connection Strings Decryption

Microsoft IIS often stores sensitive connection strings in encrypted form to secure database credentials. The `aspnet_regiis` tool can decrypt these strings, a feature intended for legitimate administrative tasks. However, attackers with access to the IIS server, possibly via a webshell, can exploit this to extract credentials. The detection rule identifies suspicious use of `aspnet_regiis` by monitoring process execution with specific arguments, flagging potential credential access attempts.

### Possible investigation steps

- Review the process execution details to confirm the presence of aspnet_regiis.exe with the specific arguments "connectionStrings" and "-pdf" to ensure the alert is not a false positive.
- Check the user account associated with the process execution to determine if it is a legitimate administrative account or a potentially compromised one.
- Investigate the source of the process initiation by examining the parent process and any related processes to identify if a webshell or unauthorized script triggered the execution.
- Analyze recent login activities and access logs on the IIS server to identify any unusual or unauthorized access patterns that could indicate a compromise.
- Review the server's security logs and any available network traffic data to detect any signs of data exfiltration or further malicious activity following the decryption attempt.
- Assess the integrity and security of the IIS server by checking for any unauthorized changes or suspicious files that may have been introduced by an attacker.

### False positive analysis

- Routine administrative tasks using aspnet_regiis for legitimate configuration changes can trigger the rule. To manage this, create exceptions for known maintenance windows or specific administrator accounts performing these tasks.
- Automated deployment scripts that include aspnet_regiis for setting up or updating IIS configurations may cause false positives. Exclude these scripts by identifying their unique process arguments or execution paths.
- Scheduled tasks or services that periodically run aspnet_regiis for configuration validation or updates might be flagged. Document these tasks and exclude them based on their scheduled times or associated service accounts.
- Development environments where developers frequently use aspnet_regiis for testing purposes can generate alerts. Consider excluding specific development servers or user accounts from the rule to reduce noise.
- Security tools or monitoring solutions that simulate attacks for testing purposes may inadvertently trigger the rule. Coordinate with security teams to whitelist these tools or their specific test scenarios.

### Response and remediation

- Immediately isolate the affected IIS server from the network to prevent further unauthorized access and potential data exfiltration.
- Terminate any suspicious processes related to aspnet_regiis.exe to halt any ongoing decryption attempts.
- Conduct a thorough review of IIS server logs and webshell activity to identify the source of the compromise and any other affected systems.
- Change all credentials associated with the decrypted connection strings, including database passwords and service account credentials, to prevent unauthorized access.
- Restore the IIS server from a known good backup taken before the compromise, ensuring that any webshells or malicious scripts are removed.
- Implement enhanced monitoring and alerting for any future unauthorized use of aspnet_regiis.exe, focusing on the specific arguments used in the detection query.
- Escalate the incident to the security operations center (SOC) or relevant incident response team for further investigation and to assess the broader impact on the organization.
