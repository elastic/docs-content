---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "File Creation by Cups or Foomatic-rip Child" prebuilt detection rule.'
---

# File Creation by Cups or Foomatic-rip Child

## Triage and analysis

### Investigating File Creation by Cups or Foomatic-rip Child

This rule identifies potential exploitation attempts of several vulnerabilities in the CUPS printing system (CVE-2024-47176, CVE-2024-47076, CVE-2024-47175, CVE-2024-47177). These vulnerabilities allow attackers to send crafted IPP requests or manipulate UDP packets to execute arbitrary commands or modify printer configurations. Attackers can exploit these flaws to inject malicious data, leading to Remote Code Execution (RCE) on affected systems.

#### Possible Investigation Steps

- Investigate the incoming IPP requests or UDP packets targeting port 631.
- Examine the printer configurations on the system to determine if any unauthorized printers or URLs have been added.
- Investigate the process tree to check if any unexpected processes were triggered as a result of IPP activity. Review the executable files for legitimacy.
- Check for additional alerts related to the compromised system or user within the last 48 hours.
- Investigate network traffic logs for suspicious outbound connections to unrecognized domains or IP addresses.
- Check if any of the contacted domains or addresses are newly registered or have a suspicious reputation.
- Retrieve any scripts or executables dropped by the attack for further analysis in a private sandbox environment:
- Analyze potential malicious activity, including:
  - Attempts to communicate with external servers.
  - File access or creation of unauthorized executables.
  - Cron jobs, services, or other persistence mechanisms.

### Related Rules
- Cupsd or Foomatic-rip Shell Execution - 476267ff-e44f-476e-99c1-04c78cb3769d
- Printer User (lp) Shell Execution - f86cd31c-5c7e-4481-99d7-6875a3e31309
- Network Connection by Cups or Foomatic-rip Child - e80ee207-9505-49ab-8ca8-bc57d80e2cab
- Suspicious Execution from Foomatic-rip or Cupsd Parent - 986361cd-3dac-47fe-afa1-5c5dd89f2fb4

### False Positive Analysis

- This activity is rarely legitimate. However, verify the context to rule out non-malicious printer configuration changes or legitimate IPP requests.

### Response and Remediation

- Initiate the incident response process based on the triage outcome.
- Isolate the compromised host to prevent further exploitation.
- If the investigation confirms malicious activity, search the environment for additional compromised hosts.
- Implement network segmentation or restrictions to contain the attack.
- Stop suspicious processes or services tied to CUPS exploitation.
- Block identified Indicators of Compromise (IoCs), including IP addresses, domains, or hashes of involved files.
- Review compromised systems for backdoors, such as reverse shells or persistence mechanisms like cron jobs.
- Investigate potential credential exposure on compromised systems and reset passwords for any affected accounts.
- Restore the original printer configurations or uninstall unauthorized printer entries.
- Perform a thorough antimalware scan to identify any lingering threats or artifacts from the attack.
- Investigate how the attacker gained initial access and address any weaknesses to prevent future exploitation.
- Use insights from the incident to improve detection and response times in future incidents (MTTD and MTTR).
