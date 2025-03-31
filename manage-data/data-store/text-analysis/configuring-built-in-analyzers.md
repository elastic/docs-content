---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/configuring-analyzers.html
applies_to:
  stack: ga
  serverless: ga
---

# Configuring built-in analyzers [configuring-analyzers]

The built-in analyzers can be used directly without any configuration. Some of them, however, support configuration options to alter their behaviour. For instance, the [`standard` analyzer](elasticsearch://reference/text-analysis/analysis-standard-analyzer.md) can be configured to support a list of stop words:

```console
PUT my-index-000001
{
  "settings": {
    "analysis": {
      "analyzer": {
        "std_english": { <1>
          "type":      "standard",
          "stopwords": "_english_"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "my_text": {
        "type":     "text",
        "analyzer": "standard", <2>
        "fields": {
          "english": {
            "type":     "text",
            "analyzer": "std_english" <3>
          }
        }
      }
    }
  }
}

POST my-index-000001/_analyze
{
  "field": "my_text", <2>
  "text": "The old brown cow"
}

POST my-index-000001/_analyze
{
  "field": "my_text.english", <3>
  "text": "The old brown cow"
}
```

1. We define the `std_english` analyzer to be based on the `standard` analyzer, but configured to remove the pre-defined list of English stopwords.
2. The `my_text` field uses the `standard` analyzer directly, without any configuration. No stop words will be removed from this field. The resulting terms are: `[ the, old, brown, cow ]`
3. The `my_text.english` field uses the `std_english` analyzer, so English stop words will be removed. The resulting terms are: `[ old, brown, cow ]`


