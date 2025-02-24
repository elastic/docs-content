---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-custom-analyzer.html
applies_to:
  stack: ga
  serverless: ga
---

# Create a custom analyzer [analysis-custom-analyzer]

When the built-in analyzers do not fulfill your needs, you can create a `custom` analyzer which uses the appropriate combination of:

* zero or more [character filters](asciidocalypse://docs/elasticsearch/docs/reference/data-analysis/text-analysis/character-filter-reference.md)
* a [tokenizer](asciidocalypse://docs/elasticsearch/docs/reference/data-analysis/text-analysis/tokenizer-reference.md)
* zero or more [token filters](asciidocalypse://docs/elasticsearch/docs/reference/data-analysis/text-analysis/token-filter-reference.md).


## Configuration [_configuration] 

The `custom` analyzer accepts the following parameters:

`type`
:   Analyzer type. Accepts [built-in analyzer types](asciidocalypse://docs/elasticsearch/docs/reference/data-analysis/text-analysis/analyzer-reference.md). For custom analyzers, use `custom` or omit this parameter.

`tokenizer`
:   A built-in or customised [tokenizer](asciidocalypse://docs/elasticsearch/docs/reference/data-analysis/text-analysis/tokenizer-reference.md). (Required)

`char_filter`
:   An optional array of built-in or customised [character filters](asciidocalypse://docs/elasticsearch/docs/reference/data-analysis/text-analysis/character-filter-reference.md).

`filter`
:   An optional array of built-in or customised [token filters](asciidocalypse://docs/elasticsearch/docs/reference/data-analysis/text-analysis/token-filter-reference.md).

`position_increment_gap`
:   When indexing an array of text values, Elasticsearch inserts a fake "gap" between the last term of one value and the first term of the next value to ensure that a phrase query doesn’t match two terms from different array elements. Defaults to `100`. See [`position_increment_gap`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/position-increment-gap.md) for more.


## Example configuration [_example_configuration] 

Here is an example that combines the following:

Character Filter
:   * [HTML Strip Character Filter](asciidocalypse://docs/elasticsearch/docs/reference/data-analysis/text-analysis/analysis-htmlstrip-charfilter.md)


Tokenizer
:   * [Standard Tokenizer](asciidocalypse://docs/elasticsearch/docs/reference/data-analysis/text-analysis/analysis-standard-tokenizer.md)


Token Filters
:   * [Lowercase Token Filter](asciidocalypse://docs/elasticsearch/docs/reference/data-analysis/text-analysis/analysis-lowercase-tokenfilter.md)
* [ASCII-Folding Token Filter](asciidocalypse://docs/elasticsearch/docs/reference/data-analysis/text-analysis/analysis-asciifolding-tokenfilter.md)


```console
PUT my-index-000001
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_custom_analyzer": {
          "type": "custom", <1>
          "tokenizer": "standard",
          "char_filter": [
            "html_strip"
          ],
          "filter": [
            "lowercase",
            "asciifolding"
          ]
        }
      }
    }
  }
}

POST my-index-000001/_analyze
{
  "analyzer": "my_custom_analyzer",
  "text": "Is this <b>déjà vu</b>?"
}
```

1. For `custom` analyzers, use a `type` of `custom` or omit the `type` parameter.


The above example produces the following terms:

```text
[ is, this, deja, vu ]
```

The previous example used tokenizer, token filters, and character filters with their default configurations, but it is possible to create configured versions of each and to use them in a custom analyzer.

Here is a more complicated example that combines the following:

Character Filter
:   * [Mapping Character Filter](asciidocalypse://docs/elasticsearch/docs/reference/data-analysis/text-analysis/analysis-mapping-charfilter.md), configured to replace `:)` with `_happy_` and `:(` with `_sad_`


Tokenizer
:   * [Pattern Tokenizer](asciidocalypse://docs/elasticsearch/docs/reference/data-analysis/text-analysis/analysis-pattern-tokenizer.md), configured to split on punctuation characters


Token Filters
:   * [Lowercase Token Filter](asciidocalypse://docs/elasticsearch/docs/reference/data-analysis/text-analysis/analysis-lowercase-tokenfilter.md)
* [Stop Token Filter](asciidocalypse://docs/elasticsearch/docs/reference/data-analysis/text-analysis/analysis-stop-tokenfilter.md), configured to use the pre-defined list of English stop words


Here is an example:

```console
PUT my-index-000001
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_custom_analyzer": { <1>
          "char_filter": [
            "emoticons"
          ],
          "tokenizer": "punctuation",
          "filter": [
            "lowercase",
            "english_stop"
          ]
        }
      },
      "tokenizer": {
        "punctuation": { <2>
          "type": "pattern",
          "pattern": "[ .,!?]"
        }
      },
      "char_filter": {
        "emoticons": { <3>
          "type": "mapping",
          "mappings": [
            ":) => _happy_",
            ":( => _sad_"
          ]
        }
      },
      "filter": {
        "english_stop": { <4>
          "type": "stop",
          "stopwords": "_english_"
        }
      }
    }
  }
}

POST my-index-000001/_analyze
{
  "analyzer": "my_custom_analyzer",
  "text": "I'm a :) person, and you?"
}
```

1. Assigns the index a default custom analyzer, `my_custom_analyzer`. This analyzer uses a custom tokenizer, character filter, and token filter that are defined later in the request. This analyzer also omits the `type` parameter.
2. Defines the custom `punctuation` tokenizer.
3. Defines the custom `emoticons` character filter.
4. Defines the custom `english_stop` token filter.


The above example produces the following terms:

```text
[ i'm, _happy_, person, you ]
```

