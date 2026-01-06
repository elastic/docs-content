---
navigation_title: Osquery manager integration
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/manage-osquery-integration.html
applies_to:
  stack: preview all
  serverless:
    security: preview all
products:
  - id: kibana
---

# Manage the integration [manage-osquery-integration]


## System requirements [_system_requirements]

* [{{fleet}}](/reference/fleet/index.md) is enabled on your cluster, and one or more [{{agents}}](/reference/fleet/install-elastic-agents.md) is enrolled.
* The [Osquery Manager](https://docs.elastic.co/en/integrations/osquery_manager) integration has been added and configured for an agent policy through {{fleet}}. This integration supports x64 architecture on Windows, MacOS, and Linux platforms, and ARM64 architecture on Linux.

::::{note}
* The original [Filebeat Osquery module](beats://reference/filebeat/filebeat-module-osquery.md) and the [Osquery](https://docs.elastic.co/en/integrations/osquery) integration collect logs from self-managed Osquery deployments. The **Osquery Manager** integration manages Osquery deployments and supports running and scheduling queries from {{kib}}.
* **Osquery Manager** cannot be integrated with an {{agent}} in standalone mode.

::::



## Customize Osquery sub-feature privileges [_customize_osquery_sub_feature_privileges]

Depending on your [subscription level](https://www.elastic.co/pricing) or  [{{serverless-short}} project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md), you can further customize the sub-feature privileges for **Osquery Manager**. These include options to grant specific access for running live queries, running saved queries, saving queries, and scheduling packs. For example, you can create roles for users who can only run live or saved queries, but who cannot save or schedule queries. This is useful for teams who need in-depth and detailed control.


## Customize Osquery configuration [osquery-custom-config]

By default, all Osquery Manager integrations share the same Osquery configuration. However, you can customize how Osquery is configured by editing the Osquery Manager integration for each agent policy you want to adjust. The custom configuration is then applied to all agents in the policy. This powerful feature allows you to configure [File Integrity Monitoring](https://osquery.readthedocs.io/en/stable/deployment/file-integrity-monitoring), [Process auditing](https://osquery.readthedocs.io/en/stable/deployment/process-auditing), and [others](https://osquery.readthedocs.io/en/stable/deployment/configuration/#configuration-specification).

::::{important}
* Take caution when editing this configuration. The changes you make are distributed to all agents in the policy.
* Take caution when editing `packs` using the Advanced **Osquery config** field. Any changes you make to `packs` from this field are not reflected in the UI on the Osquery **Packs** page in {{kib}}, however, these changes are deployed to agents in the policy. While this allows you to use advanced Osquery functionality like pack discovery queries, you do lose the ability to manage packs defined this way from the Osquery **Packs** page.

::::


1. Go to **Fleet** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then open the **Agent policies** tab.
2. Click the name of the agent policy where you want to adjust the Osquery configuration. The configuration changes you make only apply to the policy you select.
3. Click the name of the **Osquery Manager** integration, or add the integration first if the agent policy does not yet have it.
4. From the **Edit Osquery Manager integration** page, expand the **Advanced** section.
5. Edit the **Osquery config** JSON field to apply your preferred Osquery configuration. Note the following:

    * The field may already have content if you’ve scheduled packs for this agent policy. To keep these packs scheduled, do not remove the `packs` section. The `shard` field value is the percentage of agents in the policy using the pack.
    * Refer to the [Osquery documentation](https://osquery.readthedocs.io/en/stable/) for configuration options.
    * Some fields are protected and cannot be set. A warning is displayed with details about which fields should be removed.
    * (Optional) To load a full configuration file, drag and drop an Osquery `.conf` file into the area at the bottom of the page.

6. Click **Save integration** to apply the custom configuration to all agents in the policy.

    As an example, the following configuration disables two tables.

    ```ts
    {
       "options": {
          "disable_tables":"file,process_envs"
       }
    }
    ```



### Enabling the `curl` table [enable-curl-table]

By default, the [curl table](https://osquery.io/schema/#curl) is disabled. If preferred, you can enable it using the Advanced **Osquery config**.

**Why is the `curl` table disabled?**

When you query the [curl table](https://osquery.io/schema/#curl), this results in an HTTP request. The query results include the response to the request. As a simple example, if you run the query `SELECT * FROM curl WHERE url='https://www.elastic.co/';`, the `result` field contains the webpage content.

This table can be misused in some environments, for example, when used to issue HTTP requests to an AWS metadata service or to services on your internal network.

Out of an abundance of caution, we have opted to disable access to this table by default. However, if you need access to the table for your own monitoring purposes, you can enable it as needed.

**How to enable the `curl` table:**

For each agent policy where you want to allow `curl` table queries, edit the Osquery Manager integration to add the following Advanced **Osquery config**:

```ts
{
   "options": {
      "enable_tables":"curl"
   }
}
```


## Upgrade Osquery versions [_upgrade_osquery_versions]

The [Osquery version](https://github.com/osquery/osquery/releases) available on an {{agent}} is associated to the version of Osquery Beat on the Agent. To get the latest version of Osquery Beat, [upgrade your {{agent}}](/reference/fleet/upgrade-elastic-agent.md).


## Debug issues [_debug_issues]

If you encounter issues with **Osquery Manager**, find the relevant logs for {{agent}} and Osquerybeat in the agent directory. Refer to the [Fleet Installation layout](/reference/fleet/installation-layout.md) to find the log file location for your OS.

```ts
../data/elastic-agent-*/logs/elastic-agent-json.log-*
../data/elastic-agent-*/logs/default/osquerybeat-json.log
```

To get more details in the logs, change the agent logging level to debug:

1. Go to **{{fleet}}** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the agent that you want to debug.
3. On the **Logs** tab, change the **Agent logging level** to **debug**, and then click **Apply changes**.

    `agent.logging.level` is updated in `fleet.yml`, and the logging level is changed to `debug`.
