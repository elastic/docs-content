---
navigation_title: Subfield access
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Troubleshoot subfield access in Painless

Follow these guidelines to avoid nested field access errors in your Painless scripts.

When you access subfields using the doc accessor, using incorrect syntax or trying to access non-existent fields without proper validation leads to runtime errors.

## Sample error

```json
{
  "error": {
    "root_cause": [
      {
        "type": "script_exception",
        "reason": "runtime error",
        "script_stack": [
          "org.elasticsearch.server@9.0.0/org.elasticsearch.search.lookup.LeafDocLookup.getFactoryForDoc(LeafDocLookup.java:146)",
          "org.elasticsearch.server@9.0.0/org.elasticsearch.search.lookup.LeafDocLookup.get(LeafDocLookup.java:186)",
          "org.elasticsearch.server@9.0.0/org.elasticsearch.search.lookup.LeafDocLookup.get(LeafDocLookup.java:33)",
          """start = doc['event'].start.value;
          def """,
          "            ^---- HERE"
        ],
        "script": " ...",
        "lang": "painless",
        "position": {
          "offset": 95,
          "start": 83,
          "end": 131
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
        "index": "events",
        "node": "CxMTEjvKSEC0k0aTr4OM3A",
        "reason": {
          "type": "script_exception",
          "reason": "runtime error",
          "script_stack": [
            "org.elasticsearch.server@9.0.0/org.elasticsearch.search.lookup.LeafDocLookup.getFactoryForDoc(LeafDocLookup.java:146)",
            "org.elasticsearch.server@9.0.0/org.elasticsearch.search.lookup.LeafDocLookup.get(LeafDocLookup.java:186)",
            "org.elasticsearch.server@9.0.0/org.elasticsearch.search.lookup.LeafDocLookup.get(LeafDocLookup.java:33)",
            """start = doc['event'].start.value;
          def """,
            "            ^---- HERE"
          ],
          "script": " ...",
          "lang": "painless",
          "position": {
            "offset": 95,
            "start": 83,
            "end": 131
          },
          "caused_by": {
            "type": "illegal_argument_exception",
            "reason": "No field found for [event] in mapping"
          }
        }
      }
    ]
  },
  "status": 400
}
```

## Problematic approaches

The following two methods of accessing subfields will result in errors:

```json
{
  "runtime_mappings": {
    "event_duration_match": {
      "type": "boolean", 
      "script": {
        "source": """
          // Incorrect approach 1: trying to access nested property
          def start = doc['event'].start.value;
          def end = doc['event'].end.value;
          emit(start == end);
        """
      }
    }
  }
}
```

Or:

```json
{
  "runtime_mappings": {
    "event_duration_match": {
      "type": "boolean",
      "script": {
        "source": """
          // Incorrect approach 2: using bracket notation incorrectly
          def start = doc['event']['start'].value;
          def end = doc['event']['end'].value;
          emit(start == end);
        """
      }
    }
  }
}
```

## Sample data

```json
PUT events/_doc/1
{
  "title": "Conference Call",
  "event": {
    "start": "2024-01-15T09:00:00Z",
    "end": "2024-01-15T10:00:00Z"
  }
}

PUT events/_doc/2
{
  "title": "Team Meeting",
  "event": {
    "start": "2024-01-15T14:00:00Z",
    "end": "2024-01-15T14:00:00Z"
  }
}

PUT events/_doc/3
{
  "title": "Quick Update"
}
```

## Root cause

When accessing subfields in Painless scripts using the `doc` accessor, the correct syntax requires using the full dot notation path as a single string (`doc['parent.child’]`), rather than as a separate property access or bracket notation. This applies to all Painless contexts where `doc` accessor is available, including runtime mapping, script queries, aggregations, and ingest processors.

The error occurs because `doc[‘event’]` attempts to find a field named “event” rather than accessing subfields within the event object. 

## Solution: Correct subfield access with validation

Use full dot notation and validate that the field exists::

```json
POST events/_search
{
  "fields": [
    {
      "field": "*",
      "include_unmapped": "true"
    }
  ],
  "runtime_mappings": {
    "event_duration_match": {
      "type": "boolean",
      "script": {
        "source": """
          if (doc.containsKey('event.start') && doc.containsKey('event.end') && doc['event.start'].size() > 0 && doc['event.end'].size() > 0) {

            def start = doc['event.start'].value;
            def end = doc['event.end'].value;
            emit(start == end);
          } else {
            emit(false);
          }
        """
      }
    }
  }
}
```

## Results

```json
{
  ...,
  "hits": {
    ...,
    "hits": [
      {
        ...,
        "_source": {
          "title": "Conference Call",
          "event": {
            "start": "2024-01-15T09:00:00Z",
            "end": "2024-01-15T10:00:00Z"
          }
        },
        "fields": {
          "title.keyword": [
            "Conference Call"
          ],
          "event_duration_match": [
            false
          ],
          "title": [
            "Conference Call"
          ],
          "event": [
            {
              "start": [
                "2024-01-15T09:00:00.000Z"
              ],
              "end": [
                "2024-01-15T10:00:00.000Z"
              ]
            }
          ]
        }
      },
      {
        ...,
        "_source": {
          "title": "Team Meeting",
          "event": {
            "start": "2024-01-15T14:00:00Z",
            "end": "2024-01-15T14:00:00Z"
          }
        },
        "fields": {
          "title.keyword": [
            "Team Meeting"
          ],
          "event_duration_match": [
            false
          ],
          "title": [
            "Team Meeting"
          ],
          "event": [
            {
              "start": [
                "2024-01-15T14:00:00.000Z"
              ],
              "end": [
                "2024-01-15T14:00:00.000Z"
              ]
            }
          ]
        }
      },
      {
        ...,
        "_source": {
          "title": "Quick Update"
        },
        "fields": {
          "title.keyword": [
            "Quick Update"
          ],
          "title": [
            "Quick Update"
          ],
          "event_duration_match": [
            false
          ]
        }
      }
    ]
  }
}
```

## Notes

* Use full dot notation as a single string: `doc['parent.child’]` rather than `doc['parent.['child’].`  
* Always validate field existence using `.size() > 0` before accessing subfield values.  
* Field validation is crucial when documents have varying object structures.

