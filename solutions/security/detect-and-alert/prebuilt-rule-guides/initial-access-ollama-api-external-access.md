---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Ollama API Accessed from External Network" prebuilt detection rule.'
---

# Ollama API Accessed from External Network

## Triage and analysis

### Investigating Ollama API Accessed from External Network

This rule detects when Ollama accepts connections from external IP addresses. Ollama binds to localhost:11434 by default but can be exposed via OLLAMA_HOST. Since Ollama lacks authentication, exposed instances allow unauthenticated model theft, prompt injection, and resource hijacking.

### Possible investigation steps

- Check the OLLAMA_HOST environment variable to determine if external exposure was intentional.
- Review the source IP address to identify if it's a known attacker, scanner, or miscategorized internal system.
- Examine Ollama logs for suspicious API calls to /api/pull, /api/push, or /api/generate.
- Check ~/.ollama/models/ for unexpected model downloads that may indicate model poisoning.
- Review network traffic for data exfiltration following the connection.
- Look for child processes spawned by Ollama that may indicate exploitation.

### False positive analysis

- Internal networks not properly classified in CIDR ranges may trigger false positives.
- Load balancers or reverse proxies accessing Ollama from external-facing IPs within trusted infrastructure.
- Legitimate remote access through VPN or authenticated proxy (add proxy IPs to exclusions).

### Response and remediation

- Restrict access immediately by setting OLLAMA_HOST=127.0.0.1:11434 or applying firewall rules.
- If exploitation is suspected, stop Ollama and audit ~/.ollama/models/ for unauthorized models.
- Review Ollama and system logs for signs of compromise.
- Consider running Ollama in a container with network isolation.
