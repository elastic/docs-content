---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Potential JAVA/JNDI Exploitation Attempt" prebuilt detection rule.
---

# Potential JAVA/JNDI Exploitation Attempt

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Potential JAVA/JNDI Exploitation Attempt

Java Naming and Directory Interface (JNDI) is a Java API that provides naming and directory functionality, allowing Java applications to discover and look up data and resources via a directory service. Adversaries exploit JNDI by injecting malicious payloads that trigger outbound connections to LDAP, RMI, or DNS services, potentially leading to remote code execution. The detection rule identifies such exploitation attempts by monitoring Java processes making suspicious outbound connections followed by the execution of potentially harmful child processes, such as shell scripts or scripting languages, indicating a possible compromise.

### Possible investigation steps

- Review the network logs to confirm the outbound connection attempt by the Java process to the specified ports (1389, 389, 1099, 53, 5353) and identify the destination IP addresses to determine if they are known malicious or suspicious entities.
- Examine the process tree to verify the parent-child relationship between the Java process and any suspicious child processes such as shell scripts or scripting languages (e.g., sh, bash, curl, python).
- Check the command line arguments and environment variables of the suspicious child processes to identify any potentially malicious payloads or commands being executed.
- Investigate the host's recent activity and logs for any other indicators of compromise or unusual behavior that might correlate with the suspected exploitation attempt.
- Assess the system for any unauthorized changes or new files that may have been introduced as a result of the exploitation attempt, focusing on directories commonly used by Java applications.

### False positive analysis

- Development and testing environments may trigger false positives when developers use Java applications to test connections to LDAP, RMI, or DNS services. To mitigate this, exclude known development servers or IP ranges from the detection rule.
- Automated scripts or maintenance tasks that involve Java applications making legitimate outbound connections to the specified ports can be mistaken for exploitation attempts. Identify and whitelist these scripts or tasks by their process names or hashes.
- Legitimate Java-based applications that require frequent updates or data retrieval from external services might generate similar network patterns. Monitor and document these applications, then create exceptions for their specific network behaviors.
- Security tools or monitoring solutions that use Java for network scanning or analysis might inadvertently match the rule's criteria. Ensure these tools are recognized and excluded by their process identifiers or network activity profiles.

### Response and remediation

- Immediately isolate the affected host from the network to prevent further outbound connections and potential lateral movement.
- Terminate any suspicious Java processes identified in the alert, especially those making outbound connections to LDAP, RMI, or DNS ports.
- Conduct a thorough review of the affected system for any unauthorized changes or additional malicious processes, focusing on child processes like shell scripts or scripting languages.
- Restore the affected system from a known good backup if unauthorized changes or malware are detected.
- Update and patch Java and any related applications to the latest versions to mitigate known vulnerabilities.
- Implement network-level controls to block outbound connections to suspicious or unauthorized LDAP, RMI, or DNS services from Java processes.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to assess the potential impact on other systems within the network.
