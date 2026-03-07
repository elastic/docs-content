---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Potential Linux Tunneling and/or Port Forwarding" prebuilt detection rule.'
---

# Potential Linux Tunneling and/or Port Forwarding

## Triage and analysis

### Investigating Potential Linux Tunneling and/or Port Forwarding

Attackers can leverage many utilities to clandestinely tunnel network communications and evade security measures, potentially gaining unauthorized access to sensitive systems.

This rule looks for several utilities that are capable of setting up tunnel network communications by analyzing process names or command line arguments. 

> **Note**:
> This investigation guide uses the [Osquery Markdown Plugin](https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html) introduced in Elastic Stack version 8.5.0. Older Elastic Stack versions will display unrendered Markdown in this guide.
> This investigation guide uses [placeholder fields](https://www.elastic.co/guide/en/security/current/osquery-placeholder-fields.html) to dynamically pass alert data into Osquery queries. Placeholder fields were introduced in Elastic Stack version 8.7.0. If you're using Elastic Stack version 8.6.0 or earlier, you'll need to manually adjust this investigation guide's queries to ensure they properly run.

#### Possible investigation steps

- Identify any signs of suspicious network activity or anomalies that may indicate protocol tunneling. This could include unexpected traffic patterns or unusual network behavior.
  - Investigate listening ports and open sockets to look for potential protocol tunneling, reverse shells, or data exfiltration.
    - $osquery_0
    - $osquery_1
- Identify the user account that performed the action, analyze it, and check whether it should perform this kind of action.
  - $osquery_2
- Investigate whether the user is currently logged in and active.
  - $osquery_3
- Investigate the script execution chain (parent process tree) for unknown processes. Examine their executable files for prevalence and whether they are located in expected locations.
  - $osquery_4
  - $osquery_5
- Investigate other alerts associated with the user/host during the past 48 hours.
  - If scripts or executables were dropped, retrieve the files and determine if they are malicious:
    - Use a private sandboxed malware analysis system to perform analysis.
      - Observe and collect information about the following activities:
        - Attempts to contact external domains and addresses.
          - Check if the domain is newly registered or unexpected.
          - Check the reputation of the domain or IP address.
        - File access, modification, and creation activities.

### Related rules

- Potential Linux Tunneling and/or Port Forwarding via Command Line - 8c8df61f-ed2a-4832-87b8-ee30812606e0
- Potential Protocol Tunneling via Chisel Client - 3f12325a-4cc6-410b-8d4c-9fbbeb744cfd
- Potential Protocol Tunneling via Chisel Server - ac8805f6-1e08-406c-962e-3937057fa86f
- Potential Protocol Tunneling via EarthWorm - 9f1c4ca3-44b5-481d-ba42-32dc215a2769
- Suspicious Utility Launched via ProxyChains - 6ace94ba-f02c-4d55-9f53-87d99b6f9af4
- ProxyChains Activity - 4b868f1f-15ff-4ba3-8c11-d5a7a6356d37

### False positive analysis

- If this activity is related to new benign software installation activity, consider adding exceptions — preferably with a combination of user and command line conditions.
- If this activity is related to a system administrator or developer who uses port tunneling/forwarding for benign purposes, consider adding exceptions for specific user accounts or hosts. 
- Try to understand the context of the execution by thinking about the user, machine, or business purpose. A small number of endpoints, such as servers with unique software, might appear unusual but satisfy a specific business need.

### Response and remediation

- Initiate the incident response process based on the outcome of the triage.
- Isolate the involved host to prevent further post-compromise behavior.
- If the triage identified malware, search the environment for additional compromised hosts.
  - Implement temporary network rules, procedures, and segmentation to contain the malware.
  - Stop suspicious processes.
  - Immediately block the identified indicators of compromise (IoCs).
  - Inspect the affected systems for additional malware backdoors, such as reverse shells, reverse proxies, or droppers, that attackers could use to reinfect the system.
- Remove and block malicious artifacts identified during triage.
- Investigate credential exposure on systems compromised or used by the attacker to ensure all compromised accounts are identified. Reset passwords for these accounts and other potentially compromised credentials, such as email, business systems, and web services.
- Run a full antimalware scan. This may reveal additional artifacts left in the system, persistence mechanisms, and malware components.
- Determine the initial vector abused by the attacker and take action to prevent reinfection through the same vector.
- Leverage the incident response data and logging to improve the mean time to detect (MTTD) and the mean time to respond (MTTR).
