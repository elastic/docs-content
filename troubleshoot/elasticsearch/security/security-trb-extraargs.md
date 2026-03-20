---
navigation_title: "Error: Extra arguments provided"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-trb-extraargs.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
---

# Error: Extra arguments were provided [security-trb-extraargs]

**Symptoms:**

* The `elasticsearch-users` command fails with the following message: `ERROR: extra arguments [...] were provided`.

**Resolution:**

This error occurs when the `elasticsearch-users` tool is parsing the input and finds unexpected arguments. This can happen when there are special characters used in some of the arguments. For example, on Windows systems the `,` character is considered a parameter separator; in other words `-r role1,role2` is translated to `-r role1 role2` and the `elasticsearch-users` tool only recognizes `role1` as an expected parameter. The solution here is to quote the parameter: `-r "role1,role2"`.

For more information about this command, see [`elasticsearch-users` command](elasticsearch://reference/elasticsearch/command-line-tools/users-command.md).

