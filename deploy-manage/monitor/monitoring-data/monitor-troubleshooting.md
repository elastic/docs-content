---
navigation_title: Troubleshooting
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/monitor-troubleshooting.html
applies_to:
  deployment:
    self: all
products:
  - id: kibana
---

% this page probably needs to be moved


# Troubleshooting visualizing monitoring data in {{kib}} [monitor-troubleshooting]


Use the information in this section to troubleshoot common problems and find answers for frequently asked questions related to the {{kib}} {{monitor-features}}.


## Cannot view the cluster because the license information is invalid [_cannot_view_the_cluster_because_the_license_information_is_invalid]

**Symptoms:**

The following error appears in a banner at the top of the screen in {{kib}} on the **Stack Monitoring > Clusters** page: `You can't view the "<my_cluster>" cluster because the license information is invalid.`

**Resolution:**

You cannot monitor a version 6.3 or later cluster from {{kib}} version 6.2 or earlier. To resolve this issue, upgrade {{kib}} to 6.3 or later. See [Upgrading the {{stack}}](../../upgrade/deployment-or-cluster.md).


## {{filebeat}} index is corrupt [_filebeat_index_is_corrupt]

**Symptoms:**

The **Stack Monitoring** application displays a Monitoring Request error indicating that an illegal argument exception has occurred because fielddata is disabled on text fields by default.

**Resolution**

1. Stop all your {{filebeat}} instances.
2. Delete indices beginning with `filebeat-$VERSION`, where `VERSION` corresponds to the version of {{filebeat}} running.
3. Restart all your {{filebeat}} instances.


## No monitoring data is visible in {{kib}} [_no_monitoring_data_is_visible_in_kib]

**Symptoms:**

The **Stack Monitoring** page in {{kib}} is empty.

**Resolution:**

1. Confirm that {{kib}} is seeking monitoring data from the appropriate {{es}} URL. By default, data is retrieved from the cluster specified in the `elasticsearch.hosts` setting in the [`kibana.yml`](/deploy-manage/stack-settings.md) file. If you want to retrieve it from a different monitoring cluster, set `monitoring.ui.elasticsearch.hosts`. See [Monitoring settings](kibana://reference/configuration-reference/monitoring-settings.md).
2. Confirm that there is monitoring data available at that URL. It is stored in indices such as `.monitoring-kibana-*` and `.monitoring-es-*` or `metrics-kibana.stack_monitoring.*`, depending on which method is used to collect monitoring data. At a minimum, you must have monitoring data for the {{es}} production cluster. Once that data exists, {{kib}} can display monitoring data for other products in the cluster.
3. Set the time filter to “Last 1 hour”.  When monitoring data appears in your cluster, the page automatically refreshes with the monitoring summary.
4. If using {{agent}}, ensure that all integration assets have been installed in the monitoring cluster.

