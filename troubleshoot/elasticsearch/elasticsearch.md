---
navigation_title: "Elasticsearch"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/troubleshooting.html
---

# Troubleshoot {{es}} [troubleshooting]

This section provides a series of troubleshooting solutions aimed at helping users fix problems that an {{es}} deployment might encounter.

::::{tip}
If you’re using Elastic Cloud Hosted, then you can use AutoOps to monitor your cluster. AutoOps significantly simplifies cluster management with performance recommendations, resource utilization visibility, real-time issue detection and resolution paths. For more information, refer to [Monitor with AutoOps](/deploy-manage/monitor/autoops.md).

::::



## General [troubleshooting-general]

* [Fix common cluster issues](fix-common-cluster-issues.md)
* Several troubleshooting issues can be diagnosed using the [health API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-health-report).


## Data [troubleshooting-data]

* [Fix watermark errors caused by low disk space](fix-watermark-errors.md)
* [Add a missing tier to the system](add-tier.md)
* [Allow Elasticsearch to allocate the data in the system](allow-all-cluster-allocation.md)
* [Allow Elasticsearch to allocate the index](allow-all-index-allocation.md)
* [Indices mix index allocation filters with data tiers node roles to move through data tiers](troubleshoot-migrate-to-tiers.md)
* [Not enough nodes to allocate all shard replicas](increase-tier-capacity.md)
* [Total number of shards for an index on a single node exceeded](increase-shard-limit.md)
* [Total number of shards per node has been reached](increase-cluster-shard-limit.md)
* [Troubleshooting data corruption](corruption-troubleshooting.md)


## Management [troubleshooting-management]

* [Troubleshoot index and snapshot lifecycle management](start-ilm.md)
* [Fix index lifecycle management errors](/troubleshoot/elasticsearch/index-lifecycle-management-errors.md)


## Capacity [troubleshooting-capacity]

* [Fix data nodes out of disk](fix-data-node-out-of-disk.md)
* [Fix master nodes out of disk](fix-master-node-out-of-disk.md)
* [Fix other role nodes out of disk](fix-other-node-out-of-disk.md)


## Snapshot and restore [troubleshooting-snapshot]

* [Restore data from snapshot](restore-from-snapshot.md)
* [Troubleshooting broken repositories](add-repository.md)
* [Troubleshooting repeated snapshot failures](repeated-snapshot-failures.md)


## Other issues [troubleshooting-others]

* [Troubleshooting an unstable cluster](troubleshooting-unstable-cluster.md)
* [Troubleshooting discovery](discovery-troubleshooting.md)
* [Troubleshooting monitoring](monitoring-troubleshooting.md)
* [Troubleshooting transforms](transform-troubleshooting.md)
* [Troubleshooting Watcher](watcher-troubleshooting.md)
* [Troubleshooting searches](troubleshooting-searches.md)
* [Troubleshooting shards capacity](troubleshooting-shards-capacity-issues.md)
* [Troubleshooting an unbalanced cluster](troubleshooting-unbalanced-cluster.md)
* [Troubleshooting remote clusters](/troubleshoot/elasticsearch/remote-clusters.md)


## Contact us [troubleshooting-contact-support]

If none of these guides relate to your issue, or you need further assistance, then you can contact us as follows:

* If you have an active subscription, you have several options:

    * Go directly to the [Support Portal](http://support.elastic.co)
    * From the {{ecloud}} Console, go to the [Support page](https://cloud.elastic.co/support?page=docs&placement=docs-body), or select the support icon that looks like a life preserver on any page.
    * Contact us by email: `support@elastic.co`

        ::::{tip}
        If you contact us by email, use the email address that you registered with so that we can help you more quickly. If you are using a distribution list as your registered email, you can also register a second email address with us. Just open a case to let us know the name and email address you want to add.

        ::::

* For users without an active subscription, visit the [Elastic community forums](https://discuss.elastic.co/) and get answers from the experts in the community, including people from Elastic.
