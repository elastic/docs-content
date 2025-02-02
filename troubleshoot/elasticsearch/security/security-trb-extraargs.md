---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-trb-extraargs.html
---

# Users command fails due to extra arguments [security-trb-extraargs]

**Symptoms:**

* The `elasticsearch-users` command fails with the following message: `ERROR: extra arguments [...] were provided`.

**Resolution:**

This error occurs when the `elasticsearch-users` tool is parsing the input and finds unexpected arguments. This can happen when there are special characters used in some of the arguments. For example, on Windows systems the `,` character is considered a parameter separator; in other words `-r role1,role2` is translated to `-r role1 role2` and the `elasticsearch-users` tool only recognizes `role1` as an expected parameter. The solution here is to quote the parameter: `-r "role1,role2"`.

For more information about this command, see [`elasticsearch-users` command](https://www.elastic.co/guide/en/elasticsearch/reference/current/users-command.html).

