---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "GenAI Process Performing Encoding/Chunking Prior to Network Activity" prebuilt detection rule.
---

# GenAI Process Performing Encoding/Chunking Prior to Network Activity

## Triage and analysis

### Investigating GenAI Process Performing Encoding/Chunking Prior to Network Activity

GenAI processes performing encoding or chunking operations followed by network activity is highly suspicious. This behavior indicates data preparation for exfiltration via GenAI prompts or agents, which is a strong indicator of malicious activity.

### Possible investigation steps

- Review the GenAI process that performed the encoding to identify which tool is running and verify if it's an expected/authorized tool.
- Examine the encoding/chunking command line arguments to understand what data is being processed.
- Review the network connection details to identify the destination and determine if it's expected.
- Investigate the user account associated with the GenAI process to determine if this activity is expected for that user.
- Review the data that was encoded to determine if it contains sensitive information.
- Determine whether the encoding was initiated by a GenAI agent or automation loop rather than a user action.
- Check whether the encoded data size or entropy suggests credential files, browser data, SSH keys, or cloud tokens.
- Validate that the GenAI tool is installed from a trusted source and has not been modified.

### False positive analysis

- Legitimate data processing workflows that use GenAI tools may trigger this rule if they encode data before transmission.
- Some local developer workflows may encode files before uploading training data or embeddings; confirm whether the host is a model-development workstation.

### Response and remediation

- Terminate the GenAI process and any spawned encoding/network processes to stop the malicious activity.
- Review and revoke any API keys, tokens, or credentials that may have been exposed or used by the GenAI tool.
- Investigate the encoded data and network destination to determine the scope of potential data exfiltration.

