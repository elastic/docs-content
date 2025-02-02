# {{transforms-app}} [transforms]

This content applies to: [![Elasticsearch](../../../images/serverless-es-badge.svg "")](../../../solutions/search.md) [![Observability](../../../images/serverless-obs-badge.svg "")](../../../solutions/observability.md) [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md)

{{transforms-cap}} enable you to convert existing {{es}} indices into summarized indices, which provide opportunities for new insights and analytics.

For example, you can use {{transforms}} to pivot your data into entity-centric indices that summarize the behavior of users or sessions or other entities in your data. Or you can use {{transforms}} to find the latest document among all the documents that have a certain unique key.

For more information, check out:

* [When to use transforms](../../../explore-analyze/transforms/transform-usage.md)
* [Generating alerts for transforms](../../../explore-analyze/transforms/transform-alerts.md)
* [Transforms at scale](../../../explore-analyze/transforms/transform-scale.md)
* [How checkpoints work](../../../explore-analyze/transforms/transform-checkpoints.md)
* [Examples](../../../explore-analyze/transforms/transform-examples.md)
* [Painless examples](../../../explore-analyze/transforms/transform-painless-examples.md)
* [Troubleshooting transforms](../../../troubleshoot/elasticsearch/transform-troubleshooting.md)
* [Limitations](../../../explore-analyze/transforms/transform-limitations.md)


## Create and manage {{transforms}} [transforms-create-and-manage-transforms]

In **{{project-settings}} → {{manage-app}} → {{transforms-app}}**, you can create, edit, stop, start, reset, and delete {{transforms}}:

:::{image} ../../../images/serverless-transform-management.png
:alt: {{transforms-app}} app
:class: screenshot
:::

When you create a {{transform}}, you must choose between two types: *pivot* and *latest*. You must also decide whether you want the {{transform}} to run once or continuously. For more information, go to [{{transforms-cap}} overview](../../../explore-analyze/transforms/transform-overview.md).
