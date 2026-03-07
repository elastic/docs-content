---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Investigation guide for the "GenAI Process Compiling or Generating Executables" prebuilt detection rule.
---

# GenAI Process Compiling or Generating Executables

## Triage and analysis

### Investigating GenAI Process Compiling or Generating Executables

This rule detects GenAI tools spawning compilers or packaging tools. While developers may use GenAI to write code that they then compile, autonomous compilation by GenAI processes is unusual.

### Possible investigation steps

- Review the GenAI process that spawned the compiler to identify which tool is running and verify if it's an expected/authorized tool.
- Investigate the user account associated with the GenAI process to determine if this activity is expected for that user.
- Review the output files created by the compilation process to identify any malicious executables.
- Check for other alerts or suspicious activity on the same host around the same time.
- Verify if the GenAI tool is from a trusted source and if it's authorized for use in your environment.
- Identify whether the generated executables appear in temporary directories often used for malware staging (`%TEMP%`, `/tmp`, `.cache`).
- Inspect the compiled artifacts for networking imports, credential harvesting functionality, or persistence mechanisms.

### False positive analysis

- Legitimate development workflows that use GenAI tools for code generation may trigger this rule if they compile the generated code.
- Some GenAI-assisted coding IDEs (Cursor, Copilot Workspace) may run compilation tasks when testing code; confirm whether the behavior is tied to developer workflow.

### Response and remediation

- Terminate the GenAI process and any spawned compiler processes to stop the malicious activity.
- Investigate the compiled executables to determine if they are malicious.
- Review audit logs to determine the scope of compilation activity and identify any executables that may have been created.
- Quarantine any compiled binaries; submit suspicious artifacts to sandbox or malware analysis.

