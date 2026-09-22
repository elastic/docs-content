---
navigation_title: Synonyms
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-with-synonyms.html
description: Learn how to define synonym sets, configure synonym token filters and analyzers, and apply synonyms at search time or index time in Elasticsearch.
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
---

# Configure synonyms in {{es}} [search-with-synonyms]

Synonyms are words or phrases that have the same or similar meaning. When you configure synonyms in {{product.elasticsearch}}, a search for one term automatically matches documents that use an equivalent term. For example, you can define synonym rules to match different terms for the same concept, surface results for domain-specific jargon, or handle common misspellings.

This page walks you through defining synonym rules, grouping them into reusable synonym sets, configuring {{product.elasticsearch}} to apply them during text analysis, and verifying that queries return the expanded results you expect.

% TODO: these bundle links do not belong here — migration artifacts kept to avoid broken builds

$$$ece-add-custom-bundle-example-synonyms$$$
$$$ece-add-custom-bundle-example-LDA$$$
$$$ece-add-custom-bundle-example-SAML$$$
$$$ece-add-custom-bundle-example-cacerts$$$
$$$ece-add-custom-bundle-example-LDAP$$$

## Prerequisites

To manage synonym sets using the API or {{kib}} UI, you need the `manage_search_synonyms` [cluster privilege](elasticsearch://reference/elasticsearch/security-privileges.md).

## Synonyms workflow overview

To use synonyms in {{es}}, follow this workflow:

1. [**Create synonym sets and rules**](#synonyms-store-synonyms): Define which terms are equivalent and how to store your synonym sets.
2. [**Configure token filters and analyzers**](#synonyms-synonym-token-filters): Set up synonym token filters and add them to your analyzers.
3. [**Create an index with your synonym analyzer**](#synonyms-apply-synonyms): Apply your analyzer to an index mapping.
4. [**Test your analyzer**](#synonyms-test-analyzer): Verify your synonym configuration produces the expected tokens.
5. [**Search with synonyms**](#synonyms-search-example): Run a search query and confirm synonym expansion works.

## Synonym rule formats

Synonym rules define which terms should be treated as equivalent. Each rule uses one of two mapping types:

- **Explicit mappings** use `=>` to specify one-way replacements (for example, `i-pod, i pod => ipod`).
- **Equivalent mappings** use commas to group interchangeable terms (for example, `ipod, i-pod, i pod`).

For full format details, refer to the [synonym graph token filter](elasticsearch://reference/text-analysis/analysis-synonym-graph-tokenfilter.md) reference.

## Step 1: Create synonym sets and rules [synonyms-store-synonyms]

You have multiple options for creating synonym sets and rules.

Synonym sets created through the API or the {{kib}} UI can only be used at search time. For index-time synonyms, use a file-based or inline approach with the [`synonym` token filter](elasticsearch://reference/text-analysis/analysis-synonym-tokenfilter.md).

::::::{tab-set}

:::::{tab-item} REST API

$$$synonyms-store-synonyms-api$$$

You can use the [synonyms APIs]({{es-apis}}group/endpoint-synonyms) to manage synonym sets. This is the most flexible approach, as it allows you to dynamically define and modify synonym sets.
The following example creates a synonym set named `my-synonym-set`. Later steps on this page use this set.

```console
PUT _synonyms/my-synonym-set
{
  "synonyms_set": [
    {
      "id": "laptop-synonyms",
      "synonyms": "laptop, notebook"
    }
  ]
}
```

Changes to your synonym sets automatically reload the associated analyzers. For more examples, including rule validation and analyzer reloading, refer to [Create or update synonym set API examples](/solutions/search/full-text/create-update-synonyms-api-example.md).

:::::

:::::{tab-item} {{kib}} UI

$$$synonyms-store-synonyms-kibana$$$

```{applies_to}
stack: ga
serverless:
  elasticsearch:
```

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

You can define synonyms directly in your token filter using the `synonyms` parameter. This is useful for testing, but not recommended for production.

```json
"synonyms_filter": {
  "type": "synonym_graph",
  "synonyms": ["laptop, notebook", "i-pod, i pod => ipod"]
}
```

::::{warning}
A large number of inline synonyms increases cluster size unnecessarily and can lead to performance issues. For production workloads, use the REST API or file-based approach instead.
::::

:::::

::::::

::::{warning}
Synonym sets must exist before you reference them in an index. An index that references a nonexistent synonym set becomes inoperable and must be deleted and re-created, or closed and re-opened.
::::

## Step 2: Configure synonym token filters and analyzers [synonyms-synonym-token-filters]

Once your synonym sets are created, you can start configuring your token filters and analyzers to use them.

{{es}} uses synonyms as part of the [analysis process](../../../manage-data/data-store/text-analysis.md). You can use two types of [token filter](elasticsearch://reference/text-analysis/token-filter-reference.md) to include synonyms:

* [Synonym graph](elasticsearch://reference/text-analysis/analysis-synonym-graph-tokenfilter.md): Recommended for search analyzers. Correctly handles multi-word synonyms. This filter is designed for search-time use only.
* [Synonym](elasticsearch://reference/text-analysis/analysis-synonym-tokenfilter.md): Required for index-time synonyms. Not recommended if you need to use multi-word synonyms.

Refer to each token filter's reference page for configuration details and instructions on adding it to an analyzer. If your analyzer chain includes a [stop token filter](elasticsearch://reference/text-analysis/analysis-synonym-graph-tokenfilter.md#synonym-graph-tokenizer-stop-token-filter), pay attention to ordering. Stop filters placed before or after a synonym filter affect synonym expansion differently.

{applies_to}`stack: ga 9.4` {applies_to}`serverless: ga` Large synonym sets can trigger a memory [circuit breaker](elasticsearch://reference/text-analysis/analysis-synonym-graph-tokenfilter.md#synonym-graph-tokenizer-circuit-breaker). Refer to the [synonym graph token filter](elasticsearch://reference/text-analysis/analysis-synonym-graph-tokenfilter.md#synonym-graph-tokenizer-circuit-breaker) reference for thresholds and `lenient` behavior.

::::{important}
When `lenient` is `false`, invalid synonym rules cause errors: analyzer changes fail to apply, and an index with invalid rules cannot be reopened. `lenient` defaults to the value of `updateable`. Refer to [Synonyms and `stop` token filters](elasticsearch://reference/text-analysis/analysis-synonym-graph-tokenfilter.md#synonym-graph-tokenizer-stop-token-filter) for details.
::::

## Step 3: Create an index with your synonym analyzer [synonyms-apply-synonyms]

Synonyms can be applied at [search time or index time](../../../manage-data/data-store/text-analysis/index-search-analysis.md). Search time is recommended because you can update your synonym sets without [reindexing]({{es-apis}}operation/operation-reindex). If token filters are configured with `"updateable": true`, search analyzers can be [reloaded]({{es-apis}}operation/operation-indices-reload-search-analyzers) when you make changes.

The following example creates an index with `synonyms_analyzer` as a search analyzer on the `title` field.

```console
PUT /my-index
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "search_analyzer": "synonyms_analyzer" <2>
      }
    }
  },
  "settings": {
    "analysis": {
      "analyzer": {
        "synonyms_analyzer": {
          "tokenizer": "standard",
          "filter": ["lowercase", "synonyms_filter"]
        }
      },
      "filter": {
        "synonyms_filter": {
          "type": "synonym_graph",
          "synonyms_set": "my-synonym-set", <1>
          "updateable": true <3>
        }
      }
    }
  }
}
```

1. For [file-based synonym sets](#synonyms-store-synonyms-file), use `"synonyms_path": "analysis/synonym-set.txt"` instead. {applies_to}`serverless: unavailable`
2. Applies synonyms at search time only, not when indexing documents.
3. Required when you use `synonyms_set`: synonym sets can only be loaded into search-time analyzers. It also lets you [reload]({{es-apis}}operation/operation-indices-reload-search-analyzers) the analyzer when the set changes, without reindexing.

## Step 4: Test your analyzer [synonyms-test-analyzer]

After creating your index, use the [analyze API]({{es-apis}}operation/operation-indices-analyze) to verify that your synonym configuration produces the expected tokens:

```console
GET /my-index/_analyze
{
  "analyzer": "synonyms_analyzer",
  "text": "laptop"
}
```

The response contains tokens for both `laptop` and `notebook`, because `my-synonym-set` defines them as equivalent terms.

## Step 5: Search with synonyms [synonyms-search-example]

After you configure synonyms for a field, queries against that field automatically expand to include synonym terms. Queries that support synonym expansion include [match](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-query.md), [query_string](elasticsearch://reference/query-languages/query-dsl/query-dsl-query-string-query.md), and [simple_query_string](elasticsearch://reference/query-languages/query-dsl/query-dsl-simple-query-string-query.md).

Index a document so the search has something to match:

```console
POST /my-index/_doc?refresh=true
{
  "title": "Lightweight notebook for travel"
}
```

For example, if `laptop` and `notebook` are configured as equivalent terms and you search for `laptop`, {{es}} also matches documents containing `notebook`:

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

The response includes the document, even though its `title` doesn't contain the word `laptop`: `synonyms_analyzer` expanded the query term to `notebook` at search time.

## Next steps

* [Create or update synonym set API examples](/solutions/search/full-text/create-update-synonyms-api-example.md): Practical examples of managing synonym sets through the API.
* [Synonym graph token filter](elasticsearch://reference/text-analysis/analysis-synonym-graph-tokenfilter.md): Full reference for the recommended synonym token filter.
* [Synonym token filter](elasticsearch://reference/text-analysis/analysis-synonym-tokenfilter.md): Reference for the standard synonym token filter, required for index-time synonyms.
* [Text analysis](../../../manage-data/data-store/text-analysis.md): Learn more about analyzers, tokenizers, and token filters.
