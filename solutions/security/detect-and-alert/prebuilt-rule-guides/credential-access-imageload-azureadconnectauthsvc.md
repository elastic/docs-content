---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Untrusted DLL Loaded by Azure AD Sync Service" prebuilt detection rule.'
---

# Untrusted DLL Loaded by Azure AD Sync Service

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Untrusted DLL Loaded by Azure AD Sync Service

Azure AD Sync Service facilitates identity synchronization between on-premises directories and Azure AD, crucial for seamless authentication. Adversaries may exploit this by loading malicious DLLs to intercept credentials. The detection rule identifies untrusted DLLs loaded by the Azure AD Sync process, focusing on those lacking valid signatures and excluding known safe paths, thus highlighting potential credential access threats.

### Possible investigation steps

- Review the process details for AzureADConnectAuthenticationAgentService.exe to confirm its legitimacy and check for any unusual behavior or anomalies.
- Examine the specific DLL file path that triggered the alert to determine if it is located in an unexpected or suspicious directory.
- Investigate the code signature status of the DLL to understand why it is untrusted, and verify if the DLL should have a valid signature.
- Check the system for any recent changes or installations that could have introduced the untrusted DLL, focusing on the timeframe around the alert.
- Analyze the event logs for any other suspicious activities or related alerts that might indicate a broader compromise or attack pattern.
- Correlate the alert with other security tools or logs to gather additional context and determine if this is part of a larger attack campaign.

### False positive analysis

- DLLs from legitimate software updates or installations may trigger alerts if they are not yet recognized as trusted. Users can monitor these occurrences and verify the legitimacy of the software source before adding exceptions.
- Custom or in-house developed applications might load DLLs that lack valid signatures. Users should ensure these applications are from a trusted source and consider signing them or adding their paths to the exclusion list.
- DLLs located in non-standard directories that are part of legitimate software operations can be flagged. Users should verify the software's legitimacy and update the exclusion list with these specific paths if necessary.
- Temporary files or DLLs created during software installation or updates might be flagged. Users should confirm the installation process and temporarily exclude these paths during the update period.
- Security or monitoring tools that dynamically load DLLs for legitimate purposes may be misidentified. Users should verify the tool's activity and add it to the exclusion list if it is deemed safe.

### Response and remediation

- Immediately isolate the affected Azure AD Sync server from the network to prevent further unauthorized access or data exfiltration.
- Terminate the AzureADConnectAuthenticationAgentService.exe process to stop the execution of the untrusted DLL and prevent potential credential dumping.
- Conduct a thorough review of the loaded DLLs on the affected server to identify and remove any malicious or unauthorized files.
- Restore the server from a known good backup taken before the incident to ensure the system is free from compromise.
- Change all credentials that may have been exposed or compromised, focusing on those related to Azure AD and on-premises directory services.
- Implement application whitelisting to prevent unauthorized DLLs from being loaded by critical processes like Azure AD Sync.
- Escalate the incident to the security operations center (SOC) for further investigation and to determine if additional systems are affected.
