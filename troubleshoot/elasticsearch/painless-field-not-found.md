---
navigation_title: Field not found (mapping conflicts)
---

# Troubleshoot field not found (mapping conflicts) in Painless

Follow these guidelines to avoid field access errors in your Painless script.

## A document doesn't have a value for a field

When working with document fields, attempting to access fields that don't exist in all documents or aren't properly mapped leads to field not found exceptions, causing script failures.

### Sample error

```json
{
  "error": {
    "root_cause": [
      {
        "type": "script_exception",
        "reason": "runtime error",
        "script_stack": [
          "org.elasticsearch.server@9.0.0/org.elasticsearch.index.fielddata.ScriptDocValues.throwIfEmpty(ScriptDocValues.java:93)",
          "org.elasticsearch.server@9.0.0/org.elasticsearch.index.fielddata.ScriptDocValues$Longs.get(ScriptDocValues.java:117)",
          "org.elasticsearch.server@9.0.0/org.elasticsearch.index.fielddata.ScriptDocValues$Longs.getValue(ScriptDocValues.java:112)",
          "doc['author_score'].value > 50 ? doc['author_score'].value : 1",
          "                   ^---- HERE"
        ],
        "script": "doc['author_score'].value > 50 ? doc['author_score'].value : 1",
        "lang": "painless",
        "position": {
          "offset": 19,
          "start": 0,
          "end": 62
        }
      }
    ],
    "type": "search_phase_execution_exception",
    "reason": "all shards failed",
    "phase": "query",
    "grouped": true,
    "failed_shards": [
      {
        "shard": 0,
        "index": "articles",
        "node": "hupWdkj_RtmThGjNUiIt_w",
        "reason": {
          "type": "script_exception",
          "reason": "runtime error",
          "script_stack": [
            "org.elasticsearch.server@9.0.0/org.elasticsearch.index.fielddata.ScriptDocValues.throwIfEmpty(ScriptDocValues.java:93)",
            "org.elasticsearch.server@9.0.0/org.elasticsearch.index.fielddata.ScriptDocValues$Longs.get(ScriptDocValues.java:117)",
            "org.elasticsearch.server@9.0.0/org.elasticsearch.index.fielddata.ScriptDocValues$Longs.getValue(ScriptDocValues.java:112)",
            "doc['author_score'].value > 50 ? doc['author_score'].value : 1",
            "                   ^---- HERE"
          ],
          "script": "doc['author_score'].value > 50 ? doc['author_score'].value : 1",
          "lang": "painless",
          "position": {
            "offset": 19,
            "start": 0,
            "end": 62
          },
          "caused_by": {
            "type": "illegal_state_exception",
            "reason": "A document doesn't have a value for a field! Use doc[<field>].size()==0 to check if a document is missing a field!"
          }
        }
      }
    ]
  },
  "status": 400
}
```

### Problematic code

```json
{
  "query": {
    "function_score": {
      "query": {
        "match_all": {}
      },
      "script_score": {
        "script": {
          "source": "doc['author_score'].value > 50 ? doc['author_score'].value : 1",
          "lang": "painless"
        }
      }
    }
  }
}
```

### Root cause

A field not found exception occurs when a script tries to access a field that is not defined in the index mappings. If the field is defined in the mappings but has no value in some documents, the script will not fail as long as you first check whether the field has values.  
   
For example, calling `doc['author_score'].value` directly on a document without that field will cause an error. The recommended approach is to use `doc[<field>].size()==0` to check if the field is missing in a document before accessing its value.

### Sample documents

```json
POST articles/_doc
{
  "title": "Complete Guide to Elasticsearch",
  "content": "This is a comprehensive guide...",
  "author": "John Doe",
  "author_score": 85
}

POST articles/_doc
{
  "title": "Basic Query Tutorial",
  "content": "Learn the fundamentals...",
  "author": "Jane Smith"
}
```

### Solution 1: Check field existence before accessing

Always verify field existence using `size()` before accessing field values:

```json
GET articles/_search
{
  "query": {
    "function_score": {
      "query": {
        "match_all": {}
      },
      "script_score": {
        "script": {
          "source": """
            if (doc['author_score'].size() > 0) {
              return doc['author_score'].value > 50 ? doc['author_score'].value : 1;
            } else {
              return 1;
            }
          """,
          "lang": "painless"
        }
      }
    }
  }
}
```

### Solution 2: New field API approach

The [field API](/explore-analyze/scripting/script-fields-api.md) provides a more elegant solution that handles missing values automatically by allowing you to specify default values. This approach is more concise and eliminates the need for explicit field existence checks:

```json
GET articles/_search
{
  "query": {
    "function_score": {
      "query": {
        "match_all": {}
      },
      "script_score": {
        "script": {
          "source": """
            long authorScore = field('author_score').get(1L);
            return authorScore > 50 ? authorScore : 1;
          """,
          "lang": "painless"
        }
      }
    }
  }
}
```

### Solution 3: Use the $ shortcut in field API syntax

With the field API you can make the solution even more concise using the `$` shortcut:

```json
GET articles/_search
{
  "query": {
    "function_score": {
      "query": {
        "match_all": {}
      },
      "script_score": {
        "script": {
          "source": """
            long authorScore = $('author_score', 1L);
            return authorScore > 50 ? authorScore : 1;
          """,
          "lang": "painless"
        }
      }
    }
  }
}
```

### Results

```json
{
  ...,
  "hits": {
    ...,
    "hits": [
      {
        "_index": "articles",
        "_id": "pnZXL5kBTbKqUnB52aCH",
        "_score": 85,
        "_source": {
          "title": "Complete Guide to Elasticsearch",
          "content": "This is a comprehensive guide...",
          "author": "John Doe",
          "author_score": 85
        }
      },
      {
        "_index": "articles",
        "_id": "i6hXL5kB0eMypkDY3mQ4",
        "_score": 1,
        "_source": {
          "title": "Basic Query Tutorial",
          "content": "Learn the fundamentals...",
          "author": "Jane Smith"
        }
      }
    ]
  }
}
```

### Notes

* **Field presence:** Always check if fields exist before accessing them using `.size() > 0`.  
* **Document variation:** Not all documents are guaranteed to have the same field structure.  
* **Mapping awareness:** A field must be defined in the index mappings to be accessed with doc values, and its value in each document must be validated.  
* **Field API:** The `field` API and `$` shortcut handle missing values gracefully with default values.  
* **Compatibility:** Some field types (like `text` or `geo`) [aren't yet supported](/explore-analyze/scripting/script-fields-api.md#_supported_mapped_field_types) by the field API; continue using `doc` for those.


