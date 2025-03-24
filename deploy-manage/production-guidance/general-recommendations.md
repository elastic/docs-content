---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/general-recommendations.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
---

# General recommendations [general-recommendations]

This page offers general best practices to improve performance and avoid common issues when working with {{es}}.

## Don’t return large result sets [large-size]

Elasticsearch is designed as a search engine, which makes it very good at getting back the top documents that match a query. However, it is not as good for workloads that fall into the database domain, such as retrieving all documents that match a particular query. If you need to do this, make sure to use the [Scroll](elasticsearch://reference/elasticsearch/rest-apis/paginate-search-results.md#scroll-search-results) API.

## Avoid large documents [maximum-document-size]

Given that the default [`http.max_content_length`](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#http-settings) is set to 100MB, Elasticsearch will refuse to index any document that is larger than that. You might decide to increase that particular setting, but Lucene still has a limit of about 2GB.

Even without considering hard limits, large documents are usually not practical. Large documents put more stress on network, memory usage and disk, even for search requests that do not request the `_source` since Elasticsearch needs to fetch the `_id` of the document in all cases, and the cost of getting this field is bigger for large documents due to how the filesystem cache works. Indexing this document can use an amount of memory that is a multiplier of the original size of the document. Proximity search (phrase queries for instance) and [highlighting](elasticsearch://reference/elasticsearch/rest-apis/highlighting.md) also become more expensive since their cost directly depends on the size of the original document.

It is sometimes useful to reconsider what the unit of information should be. For instance, the fact you want to make books searchable doesn’t necessarily mean that a document should consist of a whole book. It might be a better idea to use chapters or even paragraphs as documents, and then have a property in these documents that identifies which book they belong to. This does not only avoid the issues with large documents, it also makes the search experience better. For instance if a user searches for two words `foo` and `bar`, a match across different chapters is probably very poor, while a match within the same paragraph is likely good.

