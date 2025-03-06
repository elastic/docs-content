---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/synthetics-journeys.html
  - https://www.elastic.co/guide/en/serverless/current/observability-synthetics-journeys.html
---

# Scripting browser monitors [synthetics-journeys]

Browser monitors are a type of synthetic monitor. Synthetic monitoring extends traditional end-to-end testing techniques because it allows your tests to run continuously on the cloud. With synthetic monitoring, you can assert that your application continues to work after a deployment by reusing the same journeys that you used to validate the software on your machine.

You can use synthetic monitors to detect bugs caused by invalid states you couldn’t predict and didn’t write tests for. Synthetic monitors can also help you catch bugs in features that don’t get much traffic by allowing you to periodically simulate users' actions.

Start by learning the basics of synthetic monitoring, including how to:

* [Write a synthetic test](../../../solutions/observability/apps/write-synthetic-test.md)
* [Test locally](../../../solutions/observability/apps/write-synthetic-test.md#synthetics-test-locally)
* [Configure individual browser monitors](../../../solutions/observability/apps/configure-individual-browser-monitors.md)
* [Work with params and secrets](../../../solutions/observability/apps/work-with-params-secrets.md)
* [Use the Synthetics Recorder](../../../solutions/observability/apps/use-synthetics-recorder.md)

:::{image} ../../../images/observability-synthetic-monitor-lifecycle.png
:alt: Diagram of the lifecycle of a synthetic monitor: write a test
:class: screenshot
:::