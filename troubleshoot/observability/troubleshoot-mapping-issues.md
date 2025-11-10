---
navigation_title: Uptime
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/troubleshoot-uptime-mapping-issues.html
applies_to:
  stack: deprecated 8.15.0
products:
  - id: observability
---

# Troubleshoot Uptime mapping issues [troubleshoot-uptime-mapping-issues]


## Mapping issues [_mapping_issues] 

There are situations in which {{heartbeat}} data can be indexed without the correct mappings applied. These situations cannot occur with the {{elastic-agent}} configured via {{fleet}}, only with standalone {{heartbeat}} or {{elastic-agent}} running in standalone mode. This can occur when the underlying `heartbeat-VERSION` {{ilm-init}} alias is deleted manually or when {{heartbeat}} writes data through an intermediary such as {{ls}} without the `setup` command being run. When running {{elastic-agent}} in standalone mode this can happen if manually setup data streams have incorrect mappings.

To fix this problem, you typically need to remove your {{heartbeat}} indices and data streams. Then you must create new ones with the appropriate mappings installed. To achieve this, follow the steps below.


### Stop your {{heartbeat}}/{{elastic-agent}} instances [_stop_your_heartbeatelastic_agent_instances] 

It is necessary to stop all {{heartbeat}}/{{elastic-agent}} instances that are targeting the cluster, so they will not write to or re-create indices prematurely.


### Delete your {{heartbeat}} indices / {{elastic-agent}} data streams [_delete_your_heartbeat_indices_elastic_agent_data_streams] 

To ensure the mapping is applied to all {{heartbeat}} data going forward, delete all the {{heartbeat}} indices that match the pattern the {{uptime-app}} will use.

There are multiple ways to achieve this. You can read about performing this using the [Index Management UI](/manage-data/data-store/index-basics.md#index-management) or with the [Delete index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-delete).

If using {{elastic-agent}} you will want to fix any issues with custom data stream mappings. We encourage the use of {{fleet}} to eliminate this issue.


### If using {{heartbeat}}, perform {{heartbeat}} setup [_if_using_heartbeat_perform_heartbeat_setup] 

The below command will cause {{heartbeat}} to perform its setup processes and recreate the index template properly.

```bash
./heartbeat setup -e
```

For more information on how to use this command, or if you’re using DEB, RPM, or Windows, see the [{{heartbeat}} quickstart guide](beats://reference/heartbeat/heartbeat-installation-configuration.md).

This command performs the necessary startup tasks and ensures that your indices have the appropriate mapping going forward.


### Run {{heartbeat}}/{{elastic-agent}} again [_run_heartbeatelastic_agent_again] 

Now, when you run {{heartbeat}}/{{elastic-agent}}, your data will be indexed with the appropriate mappings. When the {{uptime-app}} attempts to fetch your data, it should be able to render without issues.

