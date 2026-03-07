---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Reverse Shell via Java" prebuilt detection rule.'
---

# Potential Reverse Shell via Java

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential Reverse Shell via Java

Java applications, often run on Linux systems, can be exploited by adversaries to establish reverse shells, allowing remote control over a compromised system. Attackers may execute shell commands via Java processes post-network connection. The detection rule identifies suspicious Java activity by monitoring for shell executions following network connections, excluding benign processes, to flag potential reverse shell attempts.

### Possible investigation steps

- Review the network connection details, focusing on the destination IP address to determine if it is external or potentially malicious, as the rule excludes common internal and reserved IP ranges.
- Examine the Java process that initiated the network connection, including its executable path and arguments, to identify any unusual or unauthorized JAR files being executed.
- Investigate the child shell process spawned by the Java application, checking its command-line arguments and execution context to assess if it aligns with known reverse shell patterns.
- Cross-reference the parent Java process and the child shell process with known benign applications or services, such as Jenkins or NetExtender, to rule out false positives.
- Analyze historical data for the host to identify any previous similar activities or patterns that might indicate a persistent threat or repeated exploitation attempts.

### False positive analysis

- Java-based administrative tools like Jenkins may trigger false positives when executing shell commands. Exclude known benign Java applications such as Jenkins by adding their specific JAR paths to the exception list.
- Automated scripts or maintenance tasks that use Java to execute shell commands can be mistaken for reverse shell activity. Identify and exclude these scripts by specifying their unique process arguments or executable paths.
- Development environments where Java applications frequently execute shell commands for testing purposes can generate false alerts. Consider excluding these environments by filtering based on specific host identifiers or network segments.
- Security tools that utilize Java for network operations and shell executions might be flagged. Verify and exclude these tools by adding their process names or executable paths to the exception list.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further unauthorized access or data exfiltration.
- Terminate any suspicious Java processes identified in the alert to stop potential reverse shell activity.
- Conduct a thorough review of the affected system's logs to identify any additional indicators of compromise or lateral movement attempts.
- Remove any unauthorized or malicious Java JAR files and associated scripts from the system.
- Apply security patches and updates to the Java environment and any other vulnerable software on the affected host.
- Restore the system from a known good backup if any unauthorized changes or persistent threats are detected.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to assess the potential impact on other systems within the network.
