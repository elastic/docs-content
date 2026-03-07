---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Microsoft Build Engine Started by a Script Process" prebuilt detection rule.'
---

# Microsoft Build Engine Started by a Script Process

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Microsoft Build Engine Started by a Script Process

The Microsoft Build Engine (MSBuild) is a platform for building applications, typically invoked by developers. However, adversaries exploit its ability to execute inline tasks, using it as a proxy for executing malicious code. The detection rule identifies unusual MSBuild invocations initiated by script interpreters, signaling potential misuse for stealthy execution or defense evasion tactics.

### Possible investigation steps

- Review the process tree to understand the parent-child relationship, focusing on the parent process names such as cmd.exe, powershell.exe, pwsh.exe, powershell_ise.exe, cscript.exe, wscript.exe, or mshta.exe, which initiated the msbuild.exe process.
- Examine the command line arguments used to start msbuild.exe to identify any suspicious or unusual inline tasks or scripts that may indicate malicious activity.
- Check the user account associated with the msbuild.exe process to determine if it aligns with expected usage patterns or if it might be compromised.
- Investigate the timing and frequency of the msbuild.exe execution to see if it coincides with known legitimate build activities or if it appears anomalous.
- Look for any related network activity or file modifications around the time of the msbuild.exe execution to identify potential data exfiltration or further malicious actions.
- Cross-reference the alert with other security events or logs to identify any correlated indicators of compromise or additional suspicious behavior.

### False positive analysis

- Development environments where scripts are used to automate builds may trigger this rule. To manage this, identify and whitelist specific script processes or directories commonly used by developers.
- Automated testing frameworks that utilize scripts to initiate builds can cause false positives. Exclude these processes by creating exceptions for known testing tools and their associated scripts.
- Continuous integration/continuous deployment (CI/CD) pipelines often use scripts to invoke MSBuild. Consider excluding the parent processes associated with these pipelines from the rule.
- Administrative scripts that perform legitimate system maintenance tasks might start MSBuild. Review and exclude these scripts if they are verified as non-threatening.
- Custom scripts developed in-house for specific business functions may also trigger alerts. Conduct a review of these scripts and exclude them if they are deemed safe and necessary for operations.

### Response and remediation

- Isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Terminate the suspicious MSBuild process and any associated script interpreter processes (e.g., cmd.exe, powershell.exe) to stop the execution of potentially malicious code.
- Conduct a thorough scan of the affected system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any malicious payloads or artifacts.
- Review and analyze the parent script or command that initiated the MSBuild process to understand the scope and intent of the attack, and identify any additional compromised systems or accounts.
- Reset credentials for any user accounts that were active on the affected system during the time of the alert to prevent unauthorized access.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are affected.
- Implement enhanced monitoring and logging for MSBuild and script interpreter activities across the network to detect and respond to similar threats in the future.
