# Query DSL [query-dsl]

Elasticsearch provides a full Query DSL (Domain Specific Language) based on JSON to define queries. Think of the Query DSL as an AST (Abstract Syntax Tree) of queries, consisting of two types of clauses:

Leaf query clauses
:   Leaf query clauses look for a particular value in a particular field, such as the [`match`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html), [`term`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html) or [`range`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-range-query.html) queries. These queries can be used by themselves.

Compound query clauses
:   Compound query clauses wrap other leaf **or** compound queries and are used to combine multiple queries in a logical fashion (such as the [`bool`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html) or [`dis_max`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-dis-max-query.html) query), or to alter their behaviour (such as the [`constant_score`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-constant-score-query.html) query).

Query clauses behave differently depending on whether they are used in [query context or filter context](../../../explore-analyze/query-filter/languages/querydsl.md).

$$$query-dsl-allow-expensive-queries$$$

Allow expensive queries
:   Certain types of queries will generally execute slowly due to the way they are implemented, which can affect the stability of the cluster. Those queries can be categorised as follows:

    * Queries that need to do linear scans to identify matches:

        * [`script` queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-script-query.html)
        * queries on [numeric](https://www.elastic.co/guide/en/elasticsearch/reference/current/number.html), [date](https://www.elastic.co/guide/en/elasticsearch/reference/current/date.html), [boolean](https://www.elastic.co/guide/en/elasticsearch/reference/current/boolean.html), [ip](https://www.elastic.co/guide/en/elasticsearch/reference/current/ip.html), [geo_point](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-point.html) or [keyword](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html) fields that are not indexed but have [doc values](https://www.elastic.co/guide/en/elasticsearch/reference/current/doc-values.html) enabled

    * Queries that have a high up-front cost:

        * [`fuzzy` queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-fuzzy-query.html) (except on [`wildcard`](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html#wildcard-field-type) fields)
        * [`regexp` queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-regexp-query.html) (except on [`wildcard`](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html#wildcard-field-type) fields)
        * [`prefix` queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-prefix-query.html)  (except on [`wildcard`](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html#wildcard-field-type) fields or those without [`index_prefixes`](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-prefixes.html))
        * [`wildcard` queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-wildcard-query.html) (except on [`wildcard`](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html#wildcard-field-type) fields)
        * [`range` queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-range-query.html) on [`text`](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html) and [`keyword`](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html) fields

    * [Joining queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/joining-queries.html)
    * Queries that may have a high per-document cost:

        * [`script_score` queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-script-score-query.html)
        * [`percolate` queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-percolate-query.html)


The execution of such queries can be prevented by setting the value of the `search.allow_expensive_queries` setting to `false` (defaults to `true`).

