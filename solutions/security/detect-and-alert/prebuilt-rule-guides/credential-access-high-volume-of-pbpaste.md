---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: 'Investigation guide for the "Suspicious pbpaste High Volume Activity" prebuilt detection rule.'
---

# Suspicious pbpaste High Volume Activity

## Triage and analysis

To investigate `pbpaste` activity, focus on determining whether the binary is being used maliciously to collect clipboard data. Follow these steps:

> **Note**:
> This investigation guide uses the [Investigate Markdown Plugin](https://www.elastic.co/guide/en/security/current/interactive-investigation-guides.html) introduced in Elastic Stack version 8.8.0. Older Elastic Stack versions will display unrendered Markdown in this guide.

1. **Identify Frequency and Pattern of Execution:**
   - **What to check:** Analyze the frequency and timing of `pbpaste` executions. Look for consistent intervals that might indicate a script or loop is running.
   - **Why:** A high volume of regular `pbpaste` executions could suggest a bash loop designed to continuously capture clipboard data.

2. **Examine Associated Scripts or Processes:**
   - **What to check:** Investigate the parent processes or scripts invoking `pbpaste`. Look for any cron jobs, bash scripts, or automated tasks linked to these executions.
   - **Why:** Understanding what is triggering `pbpaste` can help determine if this activity is legitimate or part of a malicious attempt to gather sensitive information.
   - $investigate_1
   - $investigate_2

3. **Review Clipboard Contents:**
   - **What to check:** If possible, capture and review the clipboard contents during `pbpaste` executions to identify if sensitive data, such as user credentials, is being targeted.
   - **Why:** Attackers may use `pbpaste` to harvest valuable information from the clipboard. Identifying the type of data being collected can indicate the severity of the threat.

4. **Check for Data Exfiltration:**
   - **What to check:** Investigate any output files or network activity associated with `pbpaste` usage. Look for signs that the collected data is being saved to a file, transmitted over the network, or sent to an external location.
   - **Why:** If data is being stored or transmitted, it may be part of an exfiltration attempt. Identifying this can help prevent sensitive information from being leaked.

5. **Correlate with User Activity:**
   - **What to check:** Compare the `pbpaste` activity with the user’s normal behavior and system usage patterns.
   - **Why:** If the `pbpaste` activity occurs during times when the user is not active, or if the user denies initiating such tasks, it could indicate unauthorized access or a compromised account.

By thoroughly investigating these aspects of `pbpaste` activity, you can determine whether this is part of a legitimate process or a potential security threat that needs to be addressed.
