# Search with synonyms [search-with-synonyms]

Synonyms are words or phrases that have the same or similar meaning. They are an important aspect of search, as they can improve the search experience and increase the scope of search results.

Synonyms allow you to:

* **Improve search relevance** by finding relevant documents that use different terms to express the same concept.
* Make **domain-specific vocabulary** more user-friendly, allowing users to use search terms they are more familiar with.
* **Define common misspellings and typos** to transparently handle common mistakes.

Synonyms are grouped together using **synonyms sets**. You can have as many synonyms sets as you need.

In order to use synonyms sets in {{es}}, you need to:

* [Store your synonyms set](../../../solutions/search/full-text/search-with-synonyms.md#synonyms-store-synonyms)
* [Configure synonyms token filters and analyzers](../../../solutions/search/full-text/search-with-synonyms.md#synonyms-synonym-token-filters)


## Store your synonyms set [synonyms-store-synonyms]

Your synonyms sets need to be stored in {{es}} so your analyzers can refer to them. There are three ways to store your synonyms sets:


### Synonyms API [synonyms-store-synonyms-api]

You can use the [synonyms APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-synonyms) to manage synonyms sets. This is the most flexible approach, as it allows to dynamically define and modify synonyms sets.

Changes in your synonyms sets will automatically reload the associated analyzers.


### Synonyms File [synonyms-store-synonyms-file]

You can store your synonyms set in a file.

A synonyms set file needs to be uploaded to all your cluster nodes, and be located in the configuration directory for your {{es}} distribution. If you’re using {{ecloud}}, you can upload synonyms files using [custom bundles](../../../deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md).

An example synonyms file:

```markdown
# Blank lines and lines starting with pound are comments.

# Explicit mappings match any token sequence on the left hand side of "=>"
# and replace with all alternatives on the right hand side.
# These types of mappings ignore the expand parameter in the schema.
# Examples:
i-pod, i pod => ipod
sea biscuit, sea biscit => seabiscuit

# Equivalent synonyms may be separated with commas and give
# no explicit mapping.  In this case the mapping behavior will
# be taken from the expand parameter in the token filter configuration.
# This allows the same synonym file to be used in different synonym handling strategies.
# Examples:
ipod, i-pod, i pod
foozball , foosball
universe , cosmos
lol, laughing out loud

# If expand==true in the synonym token filter configuration,
# "ipod, i-pod, i pod" is equivalent to the explicit mapping:
ipod, i-pod, i pod => ipod, i-pod, i pod
# If expand==false, "ipod, i-pod, i pod" is equivalent
# to the explicit mapping:
ipod, i-pod, i pod => ipod

# Multiple synonym mapping entries are merged.
foo => foo bar
foo => baz
# is equivalent to
foo => foo bar, baz
```

To update an existing synonyms set, upload new files to your cluster. Synonyms set files must be kept in sync on every cluster node.

When a synonyms set is updated, search analyzers that use it need to be refreshed using the [reload search analyzers API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-reload-search-analyzers)

This manual syncing and reloading makes this approach less flexible than using the [synonyms API](../../../solutions/search/full-text/search-with-synonyms.md#synonyms-store-synonyms-api).


### Inline [synonyms-store-synonyms-inline]

You can test your synonyms by adding them directly inline in your token filter definition.

::::{warning}
Inline synonyms are not recommended for production usage. A large number of inline synonyms increases cluster size unnecessarily and can lead to performance issues.

::::



### Configure synonyms token filters and analyzers [synonyms-synonym-token-filters]

Once your synonyms sets are created, you can start configuring your token filters and analyzers to use them.

::::{warning}
Synonyms sets must exist before they can be added to indices. If an index is created referencing a nonexistent synonyms set, the index will remain in a partially created and inoperable state. The only way to recover from this scenario is to ensure the synonyms set exists then either delete and re-create the index, or close and re-open the index.

::::


::::{warning}
Invalid synonym rules can cause errors when applying analyzer changes. For reloadable analyzers, this prevents reloading and applying changes. You must correct errors in the synonym rules and reload the analyzer.

An index with invalid synonym rules cannot be reopened, making it inoperable when:

* A node containing the index starts
* The index is opened from a closed state
* A node restart occurs (which reopens the node assigned shards)

::::


{{es}} uses synonyms as part of the [analysis process](../../../manage-data/data-store/text-analysis.md). You can use two types of [token filter](asciidocalypse://docs/elasticsearch/docs/reference/data-analysis/text-analysis/token-filter-reference.md) to include synonyms:

* [Synonym graph](asciidocalypse://docs/elasticsearch/docs/reference/data-analysis/text-analysis/analysis-synonym-graph-tokenfilter.md): It is recommended to use it, as it can correctly handle multi-word synonyms ("hurriedly", "in a hurry").
* [Synonym](asciidocalypse://docs/elasticsearch/docs/reference/data-analysis/text-analysis/analysis-synonym-tokenfilter.md): Not recommended if you need to use multi-word synonyms.

Check each synonym token filter documentation for configuration details and instructions on adding it to an analyzer.


### Test your analyzer [synonyms-test-analyzer]

You can test an analyzer configuration without modifying your index settings. Use the [analyze API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-analyze) to test your analyzer chain:

```console
GET /_analyze
{
  "tokenizer": "standard",
  "filter" : [
    "lowercase",
    {
      "type": "synonym_graph",
      "synonyms": ["pc => personal computer", "computer, pc, laptop"]
    }
  ],
  "text" : "Check how PC synonyms work"
}
```


### Apply synonyms at index or search time [synonyms-apply-synonyms]

Analyzers can be applied at [index time or search time](../../../manage-data/data-store/text-analysis/index-search-analysis.md).

You need to decide when to apply your synonyms:

* Index time: Synonyms are applied when the documents are indexed into {{es}}. This is a less flexible alternative, as changes to your synonyms require [reindexing](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex).
* Search time: Synonyms are applied when a search is executed. This is a more flexible approach, which doesn’t require reindexing. If token filters are configured with `"updateable": true`, search analyzers can be [reloaded](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-reload-search-analyzers) when you make changes to your synonyms.

Synonyms sets created using the [synonyms API](../../../solutions/search/full-text/search-with-synonyms.md#synonyms-store-synonyms-api) can only be used at search time.

You can specify the analyzer that contains your synonyms set as a [search time analyzer](../../../manage-data/data-store/text-analysis/specify-an-analyzer.md#specify-search-analyzer) or as an [index time analyzer](../../../manage-data/data-store/text-analysis/specify-an-analyzer.md#specify-index-time-analyzer).

The following example adds `my_analyzer` as a search analyzer to the `title` field in an index mapping:

```JSON
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "search_analyzer": "my_analyzer"
      }
    }
  },
  "settings": {
    "analysis": {
      "analyzer": {
        "my_analyzer": {
          "tokenizer": "whitespace",
          "filter": [
            "synonyms_filter"
          ]
        }
      },
      "filter": {
        "synonyms_filter": {
          "type": "synonym",
          "synonyms_path": "analysis/synonym-set.txt",
          "updateable": true
        }
      }
    }
  }
}
```
