---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "GenAI Process Connection to Suspicious Top Level Domain" prebuilt detection rule.'
---

# GenAI Process Connection to Suspicious Top Level Domain

## Triage and analysis

### Investigating GenAI Process Connection to Suspicious Top Level Domain

This rule detects GenAI tools connecting to domains with TLDs commonly abused by malware. The suspicious TLD filter makes this a high-signal rule with low expected volume.

### Possible investigation steps

- Review the GenAI process command line to identify which tool is running and verify if it's an expected/authorized tool.
- Examine the network connection details (destination IP, port, protocol) to understand the nature of the communication.
- Check the process execution chain to identify the full attack path and initial entry point.
- Investigate the user account associated with the GenAI process to determine if this activity is expected for that user.
- Review network traffic patterns to identify data exfiltration or command and control communications.
- Check for other alerts or suspicious activity on the same host around the same time.
- Verify if the GenAI tool is from a trusted source and if it's authorized for use in your environment.
- Confirm whether the suspicious domain is used by package registries, CDN mirrors, or AI plugin repos.
- Check if the GenAI tool attempted follow-up actions such as downloading scripts, connecting to IPs directly, or loading remote models.
- Inspect whether the domain matches prompt-redirections, malicious AI plugins, or compromised package dependencies.

### False positive analysis

- Legitimate GenAI tools may occasionally connect to domains using suspicious TLDs if they're legitimate services.
- Package managers (npx, pnpm, yarn, bunx) may connect to package registries or CDNs that use suspicious TLDs. Review and exclude known legitimate package registries if needed.
- Some third-party AI plugin ecosystems (VSCode AI plugins, Cursor extensions) may download assets from unusual TLDs; verify allowlists.

### Response and remediation

- Terminate the GenAI process and any spawned child processes to stop the malicious activity.
- Review and revoke any API keys, tokens, or credentials that may have been exposed or used by the GenAI tool.
- Block the identified suspicious domains at the network level.
- Investigate the GenAI tool configuration to identify how it was configured and what it was authorized to access.
- Update security policies to restrict or monitor GenAI tool usage in the environment, especially for network communications.
- Add detection for secondary indicators (reverse shells, encoded C2 traffic, odd user-agent strings).
