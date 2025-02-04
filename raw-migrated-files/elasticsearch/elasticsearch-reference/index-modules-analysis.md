# Analysis [index-modules-analysis]

The index analysis module acts as a configurable registry of *analyzers* that can be used in order to convert a string field into individual terms which are:

* added to the inverted index in order to make the document searchable
* used by high level queries such as the [`match` query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-match-query.html) to generate search terms.

See [Text analysis](../../../solutions/search/full-text/text-analysis-during-search.md) for configuration details.

