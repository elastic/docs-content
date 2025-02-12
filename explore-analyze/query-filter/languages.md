---
applies:
  stack:
  serverless:
---
  
# Query languages [search-analyze-query-languages]

{{es}} provides a number of query languages for interacting with your data.


| Name | Description | Use cases | API endpoint |
| --- | --- | --- | --- |
| [Query DSL](languages/querydsl.md) | The primary query language for {{es}}. A powerful and flexible JSON-style language that enables complex queries. | Full-text search, semantic search, keyword search, filtering, aggregations, and more. | [`_search`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html) |
| [{{esql}}](languages/esql.md) | Introduced in **8.11**, the Elasticsearch Query Language ({{esql}}) is a piped query language language for filtering, transforming, and analyzing data. | Initially tailored towards working with time series data like logs and metrics.Robust integration with {{kib}} for querying, visualizing, and analyzing data.Does not yet support full-text search. | [`_query`](languages/esql-rest.md) |
| [EQL](languages/eql.md) | Event Query Language (EQL) is a query language for event-based time series data. Data must contain the `@timestamp` field to use EQL. | Designed for the threat hunting security use case. | [`_eql`](https://www.elastic.co/guide/en/elasticsearch/reference/current/eql-apis.html) |
| [Elasticsearch SQL](languages/sql.md) | Allows native, real-time SQL-like querying against {{es}} data. JDBC and ODBC drivers are available for integration with business intelligence (BI) tools. | Enables users familiar with SQL to query {{es}} data using familiar syntax for BI and reporting. | [`_sql`](https://www.elastic.co/guide/en/elasticsearch/reference/current/sql-apis.html) |
| [Kibana Query Language (KQL)](languages/kql.md) | {{kib}} Query Language (KQL) is a text-based query language for filtering data when you access it through the {{kib}} UI. | Use KQL to filter documents where a value for a field exists, matches a given value, or is within a given range. | N/A |

> {{esql}} does not yet support all the features of Query DSL. Look forward to new {{esql}} features and functionalities in each release.

