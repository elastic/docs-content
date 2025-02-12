---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/match-enrich-policy-type.html
---

# Example: Enrich your data based on exact values [match-enrich-policy-type]

`match` [enrich policies](data-enrichment.md#enrich-policy) match enrich data to incoming documents based on an exact value, such as a email address or ID, using a [`term` query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-term-query.html).

The following example creates a `match` enrich policy that adds user name and contact information to incoming documents based on an email address. It then adds the `match` enrich policy to a processor in an ingest pipeline.

Use the [create index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create) or [index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-create) to create a source index.

The following index API request creates a source index and indexes a new document to that index.

```console
PUT /users/_doc/1?refresh=wait_for
{
  "email": "mardy.brown@asciidocsmith.com",
  "first_name": "Mardy",
  "last_name": "Brown",
  "city": "New Orleans",
  "county": "Orleans",
  "state": "LA",
  "zip": 70116,
  "web": "mardy.asciidocsmith.com"
}
```

Use the create enrich policy API to create an enrich policy with the `match` policy type. This policy must include:

* One or more source indices
* A `match_field`, the field from the source indices used to match incoming documents
* Enrich fields from the source indices you’d like to append to incoming documents

```console
PUT /_enrich/policy/users-policy
{
  "match": {
    "indices": "users",
    "match_field": "email",
    "enrich_fields": ["first_name", "last_name", "city", "zip", "state"]
  }
}
```

Use the [execute enrich policy API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-enrich-execute-policy) to create an enrich index for the policy.

```console
POST /_enrich/policy/users-policy/_execute?wait_for_completion=false
```

Use the [create or update pipeline API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-put-pipeline) to create an ingest pipeline. In the pipeline, add an [enrich processor](https://www.elastic.co/guide/en/elasticsearch/reference/current/enrich-processor.html) that includes:

* Your enrich policy.
* The `field` of incoming documents used to match documents from the enrich index.
* The `target_field` used to store appended enrich data for incoming documents. This field contains the `match_field` and `enrich_fields` specified in your enrich policy.

```console
PUT /_ingest/pipeline/user_lookup
{
  "processors" : [
    {
      "enrich" : {
        "description": "Add 'user' data based on 'email'",
        "policy_name": "users-policy",
        "field" : "email",
        "target_field": "user",
        "max_matches": "1"
      }
    }
  ]
}
```

Use the ingest pipeline to index a document. The incoming document should include the `field` specified in your enrich processor.

```console
PUT /my-index-000001/_doc/my_id?pipeline=user_lookup
{
  "email": "mardy.brown@asciidocsmith.com"
}
```

To verify the enrich processor matched and appended the appropriate field data, use the [get API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-get) to view the indexed document.

```console
GET /my-index-000001/_doc/my_id
```

The API returns the following response:

```console-result
{
  "found": true,
  "_index": "my-index-000001",
  "_id": "my_id",
  "_version": 1,
  "_seq_no": 55,
  "_primary_term": 1,
  "_source": {
    "user": {
      "email": "mardy.brown@asciidocsmith.com",
      "first_name": "Mardy",
      "last_name": "Brown",
      "zip": 70116,
      "city": "New Orleans",
      "state": "LA"
    },
    "email": "mardy.brown@asciidocsmith.com"
  }
}
```

