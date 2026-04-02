---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-index-search-time.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Index and search analysis [analysis-index-search-time]

Text analysis occurs at two times:

Index time
:   When a document is indexed, any [`text`](elasticsearch://reference/elasticsearch/mapping-reference/text.md) field values are analyzed.

Search time
:   When running a [full-text search](elasticsearch://reference/query-languages/query-dsl/full-text-queries.md) on a `text` field, the query string (the text the user is searching for) is analyzed. Search time is also called *query time*.

    For more details on text analysis at search time, refer to [Text analysis during search](/solutions/search/full-text/text-analysis-during-search.md).

The analyzer, or set of analysis rules, used at each time is called the *index analyzer* or *search analyzer* respectively.

## How the index and search analyzer work together [analysis-same-index-search-analyzer]

In most cases, the same analyzer should be used at index and search time. This ensures the values and query strings for a field are changed into the same form of tokens. In turn, this ensures the tokens match as expected during a search.

::::{dropdown} Example
A document is indexed with the following value in a `text` field:

```text
The QUICK brown foxes jumped over the dog!
```

The index analyzer for the field converts the value into tokens and normalizes them. In this case, each of the tokens represents a word:

```text
[ quick, brown, fox, jump, over, dog ]
```

These tokens are then indexed.

Later, a user searches the same `text` field for:

```text
"Quick fox"
```

The user expects this search to match the sentence indexed earlier, `The QUICK brown foxes jumped over the dog!`.

However, the query string does not contain the exact words used in the document's original text:

* `Quick` versus `QUICK`
* `fox` versus `foxes`

To account for this, the query string is analyzed using the same analyzer. This analyzer produces the following tokens:

```text
[ quick, fox ]
```

To execute the search, {{es}} compares these query string tokens to the tokens indexed in the `text` field.

| Token | Query string | `text` field |
| --- | --- | --- |
| `quick` | X | X |
| `brown` |  | X |
| `fox` | X | X |
| `jump` |  | X |
| `over` |  | X |
| `dog` |  | X |

Because the field value and query string were analyzed in the same way, they created similar tokens. The tokens `quick` and `fox` are exact matches. This means the search matches the document containing `"The QUICK brown foxes jumped over the dog!"`, just as the user expects.

::::



## When to use a different search analyzer [different-analyzers]

While less common, it sometimes makes sense to use different analyzers at index and search time. To enable this, {{es}} allows you to [specify a separate search analyzer](specify-an-analyzer.md#specify-search-analyzer).

Generally, a separate search analyzer should only be specified when using the same form of tokens for field values and query strings would create unexpected or irrelevant search matches.

::::{dropdown} Example
:name: different-analyzer-ex

{{es}} is used to create a search engine that matches only words that start with a provided prefix. For instance, a search for `tr` should return `tram` or `trope`—but never `taxi` or `bat`.

A document is added to the search engine’s index; this document contains one such word in a `text` field:

```text
"Apple"
```

The index analyzer for the field converts the value into tokens and normalizes them. In this case, each of the tokens represents a potential prefix for the word:

```text
[ a, ap, app, appl, apple]
```

These tokens are then indexed.

Later, a user searches the same `text` field for:

```text
"appli"
```

The user expects this search to match only words that start with `appli`, such as `appliance` or `application`. The search should not match `apple`.

However, if the index analyzer is used to analyze this query string, it would produce the following tokens:

```text
[ a, ap, app, appl, appli ]
```

When {{es}} compares these query string tokens to the ones indexed for `apple`, it finds several matches.

| Token | `appli` | `apple` |
| --- | --- | --- |
| `a` | X | X |
| `ap` | X | X |
| `app` | X | X |
| `appl` | X | X |
| `appli` |  | X |

This means the search would erroneously match `apple`. Not only that, it would match any word starting with `a`.

To fix this, you can specify a different search analyzer for query strings used on the `text` field.

In this case, you could specify a search analyzer that produces a single token rather than a set of prefixes:

```text
[ appli ]
```

This query string token would only match tokens for words that start with `appli`, which better aligns with the user’s search expectations.

::::
