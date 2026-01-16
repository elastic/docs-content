---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/transforms.html
  - https://www.elastic.co/guide/en/serverless/current/transforms.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/data-rollup-transform.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
  - id: cloud-serverless
---
# Transforming data [transforms]

Transforms enable you to convert existing {{es}} indices into summarized indices, which provide opportunities for new insights and analytics. For example, you can use transforms to pivot your data into entity-centric indices that summarize the behavior of users or sessions or other entities in your data. Or you can use transforms to find the latest document among all the documents that have a certain unique key.

* [Overview](transforms/transform-overview.md)
* [Setup](transforms/transform-setup.md)
* [When to use transforms](transforms/transform-usage.md)
* [Generating alerts for transforms](transforms/transform-alerts.md)
* [Transforms at scale](transforms/transform-scale.md)
* [How checkpoints work](transforms/transform-checkpoints.md)
* [API quick reference](transforms/transform-api-quickref.md)
* [Tutorial: Transforming the eCommerce sample data](transforms/ecommerce-transforms.md)
* [Examples](transforms/transform-examples.md)
* [Painless examples](transforms/transform-painless-examples.md)
* [Troubleshooting transforms](../troubleshoot/elasticsearch/transform-troubleshooting.md)
* [Limitations](transforms/transform-limitations.md)
