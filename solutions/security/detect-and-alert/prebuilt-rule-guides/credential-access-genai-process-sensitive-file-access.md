---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "GenAI Process Accessing Sensitive Files" prebuilt detection rule.'
---

# GenAI Process Accessing Sensitive Files

## Triage and analysis

### Investigating GenAI Process Accessing Sensitive Files

This rule detects GenAI tools accessing credential files, SSH keys, browser data, or shell configurations. While GenAI tools legitimately access project files, access to sensitive credential stores is unusual and warrants investigation.

### Possible investigation steps

- Review the GenAI process that triggered the alert to identify which tool is being used and verify if it's an expected/authorized tool.
- Investigate the user account associated with the GenAI process to determine if this activity is expected for that user.
- Review the types of sensitive files being accessed (credentials, keys, browser data, etc.) to assess the potential impact of credential harvesting or data exfiltration.
- Check for other alerts or suspicious activity on the same host around the same time, particularly network exfiltration events.
- Verify if the GenAI tool or extension is from a trusted source and if it's authorized for use in your environment.
- Determine if the GenAI process accessed multiple sensitive directories in sequence, an indication of credential harvesting.
- Check if the GenAI tool recently created or accessed AI agent config files, which may contain instructions enabling autonomous file scanning.
- Review whether the access was preceded by an MCP server, LangChain agent, or background automation.

### False positive analysis

- Automated security scanning or auditing tools that leverage GenAI may access sensitive files as part of their normal operation.
- Development workflows that use GenAI tools for code analysis may occasionally access credential files.

### Response and remediation

- Immediately review the GenAI process that accessed the documents to determine if it's compromised or malicious.
- Review, rotate, and revoke any API keys, tokens, or credentials that may have been exposed or used by the GenAI tool.
- Investigate the document access patterns to determine the scope of potential data exfiltration.
- Update security policies to restrict or monitor GenAI tool usage in the environment, especially for access to sensitive files.
