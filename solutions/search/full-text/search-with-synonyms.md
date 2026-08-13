---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-with-synonyms.html
description: Learn how to define synonym sets, configure synonym token filters and analyzers, and apply synonyms at search time or index time in Elasticsearch.
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
---

# Set up and search with synonyms in {{es}} [search-with-synonyms]

Synonyms are words or phrases that have the same or similar meaning. When you configure synonyms in {{product.elasticsearch}}, a search for one term automatically matches documents that use an equivalent term. This improves relevance when users express the same concept with different words, makes domain-specific vocabulary more accessible, and handles common misspellings transparently.

This page walks you through defining synonym rules, grouping them into reusable synonym sets, configuring {{product.elasticsearch}} to apply them during text analysis, and verifying that queries return the expanded results you expect.

% TODO: these bundle links do not belong here — migration artifacts kept to avoid broken builds

$$$ece-add-custom-bundle-example-synonyms$$$
$$$ece-add-custom-bundle-example-LDA$$$
$$$ece-add-custom-bundle-example-SAML$$$
$$$ece-add-custom-bundle-example-cacerts$$$
$$$ece-add-custom-bundle-example-LDAP$$$

## Prerequisites

To manage synonym sets using the API or {{kib}} UI, you need the `manage_search_synonyms` [cluster privilege](elasticsearch://reference/elasticsearch/security-privileges.md).

## How synonyms work in {{product.elasticsearch}}

To use synonyms in {{es}}, follow this workflow:

1. [**Create synonym sets and rules**](#synonyms-store-synonyms): Define which terms are equivalent and how to store your synonym sets.
2. [**Configure token filters and analyzers**](#synonyms-synonym-token-filters): Set up synonym token filters and add them to your analyzers.
3. [**Test your analyzer**](#synonyms-test-analyzer): Verify your synonym configuration produces the expected tokens.
4. [**Apply synonyms at index or search time**](#synonyms-apply-synonyms): Specify your analyzer in your index mapping.

## Synonym rule formats

Synonym rules define which terms should be treated as equivalent during search and indexing.

Synonym rules use one of the following formats:

### Explicit mappings

Explicit mappings use `=>` to specify exact replacements:

```
i-pod, i pod => ipod
sea biscuit, sea biscit => seabiscuit
```

With explicit mappings, the relationship is one-way. In the previous examples:
- `i-pod` and `i pod` are replaced with `ipod`, but `ipod` is not replaced with `i-pod` or `i pod`.
- `sea biscuit` and `sea biscit` are replaced with `seabiscuit`, but `seabiscuit` is not replaced with `sea biscuit` or `sea biscit`.

### Equivalent mappings

Equivalent mappings use commas to group interchangeable terms:

```
ipod, i-pod, i pod
foozball, foosball
universe, cosmos
lol, laughing out loud
```

The behavior of equivalent mappings depends on the `expand` parameter in your token filter configuration:
- If `expand=true` (the default): all terms are mapped to each other bidirectionally.
- If `expand=false`: all terms are mapped to the first term only.

For details on how `expand` affects synonym rules, refer to the [synonym graph token filter](elasticsearch://reference/text-analysis/analysis-synonym-graph-tokenfilter.md) reference.

## Step 1: Create synonym sets and rules [synonyms-store-synonyms]

You have multiple options for creating synonym sets and rules.

::::{note}
Synonym sets created through the API or the {{kib}} UI can only be used at search time. For index-time synonyms, use a file-based or inline approach with the [`synonym` token filter](elasticsearch://reference/text-analysis/analysis-synonym-tokenfilter.md).
::::

::::::{tab-set}

:::::{tab-item} {{kib}} UI

You can create and manage synonym sets and synonym rules using the {{kib}} user interface.

To create a synonym set using the UI:

1. Use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to find Synonyms, then select **Synonyms / Synonyms** from the results.
2. Select **Get started**.
3. Enter a name for your synonym set.
4. Add your synonym rules in the editor by adding terms to match against:
   - Add **Equivalent rules** by adding multiple equivalent terms. For example: `ipod, i-pod, i pod`
   - Add **Explicit rules** by adding multiple terms that map to a single term. For example: `i-pod, i pod => ipod`
5. Select **Save** to save your rules.

The UI supports the same synonym rule formats as the file-based approach. Changes made through the UI automatically reload the associated analyzers.

:::::

:::::{tab-item} REST API

$$$synonyms-store-synonyms-api$$$

You can use the [synonyms APIs]({{es-apis}}group/endpoint-synonyms) to manage synonym sets. This is the most flexible approach, as it allows you to dynamically define and modify synonym sets. For examples of how to create or update a synonym set with APIs, refer to the [Create or update synonym set API examples](/solutions/search/full-text/create-update-synonyms-api-example.md) page.

Changes to your synonym sets automatically reload the associated analyzers.

:::::

:::::{tab-item} File-based

$$$synonyms-store-synonyms-file$$$

```{applies_to}
serverless: unavailable
```

You can store your synonym set in a file.

Make sure you upload the synonym set file to all your cluster nodes, in the configuration directory for your {{es}} distribution. If you're using {{ech}}, you can upload synonyms files using [custom bundles](../../../deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md).

An example of a synonym file:

```text
# Blank lines and lines starting with pound are comments.

# Explicit mappings
i-pod, i pod => ipod
sea biscuit, sea biscit => seabiscuit

# Equivalent mappings
ipod, i-pod, i pod
universe, cosmos
```

For the full synonym file format specification, including `expand` behavior and rule merging, refer to the [synonym token filter](elasticsearch://reference/text-analysis/analysis-synonym-tokenfilter.md) reference.

To update an existing synonym set, upload new files to your cluster. Synonym set files must be kept in sync on every cluster node.

When a synonym set is updated, search analyzers that use it need to be refreshed using the [reload search analyzers API]({{es-apis}}operation/operation-indices-reload-search-analyzers).

This manual syncing and reloading makes this approach less flexible than using the synonyms API.

:::::

:::::{tab-item} Inline

$$$synonyms-store-synonyms-inline$$$

You can test your synonyms by adding them directly inline in your token filter definition.

::::{warning}
Inline synonyms are not recommended for production usage. Too many inline synonyms increases cluster size unnecessarily and can lead to performance issues.
::::

:::::

::::::

## Step 2: Configure synonyms token filters and analyzers [synonyms-synonym-token-filters]

Once your synonym sets are created, you can start configuring your token filters and analyzers to use them.

::::{warning}
Synonym sets must exist before they can be added to indices. If an index is created referencing a nonexistent synonym set, the index remains in a partially created and inoperable state. The only way to recover from this scenario is to ensure the synonym set exists then either delete and re-create the index, or close and re-open the index.
::::

{{es}} uses synonyms as part of the [analysis process](../../../manage-data/data-store/text-analysis.md). You can use two types of [token filter](elasticsearch://reference/text-analysis/token-filter-reference.md) to include synonyms:

* [Synonym graph](elasticsearch://reference/text-analysis/analysis-synonym-graph-tokenfilter.md): Recommended for search analyzers. Correctly handles multi-word synonyms. This filter is designed for search-time use only.
* [Synonym](elasticsearch://reference/text-analysis/analysis-synonym-tokenfilter.md): Required for index-time synonyms. Not recommended if you need to use multi-word synonyms.

Refer to each token filter's reference page for configuration details and instructions on adding it to an analyzer.

{applies_to}`{"stack": "ga 9.4", "serverless": "ga"}` When processing synonym rules, {{es}} uses a [circuit breaker](elasticsearch://reference/elasticsearch/configuration-reference/circuit-breaker-settings.md) (a memory safety mechanism) to prevent out-of-memory errors. If the circuit breaker trips because heap usage exceeds 95%, the behavior depends on the `lenient` parameter. The `lenient` parameter defaults to the value of `updateable`. When `updateable` is `true` (recommended for search-time synonyms), {{es}} uses an empty synonym map and logs the event. When `lenient` is `false`, the affected index enters a red state. The threshold is configurable using the [`indices.breaker.total.limit` setting](elasticsearch://reference/elasticsearch/configuration-reference/circuit-breaker-settings.md#parent-circuit-breaker). {applies_to}`serverless: unavailable`

::::{warning}
Invalid synonym rules can cause errors when applying analyzer changes and can prevent an index from being reopened. Refer to the [synonym graph token filter](elasticsearch://reference/text-analysis/analysis-synonym-graph-tokenfilter.md) reference for details.
::::

## Step 3: Test your analyzer [synonyms-test-analyzer]

You can test an analyzer configuration without modifying your index settings. Use the [analyze API]({{es-apis}}operation/operation-indices-analyze) to test your analyzer chain:

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

* **Index time**: {applies_to}`serverless: unavailable` Synonyms are applied when the documents are indexed into {{es}}. This is a less flexible alternative, as changes to your synonyms require [reindexing]({{es-apis}}operation/operation-reindex).
* **Search time**: Synonyms are applied when a search is executed. This is a more flexible approach, which doesn't require reindexing. If token filters are configured with `"updateable": true`, search analyzers can be [reloaded]({{es-apis}}operation/operation-indices-reload-search-analyzers) when you make changes to your synonyms.
  :::{note}
  Synonym sets created using the synonyms API or the UI can only be used at search time.
  :::

You can specify the analyzer that contains your synonym set as a [search time analyzer](../../../manage-data/data-store/text-analysis/specify-an-analyzer.md#specify-search-analyzer) or as an [index time analyzer](../../../manage-data/data-store/text-analysis/specify-an-analyzer.md#specify-index-time-analyzer).

Queries that support synonym expansion include [match](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query.md), [query_string](elasticsearch://reference/query-languages/query-dsl/query-dsl-query-string-query.md), and [simple_query_string](elasticsearch://reference/query-languages/query-dsl/query-dsl-simple-query-string-query.md). These queries support the `auto_generate_synonyms_phrase_query` parameter, which controls how multi-word synonyms are handled at query time.

The following example adds `my_analyzer` as a search analyzer to the `title` field in an index mapping. The filter references a synonym set created through the API or {{kib}} UI.

For [file-based synonym sets](#synonyms-store-synonyms-file), use `synonyms_path` instead of `synonyms_set`. {applies_to}`serverless: unavailable`

```console
PUT /my-index
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
          "tokenizer": "standard",
          "filter": ["lowercase", "synonyms_filter"]
        }
      },
      "filter": {
        "synonyms_filter": {
          "type": "synonym_graph",
          "synonyms_set": "my-synonym-set", <1>
          "updateable": true
        }
      }
    }
  }
}
```

1. For file-based synonym sets, replace with `"synonyms_path": "analysis/synonym-set.txt"`.

## Search with synonyms in action [synonyms-search-example]

After you configure synonyms for a field, queries against that field automatically expand to include synonym terms. For example, if `laptop` and `notebook` are configured as equivalent terms and you search for `laptop`, {{es}} also matches documents containing `notebook`.

```console
GET /my-index/_search
{
  "query": {
    "match": {
      "title": "laptop"
    }
  }
}
```

This query matches documents where the `title` field contains `laptop` or `notebook`, because the synonym rule treats them as equivalent.

## Next steps

* [Create or update synonym set API examples](/solutions/search/full-text/create-update-synonyms-api-example.md): Practical examples of managing synonym sets through the API.
* [Synonym graph token filter](elasticsearch://reference/text-analysis/analysis-synonym-graph-tokenfilter.md): Full reference for the recommended synonym token filter.
* [Synonym token filter](elasticsearch://reference/text-analysis/analysis-synonym-tokenfilter.md): Reference for the standard synonym token filter, required for index-time synonyms.
* [Text analysis](../../../manage-data/data-store/text-analysis.md): Learn more about analyzers, tokenizers, and token filters.
