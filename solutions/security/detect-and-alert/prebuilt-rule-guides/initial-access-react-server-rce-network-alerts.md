---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "React2Shell Network Security Alert" prebuilt detection rule.
---

# React2Shell Network Security Alert

## Triage and analysis

### Investigating React2Shell Network Security Alert

This rule detects exploitation attempts targeting CVE-2025-55182, a critical remote code execution vulnerability in React's Flight protocol used by Next.js and other RSC implementations. The vulnerability stems from insecure prototype chain traversal in the Flight deserializer, allowing attackers to access `__proto__`, `constructor`, and ultimately the `Function` constructor to execute arbitrary code.

### Possible investigation steps

- Examine the full HTTP request body to identify the specific attack payload and command being executed.
- Check the response body for `E{"digest":"..."}` patterns which contain command output from successful exploitation.
- Identify the target application and verify if it runs vulnerable React (< 19.1.0) or Next.js (< 15.3.2) versions.
- Review the source IP for other reconnaissance or exploitation attempts against web applications.
- Check for the `Next-Action` header which is required for the exploit to work.
- Correlate with process execution logs to identify if child processes (e.g., shell commands) were spawned by the Node.js process.

### False positive analysis

- Legitimate React Server Components traffic will NOT contain `__proto__`, `constructor:constructor`, or code execution patterns.
- Security scanning tools like react2shell-scanner may trigger this rule during authorized penetration testing.
- The combination of prototype pollution patterns with RSC-specific syntax is highly indicative of malicious activity.

### Response and remediation

- Immediately update affected applications: React >= 19.1.0, Next.js >= 15.3.2.
- Block the source IP at the WAF/reverse proxy if exploitation is confirmed.
- If HTTP 500 or 303 responses with `digest` output were observed, assume successful code execution and investigate for compromise.
- Review server logs for evidence of command execution (file creation, network connections, process spawning).
- Implement WAF rules to block requests containing `__proto__` or `constructor:constructor` in POST bodies.

