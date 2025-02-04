# Enrich your data [ingest-enriching-data]

You can use the [enrich processor](https://www.elastic.co/guide/en/elasticsearch/reference/current/enrich-processor.html) to add data from your existing indices to incoming documents during ingest.

For example, you can use the enrich processor to:

* Identify web services or vendors based on known IP addresses
* Add product information to retail orders based on product IDs
* Supplement contact information based on an email address
* Add postal codes based on user coordinates


## How the enrich processor works [how-enrich-works]

Most processors are self-contained and only change *existing* data in incoming documents.

:::{image} ../../../images/elasticsearch-reference-ingest-process.svg
:alt: ingest process
:::

The enrich processor adds *new* data to incoming documents and requires a few special components:

:::{image} ../../../images/elasticsearch-reference-enrich-process.svg
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

Before it can be used with an enrich processor, an enrich policy must be [executed](https://www.elastic.co/guide/en/elasticsearch/reference/current/execute-enrich-policy-api.html). When executed, an enrich policy uses enrich data from the policy’s source indices to create a streamlined system index called the *enrich index*. The processor uses this index to match and enrich incoming documents.


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
* They are [force merged](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-forcemerge.html) for fast retrieval.






