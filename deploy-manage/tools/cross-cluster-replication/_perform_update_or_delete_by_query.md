---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/_perform_update_or_delete_by_query.html

applies_to:
  deployment:
    eck: 
    ess: 
    ece: 
    self: 
---

# Perform update or delete by query [_perform_update_or_delete_by_query]

It is possible to update or delete the documents but you can only perform these actions on the leader index.

1. First identify which backing index contains the document you want to update.

    ```console
    ### On either of the cluster ###
    GET logs-generic-default*/_search?filter_path=hits.hits._index
    {
    "query": {
        "match": {
          "event.sequence": "97"
        }
      }
    }
    ```

    * If the hits returns `"_index": ".ds-logs-generic-default-replicated_from_clustera-<yyyy.MM.dd>-*"`, then you need to proceed to the next step on `cluster A`.
    * If the hits returns `"_index": ".ds-logs-generic-default-replicated_from_clusterb-<yyyy.MM.dd>-*"`, then you need to proceed to the next step on `cluster B`.
    * If the hits returns `"_index": ".ds-logs-generic-default-<yyyy.MM.dd>-*"`, then you need to proceed to the next step on the same cluster where you performed the search query.

2. Perform the update (or delete) by query:

    ```console
    ### On the cluster identified from the previous step ###
    POST logs-generic-default/_update_by_query
    {
      "query": {
        "match": {
          "event.sequence": "97"
        }
      },
      "script": {
        "source": "ctx._source.event.original = params.new_event",
        "lang": "painless",
        "params": {
          "new_event": "FOOBAR"
        }
      }
    }
    ```

    ::::{tip} 
    If a soft delete is merged away before it can be replicated to a follower the following process will fail due to incomplete history on the leader, see [index.soft_deletes.retention_lease.period](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/index-settings/index.md#ccr-index-soft-deletes-retention-period) for more details.
    ::::


