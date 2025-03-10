---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-match-enrich-policy-type.html
applies_to:
  stack: ga
  serverless: ga
---

# Example: Enrich your data based on geolocation [geo-match-enrich-policy-type]

`geo_match` [enrich policies](data-enrichment.md#enrich-policy) match enrich data to incoming documents based on a geographic location, using a [`geo_shape` query](elasticsearch://reference/query-languages/query-dsl-geo-shape-query.md).

The following example creates a `geo_match` enrich policy that adds postal codes to incoming documents based on a set of coordinates. It then adds the `geo_match` enrich policy to a processor in an ingest pipeline.

Use the [create index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create) to create a source index containing at least one `geo_shape` field.

```console
PUT /postal_codes
{
  "mappings": {
    "properties": {
      "location": {
        "type": "geo_shape"
      },
      "postal_code": {
        "type": "keyword"
      }
    }
  }
}
```

Use the [index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-create) to index enrich data to this source index.

```console
PUT /postal_codes/_doc/1?refresh=wait_for
{
  "location": {
    "type": "envelope",
    "coordinates": [ [ 13.0, 53.0 ], [ 14.0, 52.0 ] ]
  },
  "postal_code": "96598"
}
```
%  TEST[continued]

Use the [create enrich policy API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-enrich-put-policy) to create an enrich policy with the `geo_match` policy type. This policy must include:

* One or more source indices
* A `match_field`, the `geo_shape` field from the source indices used to match incoming documents
* Enrich fields from the source indices you’d like to append to incoming documents

```console
PUT /_enrich/policy/postal_policy
{
  "geo_match": {
    "indices": "postal_codes",
    "match_field": "location",
    "enrich_fields": [ "location", "postal_code" ]
  }
}
```
%  TEST[continued]

Use the [execute enrich policy API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-enrich-execute-policy) to create an enrich index for the policy.

```console
POST /_enrich/policy/postal_policy/_execute?wait_for_completion=false
```
%  TEST[s/?wait_for_completion=false//]
%  TEST[continued]

Use the [create or update pipeline API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-put-pipeline) to create an ingest pipeline. In the pipeline, add an [enrich processor](elasticsearch://reference/ingestion-tools/enrich-processor/enrich-processor.md) that includes:

* Your enrich policy.
* The `field` of incoming documents used to match the geoshape of documents from the enrich index.
* The `target_field` used to store appended enrich data for incoming documents. This field contains the `match_field` and `enrich_fields` specified in your enrich policy.
* The `shape_relation`, which indicates how the processor matches geoshapes in incoming documents to geoshapes in documents from the enrich index. See [Spatial Relations](elasticsearch://reference/query-languages/query-dsl-shape-query.md#_spatial_relations) for valid options and more information.

```console
PUT /_ingest/pipeline/postal_lookup
{
  "processors": [
    {
      "enrich": {
        "description": "Add 'geo_data' based on 'geo_location'",
        "policy_name": "postal_policy",
        "field": "geo_location",
        "target_field": "geo_data",
        "shape_relation": "INTERSECTS"
      }
    }
  ]
}
```
%  TEST[continued]

Use the ingest pipeline to index a document. The incoming document should include the `field` specified in your enrich processor.

```console
PUT /users/_doc/0?pipeline=postal_lookup
{
  "first_name": "Mardy",
  "last_name": "Brown",
  "geo_location": "POINT (13.5 52.5)"
}
```
%  TEST[continued]

To verify the enrich processor matched and appended the appropriate field data, use the [get API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-get) to view the indexed document.

```console
GET /users/_doc/0
```
%  TEST[continued]

The API returns the following response:

```console-result
{
  "found": true,
  "_index": "users",
  "_id": "0",
  "_version": 1,
  "_seq_no": 55,
  "_primary_term": 1,
  "_source": {
    "geo_data": {
      "location": {
        "type": "envelope",
        "coordinates": [[13.0, 53.0], [14.0, 52.0]]
      },
      "postal_code": "96598"
    },
    "first_name": "Mardy",
    "last_name": "Brown",
    "geo_location": "POINT (13.5 52.5)"
  }
}
```
%  TESTRESPONSE[s/"_seq_no": \d+/"_seq_no" : $body._seq_no/ s/"_primary_term":1/"_primary_term" : $body._primary_term/]

