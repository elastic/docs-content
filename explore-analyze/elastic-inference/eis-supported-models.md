---
navigation_title: Supported models
applies_to:
  stack: ga
  serverless: ga
products:
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
description: Identify the models that are supported by Elastic Inference Service (EIS).
---

# Elastic {{infer-cap}} Service supported models

The following tables list the models supported by Elastic {{infer-cap}} Service by model type.

The corresponding {{kib}} connectors and {{infer}} endpoints for these models are created automatically. To customize the configuration, you can create [your own connectors](kibana://reference/connectors-kibana.md#creating-new-connector) or [{{infer}} endpoints](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put).

::::{note}
The **{{infer-cap}} Regions** column shows the regions where {{infer}} requests are processed and where data is sent.
::::

For region availability and request routing, refer to [Region and hosting](eis-region-and-hosting.md). For rate limits, refer to [Rate limits](eis-rate-limits.md).

### LLM chat models

:::{csv-include} chat-models.csv
:caption: Scroll horizontally to view more information.
:::

### Embedding models

:::{csv-include} embedding-models.csv
:caption: Scroll horizontally to view more information.
:::

### Rerankers

:::{csv-include} reranker-models.csv
:caption: Scroll horizontally to view more information.
:::

::::{important}

* The applicable terms of use, uptime, and performance for each of the AI models available with EIS are each described in the applicable AI model's Provider Terms and Model Card.
* Prior to using the AI model with EIS, Customers are responsible for reviewing and agreeing to the chosen AI model's Provider Terms to understand the availability and data practices of the AI model's provider.
* After the listed end-of-life (EOL) date, the model is no longer available for {{infer}} use and requests will fail. You need to actively transition to another model before the EOL date, there is no automated migration.
* Elastic makes every effort to use third party providers who do not use inputs to train models, and do not retain any data (zero data retention). Browse the tables on this page to double-check the status of a specific model.
::::
