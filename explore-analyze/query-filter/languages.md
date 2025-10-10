---
applies_to:
  stack: ga
  serverless: ga
products:
 - id: elasticsearch
 - id: kibana
---
  
# Query languages [search-analyze-query-languages]

{{es}} provides a number of query languages for interacting with your data. You can use these languages programmatically when working with {{es}} and {{kib}} APIs in your application, or interactively using the {{kib}} UI.


| Name | Description | Use cases | API endpoint |
| --- | --- | --- | --- |
| **Query DSL** | {{es}}'s primary, most powerful and flexible JSON-style language for complex queries.<br><br>[Full language reference](elasticsearch://reference/query-languages/querydsl.md)| Full-text search, semantic search, keyword search, filtering, aggregations, and more. <br><br>[Query DSL in Kibana](languages/querydsl.md) |[`_search`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) |
| **{{esql}}** | Introduced in **8.11**, the Elasticsearch Query Language ({{esql}}) is a piped query language for filtering, transforming, and analyzing data.<br><br>[Full language reference](elasticsearch://reference/query-languages/esql.md) | You can use {{esql}} in multiple {{kib}} applications for querying, visualizing, and analyzing data.<br><br>[{{esql}} in Kibana](languages/esql-kibana.md) | [`_query`](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-esql) |
| **EQL** | Event Query Language (EQL) is a query language for event-based time series data. Data must contain the `@timestamp` field to use EQL.<br><br>[Full language reference](elasticsearch://reference/query-languages/eql.md) | Designed for the threat hunting security use case.<br><br>[EQL in Kibana](languages/eql.md) | [`_eql`](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-eql) |
| **Elasticsearch SQL** | Allows native, real-time SQL-like querying against {{es}} data. JDBC and ODBC drivers are available for integration with business intelligence (BI) tools.<br><br>[Full language reference](elasticsearch://reference/query-languages/sql.md) | Query {{es}} data using a familiar SQL syntax for BI and reporting.<br><br>[Elasticsearch SQL in Kibana](languages/sql.md) | [`_sql`](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-sql) |
| **Kibana Query Language (KQL)** | {{kib}} Query Language (KQL) is a text-based query language for filtering data when you access it through the {{kib}} UI. | Use KQL to filter documents where a value for a field exists, matches a given value, or is within a given range.<br><br>[KQL in Kibana](languages/kql.md) | N/A |
| **Lucene query syntax** | The original query syntax for {{es}}, based on Apache Lucene. Simple text-based syntax for basic searches and filtering. | Perform basic text searches, simple field queries, and wildcard searches. Useful for quick searches and simple filtering.<br><br>[Lucene syntax in Kibana](languages/lucene-query-syntax.md) | [`_search`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) |