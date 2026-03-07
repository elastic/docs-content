---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Discovery Signal Alert with Unusual Process Command Line" prebuilt detection rule.
---

# Unusual Discovery Signal Alert with Unusual Process Command Line

## Triage and analysis

> **Disclaimer**:
> This investigation guide was created using generative AI technology and has been reviewed to improve its accuracy and relevance. While every effort has been made to ensure its quality, we recommend validating the content and adapting it to suit your specific environment and operational needs.

### Investigating Unusual Discovery Signal Alert with Unusual Process Command Line

This detection rule identifies anomalies in process command lines on Windows systems, which may indicate adversarial reconnaissance activities. Attackers often exploit legitimate discovery tools to gather system information stealthily. By monitoring unique combinations of host, user, and command line data, the rule flags deviations from normal behavior, helping analysts pinpoint potential threats early.

### Possible investigation steps

- Review the alert details to identify the specific host.id, user.id, and process.command_line that triggered the alert. This will help in understanding the context of the anomaly.
- Check the historical activity of the identified host.id and user.id to determine if the process.command_line has been executed previously and assess if this behavior is truly unusual.
- Investigate the process.command_line for any known malicious patterns or suspicious commands that could indicate reconnaissance or other adversarial activities.
- Correlate the alert with other security events or logs from the same host or user around the same time to identify any additional suspicious activities or patterns.
- Consult threat intelligence sources to see if the process.command_line or any associated indicators have been reported in recent threat campaigns or advisories.
- If necessary, isolate the affected host to prevent potential lateral movement or further compromise while the investigation is ongoing.

### False positive analysis

- Legitimate administrative tools may trigger alerts when used by IT staff for routine system checks. To manage this, create exceptions for known safe tools and processes frequently used by trusted users.
- Automated scripts or scheduled tasks that perform regular system audits can be flagged as unusual. Identify these scripts and add them to an allowlist to prevent unnecessary alerts.
- Software updates or installations that involve system discovery commands might be misidentified as threats. Monitor update schedules and exclude related processes during these times.
- Security software performing scans or inventory checks can mimic adversarial reconnaissance. Verify the processes associated with these tools and configure the rule to ignore them.
- New software deployments or changes in system configurations may temporarily alter normal command line behavior. Document these changes and adjust the rule settings to accommodate expected deviations.

### Response and remediation

- Isolate the affected host immediately to prevent further lateral movement or data exfiltration. Disconnect it from the network while maintaining power to preserve volatile data for forensic analysis.
- Terminate any suspicious processes identified by the alert, especially those with unusual command lines, to halt any ongoing malicious activity.
- Conduct a thorough review of the affected user's account for any unauthorized access or privilege escalation. Reset passwords and revoke any unnecessary permissions.
- Analyze the command line arguments and process execution context to understand the scope and intent of the reconnaissance activity. This may involve reviewing logs and correlating with other security events.
- Restore the affected system from a known good backup if any malicious changes or persistence mechanisms are detected. Ensure the backup is free from compromise.
- Update endpoint protection and intrusion detection systems with the latest threat intelligence to enhance detection capabilities against similar reconnaissance activities.
- Escalate the incident to the security operations center (SOC) or incident response team for further investigation and to determine if the activity is part of a larger attack campaign.
