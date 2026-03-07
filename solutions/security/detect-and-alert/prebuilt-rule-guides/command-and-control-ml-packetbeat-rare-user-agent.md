---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Unusual Web User Agent" prebuilt detection rule.'
---

# Unusual Web User Agent

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Web User Agent

User agents identify applications interacting with web servers, typically browsers. Adversaries exploit this by using non-standard user agents for malicious activities like data exfiltration or command-and-control. The 'Unusual Web User Agent' detection rule leverages machine learning to identify rare user agents, flagging potential threats from atypical processes, thus aiding in early threat detection.

### Possible investigation steps

- Review the specific user agent string that triggered the alert to determine if it matches known malicious patterns or tools like Burp or SQLmap.
- Identify the source and destination IP addresses involved in the alert to assess whether they are associated with known malicious activity or unusual geographic locations.
- Check the process that generated the unusual user agent to determine if it is a legitimate application or potentially malicious software.
- Analyze network traffic logs for additional context around the time of the alert to identify any related suspicious activities or patterns.
- Investigate any recent changes or installations on the system that could explain the presence of the unusual user agent, such as new software or updates.
- Correlate the alert with other security events or logs to see if there are any related indicators of compromise or ongoing threats.

### False positive analysis

- Non-malicious applications like weather monitoring or stock-trading programs may use uncommon user agents. Regularly review and whitelist these applications to prevent them from triggering false positives.
- Automated tools such as web scrapers or bots can generate unusual user agents. Identify and document these tools if they are part of legitimate business operations, and create exceptions for them in the detection rule.
- Internal scanners or monitoring tools might use non-standard user agents. Ensure these tools are recognized and excluded from alerts by updating the rule's exception list.
- Regularly update the list of known benign user agents to reflect changes in legitimate software and tools used within the organization, reducing unnecessary alerts.
- Collaborate with IT and security teams to maintain an up-to-date inventory of authorized applications and their user agents, ensuring that only truly suspicious activities are flagged.

### Response and remediation

- Isolate the affected system from the network to prevent further data exfiltration or command-and-control communication.
- Conduct a thorough scan of the isolated system using updated antivirus and anti-malware tools to identify and remove any malicious software.
- Review and analyze the logs of the affected system and network traffic to identify the source and scope of the unusual user agent activity.
- Block the identified malicious IP addresses or domains associated with the unusual user agent in the firewall and intrusion prevention systems.
- Update and patch all software and systems to close any vulnerabilities that may have been exploited by the adversary.
- Restore the affected system from a clean backup if malware removal is not feasible or if the system integrity is compromised.
- Report the incident to the appropriate internal teams and, if necessary, escalate to external cybersecurity authorities or partners for further investigation and support.
