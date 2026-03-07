---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Unusual Process Modifying GenAI Configuration File" prebuilt detection rule.
---

# Unusual Process Modifying GenAI Configuration File

## Triage and analysis

### Investigating Unusual Process Modifying GenAI Configuration File

Configuration files for GenAI tools like Cursor, Claude, Copilot, and Ollama control which MCP servers, plugins, and extensions are loaded. Attackers target these files to inject malicious MCP servers that execute arbitrary commands, exfiltrate data, or establish persistence. Threats include external processes (malware, compromised scripts, supply chain attacks) directly modifying configs, as well as prompt injection attacks that abuse the AI tool's own file access capabilities.

### Possible investigation steps

- Identify the process that modified the configuration file and determine if it's expected (GenAI tool, installer, user action) or suspicious (unknown script, malware).
- If the modifying process is NOT a GenAI tool, investigate its origin, parent process tree, and whether it was downloaded or executed from a suspicious location.
- If a GenAI tool made the modification, check recent user prompts or agent activity that may have triggered the config change via prompt injection.
- Review the contents of the modified configuration file for suspicious MCP server URLs, unauthorized plugins, or unusual agent permissions.
- Examine the process command line and parent process tree to identify how the modifying process was invoked.
- Check for other file modifications by the same process around the same time, particularly to other GenAI configs or startup scripts.
- Investigate whether the GenAI tool subsequently connected to unknown domains or spawned unusual child processes after the config change.

### False positive analysis

- Novel but legitimate configuration changes will trigger this rule when the process hasn't been seen modifying these files within the configured history window. Review the modified file content to determine legitimacy.
- GenAI tool updates may modify config files in new ways; correlate with recent software updates.
- IDE extensions integrating with GenAI tools may modify configs as part of initial setup.
- Developer tools (git, go, npm) checking out or downloading projects containing `.gemini/` or `.claude/` directories may trigger alerts. These are project-level configs, not user configs - verify by checking if the path is within a project directory.

### Response and remediation

- Review the modified configuration file and revert any unauthorized changes to MCP servers, plugins, or agent settings.
- If malicious MCP servers were added, block the associated domains at the network level.
- Review and rotate any API keys or credentials that may have been exposed through the compromised GenAI configuration.

