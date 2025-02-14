---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/endpoint-artifacts.html
  - https://www.elastic.co/guide/en/serverless/current/security-optimize-edr.html
---

# Optimize {{elastic-defend}} [endpoint-artifacts]

If you encounter problems like incompatibilities with other antivirus software, too many false positive alerts, or excessive storage or CPU usage, you can optimize {{elastic-defend}} to mitigate these issues.

Endpoint artifacts — such as trusted applications and event filters — and Endpoint exceptions let you modify the behavior and performance of *{{elastic-endpoint}}*, the component installed on each host that performs {{elastic-defend}}'s threat monitoring, prevention, and response actions.

The following table explains the differences between several Endpoint artifacts and exceptions, and how to use them:

|     |     |
| --- | --- |
| [Trusted application](trusted-applications.md) | **Prevents {{elastic-endpoint}} from monitoring a process.** Use to avoid conflicts with other software, usually other antivirus or endpoint security applications.<br><br> - Creates intentional blind spots in your security environment — use sparingly!<br>- Doesn’t monitor the application for threats, nor does it generate alerts, even if it behaves like malware, ransomware, etc.<br>- Doesn’t generate events for the application except process events for visualizations and other internal use by the {{stack}}.<br>- Might improve performance, since {{elastic-endpoint}} monitors fewer processes.<br>- Might still generate malicious behavior alerts, if the application’s process events indicate malicious behavior. To suppress alerts, create [Endpoint alert exceptions](../detect-and-alert/add-manage-exceptions.md#endpoint-rule-exceptions).<br> |
| [Event filter](event-filters.md) | **Prevents event documents from being written to {{es}}.** Use to reduce storage usage in {{es}}.<br><br>Does NOT lower CPU usage for {{elastic-endpoint}}. It still monitors event data for possible threats, but without writing event data to {{es}}.<br> |
| [Blocklist](blocklist.md) | **Prevents known malware from running.** Use to extend {{elastic-defend}}'s protection against malicious processes.<br><br>NOT intended to broadly block benign applications for non-security reasons.<br> |
| [Endpoint alert exception](../detect-and-alert/add-manage-exceptions.md#endpoint-rule-exceptions) | **Prevents {{elastic-endpoint}} from generating alerts or stopping processes.** Use to reduce false positive alerts, and to keep {{elastic-endpoint}} from preventing processes you want to allow.<br><br>Might also improve performance: {{elastic-endpoint}} checks for exceptions *before* most other processing, and stops monitoring a process if an exception allows it.<br> |
