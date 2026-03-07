---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "Execution via OpenClaw Agent" prebuilt detection rule.
---

# Execution via OpenClaw Agent

## Triage and analysis

### Investigating Execution via OpenClaw Agent

OpenClaw (formerly Clawdbot, rebranded to Moltbot) is a personal AI coding assistant that can execute shell commands 
and scripts on behalf of users. Malicious actors have weaponized the skill ecosystem (ClawHub) to distribute skills 
that execute download-and-execute commands, targeting cryptocurrency wallets and credentials.

### Possible investigation steps

- Verify if OpenClaw/Moltbot is an approved application in your organization.
- Review the child process command line for indicators of malicious activity (encoded payloads, remote downloads, credential access).
- Check the parent Node.js process command line to identify which OpenClaw component initiated the execution.
- Examine recently installed skills from ClawHub for malicious or obfuscated code.
- Correlate with network events to identify data exfiltration or C2 communication.
- Review the user's AI conversation history for prompt injection attempts.

### False positive analysis

- Developers legitimately using OpenClaw/Moltbot for AI-assisted coding may trigger this rule when the AI executes build scripts, curl commands, or other legitimate automation.
- If the tool is approved, consider tuning based on specific command patterns or adding exception lists.

### Response and remediation

- If the child process activity appears malicious, terminate the OpenClaw gateway and investigate the skill that initiated the command.
- Review and remove any suspicious skills from the OpenClaw configuration.
- If credentials may have been accessed, rotate affected secrets and API keys.
- Block known typosquat domains (moltbot.you, clawbot.ai, clawdbot.you) at the network level.

