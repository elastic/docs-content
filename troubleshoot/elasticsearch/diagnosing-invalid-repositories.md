---
navigation_title: Invalid repositories
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/diagnosing-invalid-repositories.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Diagnose invalid repositories [diagnosing-invalid-repositories]

When an {{es}} node faces an unexpected exception when trying to instantiate a snapshot repository, it will mark the repository as "invalid" and write a warning to the log file. Use the following steps to diagnose the underlying cause of this issue:

1. Retrieve the affected nodes from the affected resources section of the health report.
2. Refer to the logs of the affected node(s) and search for the repository name. You should be able to find logs that will contain relevant exception.
3. Try to resolve the errors reported.

