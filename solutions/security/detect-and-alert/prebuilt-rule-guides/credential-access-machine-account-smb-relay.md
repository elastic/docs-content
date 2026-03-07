---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Machine Account Relay Attack via SMB" prebuilt detection rule.'
---

# Potential Machine Account Relay Attack via SMB

## Triage and analysis

### Investigating Potential Machine Account Relay Attack via SMB

### Possible investigation steps
- Compare the source.ip to the target server host.ip addresses to make sure it's indeed a remote use of the machine account.
- Examine the source.ip activities as this is the attacker IP address used to relay.
- Review all relevant activities such as services creation, file and process events on the target server within the same period.
- Verify the machine account names that end with a dollar sign ($) to ensure they match the expected hostnames, and investigate any discrepancies.
- Check the network logon types to confirm if they align with typical usage patterns for the identified machine accounts.
- Investigate the context of the source IP addresses that do not match the host IP, looking for any signs of unauthorized access or unusual network activity.
- Correlate the findings with other security logs and alerts to identify any patterns or additional indicators of compromise related to the potential relay attack.

### False positive analysis

- Machine accounts performing legitimate network logons from different IP addresses can trigger false positives. To manage this, identify and whitelist known IP addresses associated with legitimate administrative tasks or automated processes.
- Scheduled tasks or automated scripts that use machine accounts for network operations may be flagged. Review and document these tasks, then create exceptions for their associated IP addresses and hostnames.
- Load balancers or proxy servers that alter the source IP address of legitimate authentication requests can cause false alerts. Ensure these devices are accounted for in the network architecture and exclude their IP addresses from the rule.
- Temporary network reconfigurations or migrations might result in machine accounts appearing to log in from unexpected hosts. During such events, temporarily adjust the rule parameters or disable the rule to prevent unnecessary alerts.
- Regularly review and update the list of exceptions to ensure they reflect current network configurations and operational practices, minimizing the risk of overlooking genuine threats.

### Response and remediation

- Coordinate isolation of the affected domain controller with infrastructure and identity teams to contain the threat while preserving service availability and forensic evidence. Prioritize this step if active compromise or attacker persistence is confirmed.
- Reset the domain controller's machine account password, along with any accounts suspected to be compromised or exposed. Ensure strong, unique credentials are used and apply tiered credential hygiene where applicable.
- Analyze recent authentication logs, event logs, and network traffic, focusing on suspicious activity and the source IPs referenced in the alert. Correlate findings to identify any lateral movement or additional compromised systems.
- Strengthen network segmentation, especially between domain controllers, administrative workstations, and critical infrastructure. This limits the attack surface and impedes credential relay or reuse across systems.
- Escalate the incident to the SOC or incident response team to coordinate a full investigation, containment, and recovery plan. Ensure stakeholders are kept informed throughout the response.
- Enhance detection mechanisms by tuning alerts and deploying additional telemetry focused on credential relay patterns, anomalous authentication, and NTLM-related activity.
- Conduct a structured post-incident review, documenting findings, identifying control gaps, and updating playbooks, configurations, or security policies to reduce the likelihood of similar incidents in the future.
