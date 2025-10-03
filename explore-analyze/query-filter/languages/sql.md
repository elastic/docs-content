---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/xpack-sql.html
navigation_title: SQL
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# SQL overview [sql-overview]

Elasticsearch SQL aims to provide a powerful yet lightweight SQL interface to {{es}}.

## What's SQL in {{es}}? [sql-introduction]

Elasticsearch SQL is a feature that allows SQL-like queries to be executed in real-time against {{es}}. Whether using the REST interface, command-line or JDBC, any client can use SQL to search and aggregate data *natively* inside {{es}}. One can think of Elasticsearch SQL as a *translator*, one that understands both SQL and {{es}} and makes it easy to read and process data in real-time, at scale by leveraging {{es}} capabilities.

## Why Elasticsearch SQL ? [sql-why]

Native integration
:   Elasticsearch SQL is built from the ground up for {{es}}. Each and every query is efficiently executed against the relevant nodes according to the underlying storage.

No external parts
:   No need for additional hardware, processes, runtimes or libraries to query {{es}}; Elasticsearch SQL eliminates extra moving parts by running *inside* the {{es}} cluster.

Lightweight and efficient
:   Elasticsearch SQL does not abstract {{es}} and its search capabilities - on the contrary, it embraces and exposes SQL to allow proper full-text search, in real-time, in the same declarative, succinct fashion.


## Reference documentation

:::{note}
 This overview page is in the Explore & Analyze section. All of the {{es}} SQL documentation lives in the **Reference** section.
:::

[Overview](elasticsearch://reference/query-languages/sql.md)
:   Overview of Elasticsearch SQL and its features.

[Getting Started](elasticsearch://reference/query-languages/sql/sql-getting-started.md)
:   Start using SQL right away in {{es}}.

[Concepts and Terminology](elasticsearch://reference/query-languages/sql/sql-concepts.md)
:   Language conventions across SQL and {{es}}.

[Security](elasticsearch://reference/query-languages/sql/sql-security.md)
:   Secure Elasticsearch SQL and {{es}}.

[REST API](elasticsearch://reference/query-languages/sql/sql-rest.md)
:   Execute SQL in JSON format over REST.

[Translate API](elasticsearch://reference/query-languages/sql/sql-translate.md)
:   Translate SQL in JSON format to {{es}} native query.

[CLI](elasticsearch://reference/query-languages/sql/sql-cli.md)
:   Command-line application for executing SQL against {{es}}.

[JDBC](elasticsearch://reference/query-languages/sql/sql-jdbc.md)
:   JDBC driver for {{es}}.

[ODBC](elasticsearch://reference/query-languages/sql/sql-odbc.md)
:   ODBC driver for {{es}}.

[Client Applications](elasticsearch://reference/query-languages/sql/sql-client-apps.md)
:   Setup various SQL/BI tools with Elasticsearch SQL.

[SQL Language](elasticsearch://reference/query-languages/sql/sql-spec.md)
:   Overview of the Elasticsearch SQL language, such as supported data types, commands and syntax.

[Functions and Operators](elasticsearch://reference/query-languages/sql/sql-functions.md)
:   List of functions and operators supported.

[Limitations](elasticsearch://reference/query-languages/sql/sql-limitations.md)
:   Elasticsearch SQL current limitations.

