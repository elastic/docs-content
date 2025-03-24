---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest-enriching-data.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/index-mgmt.html#manage-enrich-policies
applies_to:
  stack: ga
  serverless: ga
---

# Data enrichment

You can use the [enrich processor](elasticsearch://reference/ingestion-tools/enrich-processor/enrich-processor.md) to add data from your existing indices to incoming documents during ingest.

For example, you can use the enrich processor to:

* Identify web services or vendors based on known IP addresses
* Add product information to retail orders based on product IDs
* Supplement contact information based on an email address
* Add postal codes based on user coordinates


## How the enrich processor works [how-enrich-works]

Most processors are self-contained and only change *existing* data in incoming documents.

:::{image} /manage-data/images/elasticsearch-reference-ingest-process.svg
:alt: ingest process
:::

The enrich processor adds *new* data to incoming documents and requires a few special components:

:::{image} /manage-data/images/elasticsearch-reference-enrich-process.svg
:alt: enrich process
:::

$$$enrich-policy$$$

enrich policy
:   A set of configuration options used to add the right enrich data to the right incoming documents.

An enrich policy contains:

* A list of one or more *source indices* which store enrich data as documents
* The *policy type* which determines how the processor matches the enrich data to incoming documents
* A *match field* from the source indices used to match incoming documents
* *Enrich fields* containing enrich data from the source indices you want to add to incoming documents

Before it can be used with an enrich processor, an enrich policy must be [executed](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-enrich-execute-policy). When executed, an enrich policy uses enrich data from the policy’s source indices to create a streamlined system index called the *enrich index*. The processor uses this index to match and enrich incoming documents.


$$$source-index$$$

source index
:   An index which stores enrich data you’d like to add to incoming documents. You can create and manage these indices just like a regular {{es}} index. You can use multiple source indices in an enrich policy. You also can use the same source index in multiple enrich policies.

$$$enrich-index$$$

enrich index
:   A special system index tied to a specific enrich policy.

Directly matching incoming documents to documents in source indices could be slow and resource intensive. To speed things up, the enrich processor uses an enrich index.

Enrich indices contain enrich data from source indices but have a few special properties to help streamline them:

* They are system indices, meaning they’re managed internally by {{es}} and only intended for use with enrich processors and the {{esql}} `ENRICH` command.
* They always begin with `.enrich-*`.
* They are read-only, meaning you can’t directly change them.
* They are [force merged](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-forcemerge) for fast retrieval.

## Manage enrich policies [manage-enrich-policies]

Use the **Enrich Policies** view to add data from your existing indices to incoming documents during ingest. An enrich policy contains:

* The policy type that determines how the policy matches the enrich data to incoming documents
* The source indices that store enrich data as documents
* The fields from the source indices used to match incoming documents
* The enrich fields containing enrich data from the source indices that you want to add to incoming documents
* An optional [query](elasticsearch://reference/query-languages/query-dsl/query-dsl-match-all-query.md).

:::{image} /manage-data/images/elasticsearch-reference-management-enrich-policies.png
:alt: Enrich policies
:screenshot:
:::

When creating an enrich policy, the UI walks you through the configuration setup and selecting the fields. Before you can use the policy with an enrich processor or {{esql}} query, you must execute the policy.

When executed, an enrich policy uses enrich data from the policy’s source indices to create a streamlined system index called the enrich index. The policy uses this index to match and enrich incoming documents.

Check out these examples:

* [Example: Enrich your data based on geolocation](/manage-data/ingest/transform-enrich/example-enrich-data-based-on-geolocation.md)
* [Example: Enrich your data based on exact values](/manage-data/ingest/transform-enrich/example-enrich-data-based-on-exact-values.md)
* [Example: Enrich your data by matching a value to a range](/manage-data/ingest/transform-enrich/example-enrich-data-by-matching-value-to-range.md)
