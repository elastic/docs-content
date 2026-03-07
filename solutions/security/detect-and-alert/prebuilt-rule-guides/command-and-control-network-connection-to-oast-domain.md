---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Network Connection to OAST Domain via Script Interpreter" prebuilt detection rule.'
---

# Network Connection to OAST Domain via Script Interpreter

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Network Connection to OAST Domain via Script Interpreter

Out-of-Band Application Security Testing (OAST) services such as interact.sh, burpcollaborator.net, and similar platforms are designed for security testing to detect vulnerabilities through out-of-band data channels. However, threat actors abuse these same services for data exfiltration, command and control, and DNS-based exploitation. This detection rule identifies script interpreters or suspicious processes connecting to known OAST domains, which may indicate exploitation activity or unauthorized security testing.

### Possible investigation steps

- Verify with your security team whether authorized penetration testing or red team exercises are currently underway that would involve OAST services.
- Review the process.name and process.executable fields to identify which application initiated the OAST connection and determine if it is a known vulnerable application.
- Examine the dns.question.name field to capture the full OAST subdomain, as the subdomain often contains encoded data or unique identifiers used by attackers.
- Analyze the process.parent.executable and process.command_line to understand how the connecting process was spawned and identify the potential vulnerability being exploited.
- Check for any HTTP request or response data associated with the OAST connection to identify what data may have been exfiltrated.
- Investigate the user.name and host.name to determine the scope of affected systems and user accounts.
- Review web application logs and proxy data for injection attempts or exploitation activity that may have triggered the OAST callback.

### False positive analysis

- Authorized security researchers and penetration testers may use OAST services during sanctioned vulnerability assessments. Confirm testing windows with the security team before escalating.
- Bug bounty hunters testing your organization's applications may trigger OAST connections. Verify if bug bounty programs are active and expected.
- Security training or capture-the-flag exercises may involve OAST services for educational purposes. Confirm with training coordinators if such exercises are scheduled.
- Some commercial security scanning tools may use OAST-like services for vulnerability detection. Verify if automated security scanning is running.

### Response and remediation

- If unauthorized, immediately block the OAST domain at the network perimeter, DNS resolver, and proxy to prevent further communication.
- Isolate the affected system to prevent lateral movement or additional data exfiltration.
- Identify the vulnerable application or injection point that led to the OAST callback and apply emergency patches or mitigations.
- Review the OAST subdomain and any captured data to assess the scope of information exposure.
- Conduct a thorough code review of affected applications to identify and remediate the underlying vulnerability.
- Implement web application firewall rules to detect and block common injection patterns that lead to OAST exploitation.
- Escalate to the incident response team for further investigation if the activity indicates active exploitation or compromise.
