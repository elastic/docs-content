---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Suspicious Mining Process Creation Event" prebuilt detection rule.
---

# Suspicious Mining Process Creation Event

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Suspicious Mining Process Creation Event

Cryptomining exploits system resources to mine cryptocurrency, often without user consent, impacting performance and security. Adversaries may deploy mining services on Linux systems, disguising them as legitimate processes. The detection rule identifies the creation of known mining service files, signaling potential unauthorized mining activity. By monitoring these specific file creation events, security teams can swiftly respond to and mitigate cryptomining threats.

### Possible investigation steps

- Review the alert details to identify which specific mining service file was created, focusing on the file names listed in the query such as "aliyun.service" or "moneroocean_miner.service".
- Check the creation timestamp of the suspicious file to determine when the potential unauthorized mining activity began.
- Investigate the process that created the file by examining system logs or using process monitoring tools to identify the parent process and any associated command-line arguments.
- Analyze the system for additional indicators of compromise, such as unexpected network connections or high CPU usage, which may suggest active cryptomining.
- Verify the legitimacy of the file by comparing it against known hashes of legitimate services or using threat intelligence sources to identify known malicious files.
- Assess the system for any other suspicious activities or anomalies that may indicate further compromise or persistence mechanisms.

### False positive analysis

- Legitimate administrative scripts or services may create files with names similar to known mining services. Verify the origin and purpose of such files before taking action.
- System administrators might deploy custom monitoring or management services that inadvertently match the file names in the detection rule. Review and whitelist these services if they are confirmed to be non-threatening.
- Automated deployment tools or scripts could create service files as part of routine operations. Ensure these tools are properly documented and exclude them from the detection rule if they are verified as safe.
- Some legitimate software installations might use generic service names that overlap with those flagged by the rule. Cross-check with software documentation and exclude these from alerts if they are confirmed to be benign.

### Response and remediation

- Isolate the affected Linux system from the network to prevent further unauthorized mining activity and potential lateral movement by the adversary.
- Terminate any suspicious processes associated with the identified mining services, such as aliyun.service, moneroocean_miner.service, or others listed in the detection query.
- Remove the malicious service files from the system to prevent them from being restarted or reused by the attacker.
- Conduct a thorough scan of the system using updated antivirus or endpoint detection and response (EDR) tools to identify and remove any additional malware or persistence mechanisms.
- Review and update system and application patches to close any vulnerabilities that may have been exploited to deploy the mining services.
- Monitor network traffic for unusual outbound connections that may indicate communication with mining pools or command and control servers, and block these connections if detected.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to assess the potential impact on other systems within the network.
