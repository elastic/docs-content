---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "GenAI Process Connection to Unusual Domain" prebuilt detection rule.'
---

# GenAI Process Connection to Unusual Domain

## Triage and analysis

### Investigating GenAI Process Connection to Unusual Domain

GenAI tools with network access can be weaponized to contact attacker infrastructure for C2, data exfiltration, or payload retrieval. Compromised MCP servers, malicious plugins, or prompt injection attacks can redirect AI agents to connect to arbitrary domains. While legitimate GenAI tools connect to vendor APIs and CDNs, connections to unusual domains may indicate exploitation.

### Possible investigation steps

- Review the destination domain to determine if it's a legitimate GenAI service, CDN, package registry, or potentially malicious infrastructure.
- Investigate the GenAI process command line and configuration to identify what triggered the connection (plugin, MCP server, user prompt).
- Check if the domain was recently registered, uses a suspicious TLD, or has a low reputation score in threat intelligence feeds.
- Review the timing and context of the connection to determine if it correlates with user activity or was automated.
- Examine network traffic to and from the domain to identify the nature of the communication (API calls, file downloads, data exfiltration).
- Check for other hosts in the environment connecting to the same domain to determine if this is an isolated incident.
- Investigate whether the GenAI tool's configuration files were recently modified to add new MCP servers or plugins.
- Correlate with file events to see if the GenAI tool downloaded or created files around the same time as the connection.

### False positive analysis

- GenAI tools may connect to new domains as vendors update their infrastructure, CDNs, or API endpoints.
- Package managers (npm, pip) used by MCP servers may connect to package registries for dependency resolution.
- Legitimate MCP servers and AI plugins connect to their respective backend services.
- Developer workflows testing new AI integrations or MCP servers will naturally trigger alerts for novel domain connections.

### Response and remediation

- If the domain is confirmed malicious, block it at the network level and investigate the source of the compromise.
- Review the GenAI tool's configuration for unauthorized MCP servers, plugins, or extensions that initiated the connection.
- Investigate any data that may have been sent to the suspicious domain and assess the potential for data exfiltration.
- Review and rotate any API keys, tokens, or credentials used by the GenAI tool.
- Update detection rules to monitor the identified domain across all hosts in the environment.
