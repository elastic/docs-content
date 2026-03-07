---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Preload Environment Variable Process Execution" prebuilt detection rule.
---

# Unusual Preload Environment Variable Process Execution

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Preload Environment Variable Process Execution

In Linux environments, preload environment variables can dictate which libraries are loaded into a process, potentially altering its behavior. Adversaries exploit this by injecting malicious libraries to hijack execution flow, achieving persistence or evasion. The detection rule identifies atypical environment variables during process execution, signaling potential misuse by attackers.

### Possible investigation steps

- Review the process details associated with the alert, focusing on the process name, command line, and any unusual environment variables listed in process.env_vars.
- Investigate the parent process to understand the context of how the process was initiated and whether it aligns with expected behavior.
- Check the history of the process and its associated user account to identify any recent changes or suspicious activities that might indicate compromise.
- Analyze the libraries or binaries specified in the environment variables to determine if they are legitimate or potentially malicious.
- Cross-reference the process and environment variables with known threat intelligence sources to identify any matches with known malicious activity.
- Examine system logs and other related alerts around the same timeframe to identify any correlated or supporting evidence of malicious activity.

### False positive analysis

- Development and testing environments often use custom preload variables to test new libraries, which can trigger false positives. Users should identify and whitelist these known variables to prevent unnecessary alerts.
- Some legitimate software applications may use uncommon preload environment variables for performance optimization or compatibility reasons. Users can create exceptions for these applications by verifying their source and behavior.
- System administrators might employ preload variables for system tuning or debugging purposes. Documenting and excluding these specific cases can help reduce false positives.
- Security tools and monitoring solutions might use preload variables as part of their operation. Ensure these tools are recognized and excluded from triggering alerts by maintaining an updated list of their known behaviors.
- Regularly review and update the list of excluded variables and processes to adapt to changes in the environment and software updates, ensuring that only non-threatening behaviors are excluded.

### Response and remediation

- Immediately isolate the affected system from the network to prevent further malicious activity and lateral movement.
- Terminate any suspicious processes identified with unusual preload environment variables to halt potential malicious execution.
- Conduct a thorough review of the affected system's environment variables and loaded libraries to identify and remove any unauthorized or malicious entries.
- Restore the affected system from a known good backup to ensure all malicious modifications are removed.
- Update and patch the system to the latest security standards to mitigate vulnerabilities that could be exploited for similar attacks.
- Monitor the network and system logs for any signs of re-infection or similar suspicious activity, focusing on process execution patterns.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if additional systems are compromised.
