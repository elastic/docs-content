# Upgrade to Elastic 9.0.0-beta1 [upgrading-elastic-stack]

Before you upgrade to 9.0.0-beta1, it’s important to take some preparation steps. These steps vary based on your current version:

* [Upgrade from an earlier 8.x version](../../../deploy-manage/upgrade/deployment-or-cluster.md#prepare-to-upgrade-8x)
* [Upgrade from 7.x](../../../deploy-manage/upgrade/deployment-or-cluster.md#prepare-to-upgrade)

::::{important}
Upgrading from a release candidate build, such as 8.0.0-rc1 or 8.0.0-rc2, is not supported. Pre-releases should only be used for testing in a temporary environment.
::::



## Prepare to upgrade from an earlier 8.x version [prepare-to-upgrade-8x]

1. Review the breaking changes for each product you use and make the necessary changes so your code is compatible with 9.0.0-beta1:

    * [APM breaking changes](https://www.elastic.co/guide/en/apm/guide/current/apm-breaking.html)
    * [{{beats}} breaking changes](https://www.elastic.co/guide/en/beats/libbeat/current/breaking-changes.html)
    * [{{es}} migration guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/breaking-changes.html)
    * [{{elastic-sec}} release notes](https://www.elastic.co/guide/en/security/current/release-notes.html)
    * [{{ents}} release notes](https://www.elastic.co/guide/en/enterprise-search/current/changelog.html)
    * [{{fleet}} and {{agent}} release notes](https://www.elastic.co/guide/en/fleet/current/release-notes.html)
    * [{{kib}} release notes](https://www.elastic.co/guide/en/kibana/current/release-notes.html)
    * [{{ls}} breaking changes](https://www.elastic.co/guide/en/logstash/current/breaking-changes.html)

    ::::{important}
    * Make sure you check the breaking changes for each minor release up to 9.0.0-beta1.
    * If you are using {{ml}} {dfeeds} that contain discontinued search or query domain specific language (DSL), the upgrade will fail. In 5.6.5 and later, the Upgrade Assistant provides information about which {{dfeeds}} need to be updated.

    ::::

2. If you use any {{es}} plugins, make sure there is a version of each plugin that is compatible with {{es}} version 9.0.0-beta1.
3. Test the upgrade in an isolated environment before upgrading your production cluster.
4. Make sure you have a current snapshot before you start the upgrade.

    ::::{important}
    You cannot downgrade {{es}} nodes after upgrading. If you cannot complete the upgrade process, you will need to restore from the snapshot.
    ::::

5. If you use a separate [monitoring cluster](../../../deploy-manage/monitor/stack-monitoring/elasticsearch-monitoring-self-managed.md), you should upgrade the monitoring cluster before the production cluster. In general, the monitoring cluster and the clusters being monitored should be running the same version of the stack. A monitoring cluster cannot monitor production clusters running newer versions of the stack. If necessary, the monitoring cluster can monitor production clusters running the latest release of the previous major version.


## Prepare to upgrade from 7.x [prepare-to-upgrade]

To upgrade to 9.0.0-beta1 from 7.16 or earlier, **you must first upgrade to 8.17**. This enables you to use the **Upgrade Assistant** to identify and resolve issues, reindex indices created before 7.0, and then perform a rolling upgrade.

**Upgrading to 8.17 before upgrading to 9.0.0-beta1 is required even if you opt to do a full-cluster restart of your {{es}} cluster.** Alternatively, you can create a new 9.0.0-beta1 deployment and reindex from remote. For more information, see [Reindex to upgrade](../../../deploy-manage/upgrade/deployment-or-cluster.md#upgrading-reindex).

{{beats}} and {{ls}} 8.17 are compatible with {{es}} 9.0.0-beta1 to give you flexibility in scheduling the upgrade.

::::{admonition} Remote cluster compatibility
:class: note

If you use {{ccs}}, note that 9.0.0-beta1 can only search remote clusters running the previous minor version or later. For more information, see [Searching across clusters](../../../solutions/search/cross-cluster-search.md).

If you use {{ccr}}, a cluster that contains follower indices must run the same or newer version as the remote cluster. For more information, see [Cross cluster replication](../../../deploy-manage/tools/cross-cluster-replication.md) for version compatibility matrix.

You can view your remote clusters from **Stack Management > Remote Clusters**.

::::


1. Use the [Upgrade Assistant](https://www.elastic.co/guide/en/kibana/8.17/upgrade-assistant.html) to prepare for your upgrade from 8.17 to 9.0.0-beta1. The **Upgrade Assistant** identifies deprecated settings and guides you through resolving issues and reindexing indices created before 7.0. Make sure you have a current snapshot before making configuration changes or reindexing.

    **You must resolve all critical issues before proceeding with the upgrade.**

2. Review the deprecation logs from the **Upgrade Assistant** to determine if your applications are using features that are not supported or behave differently in 8.x. See the [breaking changes](https://www.elastic.co/guide/en/elastic-stack/current/elastic-stack-breaking-changes.html) for more information about changes in 9.0.0-beta1 that could affect your application.

    ::::{important}
    Make sure you check the breaking changes for each minor 8.x release up to 9.0.0-beta1.
    ::::

3. Make the recommended changes to ensure that your applications continue to operate as expected after the upgrade.

    ::::{note}
    As a temporary solution, you can submit requests to 9.x using the 8.x syntax with the REST API compatibility mode. While this enables you to submit requests that use the old syntax, it does not guarantee the same behavior. REST API compatibility should be a bridge to smooth out the upgrade process, not a long term strategy. For more information, see [REST API compatibility](https://www.elastic.co/guide/en/elasticsearch/reference/current/rest-api-compatibility.html).
    ::::

4. If you use any {{es}} plugins, make sure there is a version of each plugin that is compatible with {{es}} version 9.0.0-beta1.
5. Test the upgrade in an isolated environment before upgrading your production cluster.
6. Make sure you have a current snapshot before you start the upgrade.

    ::::{important}
    You cannot downgrade {{es}} nodes after upgrading. If you cannot complete the upgrade process, you will need to restore from the snapshot.
    ::::

7. If you use a separate [monitoring cluster](../../../deploy-manage/monitor/stack-monitoring/elasticsearch-monitoring-self-managed.md), you should upgrade the monitoring cluster before the production cluster. In general, the monitoring cluster and the clusters being monitored should be running the same version of the stack. A monitoring cluster cannot monitor production clusters running newer versions of the stack. If necessary, the monitoring cluster can monitor production clusters running the latest release of the previous major version.
