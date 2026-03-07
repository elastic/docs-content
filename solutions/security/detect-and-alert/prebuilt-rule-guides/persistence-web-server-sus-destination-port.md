---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Uncommon Destination Port Connection by Web Server" prebuilt detection rule.
---

# Uncommon Destination Port Connection by Web Server

 ## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Uncommon Destination Port Connection by Web Server

Web servers, crucial for hosting applications, typically communicate over standard ports like 80 and 443. Adversaries may exploit web server processes to establish unauthorized connections to unusual ports, potentially indicating web shell activity or data exfiltration. This detection rule identifies such anomalies by monitoring egress connections from web server processes to non-standard ports, excluding common local IP ranges, thus highlighting potential threats.

### Possible investigation steps

- Review the process name and user associated with the alert to determine if the connection attempt was made by a legitimate web server process or user, as specified in the query fields (e.g., process.name or user.name).
- Examine the destination IP address to assess whether it is known or suspicious, and check if it falls outside the excluded local IP ranges.
- Investigate the destination port to understand why the connection was attempted on a non-standard port, and determine if this port is associated with any known services or threats.
- Check historical logs for any previous connection attempts from the same process or user to the same or similar destination IPs and ports to identify patterns or repeated behavior.
- Analyze any related network traffic or logs to identify additional context or anomalies that may indicate unauthorized activity or data exfiltration.
- Correlate the alert with other security events or alerts to determine if it is part of a larger attack pattern or campaign.

### False positive analysis

- Routine administrative tasks or maintenance scripts may trigger alerts if they involve web server processes connecting to non-standard ports. To manage this, identify and document these tasks, then create exceptions for the specific processes and ports involved.
- Internal monitoring or management tools that use non-standard ports for legitimate purposes can cause false positives. Review the tools in use and exclude their known IP addresses and ports from the rule.
- Development or testing environments often use non-standard ports for web server processes. Ensure these environments are well-documented and consider excluding their IP ranges or specific ports from the rule.
- Load balancers or reverse proxies might redirect traffic to non-standard ports as part of their normal operation. Verify the configuration of these devices and exclude their IP addresses and ports if necessary.
- Custom applications running on web servers may require communication over non-standard ports. Work with application owners to understand these requirements and adjust the rule to exclude these specific cases.

### Response and remediation

- Immediately isolate the affected web server from the network to prevent further unauthorized access or data exfiltration.
- Conduct a thorough review of the web server's logs and processes to identify any unauthorized changes or suspicious activities, focusing on the processes and user accounts mentioned in the detection rule.
- Terminate any suspicious processes identified during the investigation that are not part of the standard operation of the web server.
- Change passwords and review permissions for the user accounts associated with the web server processes to ensure they have not been compromised.
- Restore the web server from a known good backup if any unauthorized changes or malware are detected, ensuring that the backup is free from compromise.
- Implement network segmentation to limit the web server's access to critical systems and data, reducing the potential impact of future incidents.
- Escalate the incident to the security operations team for further analysis and to determine if additional systems may be affected, ensuring comprehensive threat containment and remediation.

