---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/range-enrich-policy-type.html
applies_to:
  stack: ga
  serverless: ga
---

# Example: Enrich your data by matching a value to a range [range-enrich-policy-type]

A `range` [enrich policy](data-enrichment.md#enrich-policy) uses a [`term` query](elasticsearch://reference/query-languages/query-dsl-term-query.md) to match a number, date, or IP address in incoming documents to a range of the same type in the enrich index. Matching a range to a range is not supported.

The following example creates a `range` enrich policy that adds a descriptive network name and responsible department to incoming documents based on an IP address. It then adds the enrich policy to a processor in an ingest pipeline.

Use the [create index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create) with the appropriate mappings to create a source index.

```console
PUT /networks
{
  "mappings": {
    "properties": {
      "range": { "type": "ip_range" },
      "name": { "type": "keyword" },
      "department": { "type": "keyword" }
    }
  }
}
```

The following index API request indexes a new document to that index.

```console
PUT /networks/_doc/1?refresh=wait_for
{
  "range": "10.100.0.0/16",
  "name": "production",
  "department": "OPS"
}
```
%  TEST[continued]

Use the create enrich policy API to create an enrich policy with the `range` policy type. This policy must include:

* One or more source indices
* A `match_field`, the field from the source indices used to match incoming documents
* Enrich fields from the source indices you’d like to append to incoming documents

Since we plan to enrich documents based on an IP address, the policy’s `match_field` must be an `ip_range` field.

```console
PUT /_enrich/policy/networks-policy
{
  "range": {
    "indices": "networks",
    "match_field": "range",
    "enrich_fields": ["name", "department"]
  }
}
```
%  TEST[continued]

Use the [execute enrich policy API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-enrich-execute-policy) to create an enrich index for the policy.

```console
POST /_enrich/policy/networks-policy/_execute?wait_for_completion=false
```
%  TEST[s/?wait_for_completion=false//]
%  TEST[continued]

Use the [create or update pipeline API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-put-pipeline) to create an ingest pipeline. In the pipeline, add an [enrich processor](elasticsearch://reference/ingestion-tools/enrich-processor/enrich-processor.md) that includes:

* Your enrich policy.
* The `field` of incoming documents used to match documents from the enrich index.
* The `target_field` used to store appended enrich data for incoming documents. This field contains the `match_field` and `enrich_fields` specified in your enrich policy.

```console
PUT /_ingest/pipeline/networks_lookup
{
  "processors" : [
    {
      "enrich" : {
        "description": "Add 'network' data based on 'ip'",
        "policy_name": "networks-policy",
        "field" : "ip",
        "target_field": "network",
        "max_matches": "10"
      }
    }
  ]
}
```
%  TEST[continued]

Use the ingest pipeline to index a document. The incoming document should include the `field` specified in your enrich processor.

```console
PUT /my-index-000001/_doc/my_id?pipeline=networks_lookup
{
  "ip": "10.100.34.1"
}
```
%  TEST[continued]

To verify the enrich processor matched and appended the appropriate field data, use the [get API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-get) to view the indexed document.

```console
GET /my-index-000001/_doc/my_id
```
%  TEST[continued]

The API returns the following response:

```console-result
{
  "_index" : "my-index-000001",
  "_id" : "my_id",
  "_version" : 1,
  "_seq_no" : 0,
  "_primary_term" : 1,
  "found" : true,
  "_source" : {
    "ip" : "10.100.34.1",
    "network" : [
      {
        "name" : "production",
        "range" : "10.100.0.0/16",
        "department" : "OPS"
      }
    ]
  }
}
```
%  TESTRESPONSE[s/"_seq_no": \d+/"_seq_no" : $body._seq_no/ s/"_primary_term":1/"_primary_term" : $body._primary_term/]

