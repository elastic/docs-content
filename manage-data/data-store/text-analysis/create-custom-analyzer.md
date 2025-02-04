---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-custom-analyzer.html
---

# Create a custom analyzer [analysis-custom-analyzer]

When the built-in analyzers do not fulfill your needs, you can create a `custom` analyzer which uses the appropriate combination of:

* zero or more [character filters](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-charfilters.html)
* a [tokenizer](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenizers.html)
* zero or more [token filters](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenfilters.html).


## Configuration [_configuration] 

The `custom` analyzer accepts the following parameters:

`type`
:   Analyzer type. Accepts [built-in analyzer types](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-analyzers.html). For custom analyzers, use `custom` or omit this parameter.

`tokenizer`
:   A built-in or customised [tokenizer](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenizers.html). (Required)

`char_filter`
:   An optional array of built-in or customised [character filters](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-charfilters.html).

`filter`
:   An optional array of built-in or customised [token filters](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-tokenfilters.html).

`position_increment_gap`
:   When indexing an array of text values, Elasticsearch inserts a fake "gap" between the last term of one value and the first term of the next value to ensure that a phrase query doesn’t match two terms from different array elements. Defaults to `100`. See [`position_increment_gap`](https://www.elastic.co/guide/en/elasticsearch/reference/current/position-increment-gap.html) for more.


## Example configuration [_example_configuration] 

Here is an example that combines the following:

Character Filter
:   * [HTML Strip Character Filter](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-htmlstrip-charfilter.html)


Tokenizer
:   * [Standard Tokenizer](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-standard-tokenizer.html)


Token Filters
:   * [Lowercase Token Filter](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-lowercase-tokenfilter.html)
* [ASCII-Folding Token Filter](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-asciifolding-tokenfilter.html)


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
:   * [Mapping Character Filter](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-mapping-charfilter.html), configured to replace `:)` with `_happy_` and `:(` with `_sad_`


Tokenizer
:   * [Pattern Tokenizer](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-pattern-tokenizer.html), configured to split on punctuation characters


Token Filters
:   * [Lowercase Token Filter](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-lowercase-tokenfilter.html)
* [Stop Token Filter](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-stop-tokenfilter.html), configured to use the pre-defined list of English stop words


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

