---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/osquery-placeholder-fields.html
  - https://www.elastic.co/guide/en/serverless/current/security-osquery-placeholder-fields.html
applies_to:
  stack: all
  serverless:
    security: all
---

# Use placeholder fields in Osquery queries [security-osquery-placeholder-fields]

Instead of hard-coding alert and event values into Osquery queries, you can use placeholder fields to dynamically pass this data into queries. Placeholder fields function like parameters. You can use placeholder fields to build flexible and reusable queries.

Placeholder fields work in single queries or query packs. They’re also supported in the following features:

* [Live queries](/solutions/security/investigate/run-osquery-from-alerts.md)
* [Osquery Response Actions](/solutions/security/investigate/add-osquery-response-actions.md)
* [Investigation guides using Osquery queries](/solutions/security/investigate/run-osquery-from-investigation-guides.md)


## Placeholder field syntax and requirements [placeholder-field-syntax]

Placeholder fields use [mustache syntax](http://mustache.github.io/) and must be wrapped in double curly brackets (`{{example.field}}`). You can use any field within an event or alert document as a placeholder field.

Queries with placeholder fields can only run against alerts or events. Otherwise, they will lack the necessary values and the query status will be `error`.


### Example query with a placeholder field [placeholder-field-example]

The following query uses the `{{host.name}}` placeholder field:

```sql
SELECT * FROM os_version WHERE name = {{host.os.name}}
```

When you run the query, the value that’s stored in the alert or event’s `host.name` field will be transferred to the `{{host.os.name}}` placeholder field.

