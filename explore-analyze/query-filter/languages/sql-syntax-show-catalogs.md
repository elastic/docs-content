---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-syntax-show-catalogs.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# SHOW CATALOGS [sql-syntax-show-catalogs]

```sql
SHOW CATALOGS
```

**Description**: List the available catalogs and their types.

```sql
SHOW CATALOGS;

     name         |     type
------------------+---------------
javaRestTest         |local
my_remote_cluster |remote
```

