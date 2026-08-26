---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/ingest-data.html
  - https://www.elastic.co/guide/en/serverless/current/security-ingest-data.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Ingest data to {{elastic-sec}} [security-ingest-data]

To ingest data, you can use:

* The [{{agent}}](/reference/fleet/index.md) with the **{{elastic-defend}}** integration, which protects your hosts and sends logs, metrics, and endpoint security data to {{elastic-sec}}. See [Install {{elastic-defend}}](/solutions/security/configure-elastic-defend/install-elastic-defend.md).
* The {{agent}} with integrations, which are available in the [Elastic Package Registry (EPR)](/reference/fleet/index.md#package-registry-intro). To install an integration that works with {{elastic-sec}}, go to the {{kib}} Home page or navigation menu and click **Add integrations**. On the Integrations page, click the **Security** category filter, then select an integration to view the installation instructions. For more information on integrations, refer to [{{integrations}}](https://docs.elastic.co/en/integrations).
* [{{beats}}](beats://reference/index.md) shippers installed for each system you want to monitor.
* **{{ls}}**, which dynamically ingests, transforms, and ships your data regardless of format.
* Third-party collectors configured to ship ECS-compliant data. [](/reference/security/fields-and-object-schemas/siem-field-reference.md) provides a list of ECS fields used in {{elastic-sec}}.

::::{important}
If you use a third-party collector—or some {{ls}} plugins without {{agent}} or {{beats}}—to ship data to {{elastic-sec}}, you must map its fields to the [Elastic Common Schema (ECS)](ecs://reference/index.md). Additionally, you must add its index to the {{elastic-sec}} indices (update the `securitySolution:defaultIndex` [advanced setting](/solutions/security/get-started/configure-advanced-settings.md#update-sec-indices)).

{{elastic-sec}} uses the [`host.name`](ecs://reference/ecs-host.md) ECS field as the primary key for identifying hosts.

::::


The {{agent}} with the [{{elastic-defend}} integration](https://www.elastic.co/products/endpoint-security) ships these data sources:

* Process - Linux, macOS, Windows
* Network - Linux, macOS, Windows
* File - Linux, macOS, Windows
* DNS - Windows
* Registry - Windows
* DLL and Driver Load - Windows
* Security - Windows
