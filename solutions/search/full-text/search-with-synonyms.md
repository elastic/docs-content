---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-with-synonyms.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
---

# Search with synonyms [search-with-synonyms]

$$$ece-add-custom-bundle-example-synonyms$$$
::::{note}
Learn about [adding custom synonym bundles](/solutions/search/full-text/search-with-synonyms.md#ece-add-custom-bundle-example-synonyms) to your {{ece}} deployment.
::::

% TODO: these bundle links do not belong here

$$$ece-add-custom-bundle-example-LDA$$$

$$$ece-add-custom-bundle-example-SAML$$$

$$$ece-add-custom-bundle-example-cacerts$$$

$$$ece-add-custom-bundle-example-LDAP$$$

Synonyms are words or phrases that have the same or similar meaning. They are an important aspect of search, as they can improve the search experience and increase the scope of search results.

Synonyms allow you to:

* **Improve search relevance** by finding relevant documents that use different terms to express the same concept.
* Make **domain-specific vocabulary** more user-friendly, allowing users to use search terms they are more familiar with.
* **Define common misspellings and typos** to transparently handle common mistakes.

Synonyms are grouped together using **synonyms sets**. You can have as many synonyms sets as you need.

## How synonyms work in Elasticsearch

To use synonyms in {{es}}, you need to follow this workflow:

1. **Create synonym sets and rules** - Define which terms are equivalent and where to store your synonym sets
2. **Configure analyzers** - Apply synonyms during text analysis
3. **Test and apply** - Verify your configuration works correctly

## Step 1: Create synonym sets and rules

You can create synonym sets and rules using several methods:

### Synonym rule formats

Before creating synonym sets, you need to understand how to write synonym rules. Synonym rules define which terms should be treated as equivalent during search and indexing.

There are two main formats for synonym rules:

**Explicit mappings** use `=>` to specify exact replacements:
```
i-pod, i pod => ipod
sea biscuit, sea biscit => seabiscuit
```

**Equivalent synonyms** use commas to group interchangeable terms:
```
ipod, i-pod, i pod
foozball, foosball
universe, cosmos
lol, laughing out loud
```

The behavior of equivalent synonyms depends on the `expand` parameter in your token filter configuration:
- If `expand=true`: `ipod, i-pod, i pod` expands to `ipod, i-pod, i pod`
- If `expand=false`: `ipod, i-pod, i pod` maps to just `ipod`

### Method 1: Kibana UI

```yaml {applies_to}
serverless: 
  elasticsearch:
```

You can create and manage synonym sets and synonym rules using the Kibana user interface. This provides a user-friendly way to manage synonyms without using APIs or file uploads.

To create a synonym set using the UI:

1. Navigate to **Elasticsearch** > **Synonyms** or use the [global search field](docs-content://explore-analyze/query-filter/filtering.md#_finding_your_apps_and_objects)
2. Click **Get started**
3. Enter a name for your synonym set
4. Add your synonym rules in the editor using the formats above:
   - Explicit mappings: `i-pod, i pod => ipod`
   - Equivalent synonyms: `ipod, i-pod, i pod`
5. Click **Create** to save your synonym set

The UI supports the same synonym rule formats as the file-based approach. Changes made through the UI will automatically reload the associated analyzers.

### Method 2: REST API

You can use the [synonyms APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-synonyms) to manage synonyms sets. This is the most flexible approach, as it allows to dynamically define and modify synonyms sets. For examples of how to 
create or update a synonym set with APIs, refer to the [Create or update synonyms set API examples](/solutions/search/full-text/search-with-synonyms.md) page.

Changes in your synonyms sets will automatically reload the associated analyzers.

### Method 3: File-based

You can store your synonyms set in a file.

A synonyms set file needs to be uploaded to all your cluster nodes, and be located in the configuration directory for your {{es}} distribution. If you're using {{ech}}, you can upload synonyms files using [custom bundles](../../../deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md).

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

### Method 4: Inline

You can test your synonyms by adding them directly inline in your token filter definition.

::::{warning}
Inline synonyms are not recommended for production usage. A large number of inline synonyms increases cluster size unnecessarily and can lead to performance issues.
::::

## Step 2: Configure synonyms token filters and analyzers [synonyms-synonym-token-filters]

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

{{es}} uses synonyms as part of the [analysis process](../../../manage-data/data-store/text-analysis.md). You can use two types of [token filter](elasticsearch://reference/text-analysis/token-filter-reference.md) to include synonyms:

* [Synonym graph](elasticsearch://reference/text-analysis/analysis-synonym-graph-tokenfilter.md): It is recommended to use it, as it can correctly handle multi-word synonyms ("hurriedly", "in a hurry").
* [Synonym](elasticsearch://reference/text-analysis/analysis-synonym-tokenfilter.md): Not recommended if you need to use multi-word synonyms.

Check each synonym token filter documentation for configuration details and instructions on adding it to an analyzer.

## Step 3: Test your analyzer [synonyms-test-analyzer]

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

## Step 4: Apply synonyms at index or search time [synonyms-apply-synonyms]

Analyzers can be applied at [index time or search time](../../../manage-data/data-store/text-analysis/index-search-analysis.md).

You need to decide when to apply your synonyms:

* **Index time**: Synonyms are applied when the documents are indexed into {{es}}. This is a less flexible alternative, as changes to your synonyms require [reindexing](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex).
* **Search time**: Synonyms are applied when a search is executed. This is a more flexible approach, which doesn't require reindexing. If token filters are configured with `"updateable": true`, search analyzers can be [reloaded](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-reload-search-analyzers) when you make changes to your synonyms.
  :::{note}
  Synonyms sets created using the synonyms API or the UI can only be used at search time.
  :::

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
