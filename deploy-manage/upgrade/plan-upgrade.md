---
applies_to:
  stack:
  deployment:
    eck:
    ess:
    ece:
    self:
---
# Plan your upgrade

There are several important factors to consider before starting the upgrade process. Use the following recommendations to build a solid upgrade plan:

* Plan for an appropriate amount of time to complete the upgrade. Depending on your configuration and the size of your cluster, the process may take just a few minutes or several hours. In more complex environments, it could extend to a few weeks or more.
* Consider opening a [support case](https://support.elastic.co/) with Elastic to alert our Elastic Support team of your system change. If you need additional assistance, [Elastic Consulting Services](https://www.elastic.co/consulting) provides the technical expertise and step-by-step approach for upgrading your environment.
* Schedule a system maintenance window within your organization.
* When possible, perform testing of the upgrade process in a non-production environment.

The objective of this section is to facilitate the creation of an upgrade plan that addresses all the necessary steps and preparations needed for upgrading your deployment or cluster.

## Compatibility checks

Before upgrading, verify that your current environment supports the version you plan to upgrade to. If not, identify any required intermediate upgrades or component changes and include them in your upgrade plan.

* **System requirements**: Ensure your current operating system is supported by the target versions of {{es}}, {{kib}}, and any ingest components. Refer to the [Product and Operating System support matrix](https://www.elastic.co/support/matrix#matrix_os).

* **Ingest component compatibility**: Confirm that your ingest components, such as {{beats}}, {{ls}}, or {{agent}}, are compatible with the target {{es}} version. If they’re not, upgrade them first. Refer to [conduct a component inventory](#conduct-a-component-inventory) for guidance.

* **Orchestrator compatibility**: If you’re using an orchestrator like {{ece}} or {{eck}}, verify that it supports the target {{stack}} version. If not, [upgrade the orchestrator](/deploy-manage/upgrade/orchestrator.md) before upgrading your cluster. Refer to:
  * [ECE – Stack packs](/deploy-manage/deploy/cloud-enterprise/manage-elastic-stack-versions.md#ece_most_recent_elastic_stack_packs)
  * [ECK – {{stack}} compatibility](/deploy-manage/deploy/cloud-on-k8s.md#stack-compatibility)

* **Rest API compatibility**: If you use custom-developed applications or clients, ensure the [{{es}} client libraries](/reference/elasticsearch-clients/index.md) are compatible with the target version. If your applications use deprecated or removed APIs, you may need to update the client code first.

    ::::{note}
    By default, 8.x {{es}} clients are compatible with 9.x and use [`REST API compatibility`](elasticsearch://reference/elasticsearch/rest-apis/compatibility.md) to maintain compatibility with the 9.x {{es}} cluster.

    `REST API compatibility` is a per-request opt-in feature that can help REST clients mitigate non-compatible (breaking) changes to the REST API.
    ::::

* **Index compatibility**: {{es}} provides full query and write support for indices created in the previous major version. If you have indices created in 7.x or earlier, you must reindex, delete, or [mark them as read-only](/deploy-manage/upgrade/deployment-or-cluster/reading-indices-from-older-elasticsearch-versions.md) before upgrading to 9.x. This topic is covered during the [upgrade preparations](prepare-to-upgrade.md#prepare-to-upgrade-from-8.x), with help from the Upgrade Assistant.

* **{{es}} upgrade path**: Check the [upgrade paths](../upgrade.md#upgrade-paths) to determine whether you must upgrade through an intermediate version (such as 8.19.x before moving to 9.x), or if you can upgrade directly to the target version.

* **OpenJDK compatibility and FIPS compliance**: By default, {{es}} is built using Java and includes a bundled version of [OpenJDK](https://openjdk.java.net/) within each distribution. While we strongly recommend using the bundled Java Virtual Machine (JVM) in all installations of {{es}}, if you choose to use your own JVM, ensure it’s compatible by reviewing the [Product and JVM support matrix](https://www.elastic.co/support/matrix#matrix_jvm). 

  If you’re running {{es}} in FIPS 140-2 mode, we recommend using  [Bouncy Castle](https://www.bouncycastle.org/java.html) as a Java security provider when running {{es}}.

## Conduct a component inventory

When you plan to upgrade your deployment, it is very important to map all the components that are being used on the {{stack}}, and check if they are compatible with the {{es}} version you plan to upgrade to by reviewing the [Product compatibility support matrix](https://www.elastic.co/support/matrix#matrix_compatibility).

::::{note}
If any of your ingest components does not support the {{es}} version you plan to upgrade to, you need to upgrade that component to a version that supports the desired {{es}} version before upgrading {{es}}.
::::

As part of the upgrade plan, you will also have to determine if you want to upgrade the ingest components to the same version as {{es}}, after the upgrade of {{es}} and {{kib}}.

While not comprehensive, here’s a list of components you should check:

* {{es}}
* {{es}} Hadoop
* {{es}} plugins
* {{es}} clients
* {{ls}}
* {{ls}} plugins
* {{beats}}
* {{beats}} modules
* {{apm-agent}}
* APM server
* {{agent}}
* {{fleet}}
* Security
* Browsers
* External services (Kafka, etc.)

:::{tip}
When you do your inventory, you can [enable audit logging](/deploy-manage/security/logging-configuration/enabling-audit-logs.md) to evaluate resources accessing your deployment.
:::

## Test in a non-production environment

We highly recommend testing the upgrade process in a non-production environment before applying changes to your production environment. To ensure meaningful results, your test and production environments should be configured as similarly as possible. Consider validating the following areas:

* Enrichment information
* Plugins
* Mapping
* Index lifecycle management (ILM)
* Snapshot lifecycle management (SLM)
* Index templates
* {{ml-cap}} jobs
* Inbound sample data
* Live data
* Performance
* Outbound integrations
* Dashboards
* Alerts
* Authentication

## Upgrade order

When upgrading the {{stack}}, the process begins with {{es}}, followed by {{kib}}, which must always be aligned in terms of versioning. Other components can remain on earlier versions as long as they are compatible with the target {{es}} version, though we recommend upgrading them as well to benefit from the latest features and fixes.

If all components are compatible with the target version of {{es}}, we recommend upgrading them in the following order:

1. {{es}}
2. {{kib}} (must be kept aligned with the {{es}} version)
3. Fleet Server and APM Server (if used)
4. Ingest tools (Beats, Elastic Agent, Logstash, etc.) and {{es}} client libraries

::::{note}
If you use a separate [monitoring cluster](/deploy-manage/monitor/stack-monitoring/elasticsearch-monitoring-self-managed.md), upgrade the monitoring cluster before the production cluster.

The monitoring cluster should be running the same version, or a newer one, than the clusters being monitored. It cannot monitor clusters running a newer version of the {{stack}}. If necessary, the monitoring cluster can monitor clusters running the latest release of the previous major version.
::::

## Example of an upgrade plan

Let's assume you are running all {{stack}} components in version 8.14 and your main goal is to upgrade {{es}} and {{kib}} to the latest {{stack-version}}, without requiring to upgrade the ingest components (Beats, Elastic Agent, and Logstash) except when required by the [upgrade paths](../upgrade.md#upgrade-paths).

The minimum steps your plan should include are:

1. Upgrade {{es}} and {{kib}} to the latest 8.19 version, as a requirement for the major upgrade to {{stack-version}}.
2. Upgrade all ingest components to the latest 8.19 version, as otherwise they won't be compatible with {{es}} running {{stack-version}}.
3. Upgrade {{es}} and {{kib}} to {{stack-version}}.

## Next steps

Once you’ve planned your upgrade and defined a clear upgrade path for all the components, you can proceed to the [upgrade preparations](/deploy-manage/upgrade/prepare-to-upgrade.md).