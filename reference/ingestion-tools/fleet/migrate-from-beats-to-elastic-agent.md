---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/migrate-beats-to-agent.html
---

# Migrate from Beats to Elastic Agent [migrate-beats-to-agent]

Learn how to replace your existing {{filebeat}} and {{metricbeat}} deployments with {{agent}}, our single agent for logs, metrics, security, and threat prevention.


## Why migrate to {{agent}}? [why-migrate-to-elastic-agent]

{{agent}} and {{beats}} provide similar functionality for log collection and host monitoring, but {{agent}} has some distinct advantages over {{beats}}.

* **Easier to deploy and manage.** Instead of deploying multiple {{beats}}, you deploy a single {{agent}}. The {{agent}} downloads, configures, and manages any underlying programs required to collect and parse your data.
* **Easier to configure.** You no longer have to define and manage separate configuration files for each Beat running on a host. Instead you define a single agent policy that specifies which integration settings to use, and the {{agent}} generates the configuration required by underlying programs, like {{beats}}.
* **Central management.** Unlike {{beats}}, which require you to set up your own automation strategy for upgrades and configuration management, {{agent}}s can be managed from a central location in {{kib}} called {{fleet}}. In {{fleet}}, you can view the status of running {{agent}}s, update agent policies and push them to your hosts, and even trigger binary upgrades.
* **Endpoint protection.** Probably the biggest advantage of using {{agent}} is that it enables you to protect your endpoints from security threats.


## Limitations and requirements [_limitations_and_requirements]

There are currently some limitations and requirements to be aware of before migrating to {{agent}}:

* **No support for configuring the {{beats}} internal queue.** Each Beat has an internal queue that stores events before batching and publishing them to the output. To improve data throughput, {{beats}} users can set [configuration options](beats://docs/reference/filebeat/configuring-internal-queue.md) to tune the performance of the internal queue. However, the endless fine tuning required to configure the queue is cumbersome and not always fruitful. Instead of expecting users to configure the internal queue, {{agent}} uses sensible defaults. This means you won’t be able to migrate internal queue configurations to {{agent}}.

For more information about {{agent}} limitations, see [*{{beats}} and {{agent}} capabilities*](/reference/ingestion-tools/fleet/index.md).


## Prepare for the migration [prepare-for-migration]

Before you begin:

1. Review your existing {{beats}} configurations and make a list of the integrations that are required. For example, if your existing implementation collects logs and metrics from Nginx, add Nginx to your list.
2. Make a note of any processors or custom configurations you want to migrate. Some of these customizations may no longer be needed or possible in {{agent}}.
3. Decide if it’s the right time to migrate to {{agent}}. Review the information under [*{{beats}} and {{agent}} capabilities*](/reference/ingestion-tools/fleet/index.md). Make sure the integrations you need are supported and Generally Available, and that the output and features you require are also supported.

If everything checks out, proceed to the next step. Otherwise, you might want to continue using {{beats}} and possibly deploy {{agent}} alongside {{beats}} to use features like endpoint protection.


## Set up {{fleet-server}} (self-managed deployments only) [_set_up_fleet_server_self_managed_deployments_only]

To use {{fleet}} for central management, a [{{fleet-server}}](/reference/ingestion-tools/fleet/fleet-server.md) must be running and accessible to your hosts.

If you’re using {{ecloud}}, you can skip this step because {{ecloud}} runs a hosted version of {{fleet-server}}.

Otherwise, follow the steps for self-managed deployments described in [Deploy {{fleet-server}} on-premises and {{es}} on Cloud](/reference/ingestion-tools/fleet/add-fleet-server-mixed.md) or [Deploy on-premises and self-managed](/reference/ingestion-tools/fleet/add-fleet-server-on-prem.md), depending on your deployment model, and then return to this page when you are done.


## Deploy {{agent}} to your hosts to collect logs and metrics [_deploy_agent_to_your_hosts_to_collect_logs_and_metrics]

To begin the migration, deploy an {{agent}} to a host where {{beats}} shippers are running. It’s recommended that you set up and test the migration in a development environment before deploying across your infrastructure.

You can continue to run {{beats}} alongside {{agent}} until you’re satisfied with the data its sending to {{es}}.

Read [*Install {{agent}}s*](/reference/ingestion-tools/fleet/install-elastic-agents.md) to learn how to deploy an {{agent}}. To save time, return to this page when the {{agent}} is deployed, healthy, and successfully sending data.

Here’s a high-level overview to help you understand the deployment process.

::::{admonition} Overview of the {{agent}} deployment process
During the deployment process you:

* **Create an agent policy.** An agent policy is similar to a configuration file, but unlike a regular configuration file, which needs to be maintained on many different host systems, you can configure and maintain the agent policy in a central location in {{fleet}} and apply it to multiple {{agent}}s.
* **Add integrations to the agent policy.** {{agent}} integrations provide a simple, unified way to collect data from popular apps and services, and protect systems from security threats. To define the agent policy, you add integrations for each service or system you want to monitor. For example, to collect logs and metrics from a system running Nginx, you might add the Nginx integration and the System integration.

    **What happens when you add an integration to an agent policy?** The assets for the integration, such as dashboards and ingest pipelines, get installed if they aren’t already. Plus the settings you specify for the integration, such as how to connect to the source system or locate logs, are added as an integration policy.

    For the example described earlier, you would have an agent policy that contains two integration policies: one for collecting Nginx logs and metrics, and another for collecting system logs and metrics.

* **Install {{agent}} on the host and enroll it in the agent policy.** When you enroll the {{agent}} in an agent policy, the agent gets added to {{fleet}}, where you can monitor and manage the agent.

::::


::::{tip}
It’s best to add one integration at a time and test it before adding more integrations to your agent policy. The System integration is a good way to get started if it’s supported on your OS.
::::



## View agent details and inspect the data streams [_view_agent_details_and_inspect_the_data_streams]

After deploying an {{agent}} to a host, view details about the agent and inspect the data streams it creates. To learn more about the benefits of using data streams, refer to [Data streams](/reference/ingestion-tools/fleet/data-streams.md).

1. On the **Agents** tab in **{{fleet}}**, confirm that the {{agent}} status is `Healthy`.

    :::{image} images/migration-agent-status-healthy01.png
    :alt: Screen showing that agent status is Healthy
    :class: screenshot
    :::

2. Click the host name to examine the {{agent}} details. This page shows the integrations that are currently installed, the policy the agent is enrolled in, and information about the host machine:

    :::{image} images/migration-agent-details01.png
    :alt: Screen showing that agent status is Healthy
    :class: screenshot
    :::

3. Go back to the main {{fleet}} page and click the **Data streams** tab. You should be able to see the data streams for various logs and metrics from the host. This is out-of-the-box without any extra configuration or dashboard creation:

    :::{image} images/migration-agent-data-streams01.png
    :alt: Screen showing data streams created by the {agent}
    :class: screenshot
    :::

4. Go to **Analytics > Discover** and examine the data streams. Note that documents indexed by {{agent}} match these patterns:

    * `logs-*`
    * `metrics-*`

    If {{beats}} are installed on the host machine, the data in {{es}} will be duplicated, with one set coming from {{beats}} and another from {{agent}} for the *same* data source.

    For example, filter on `filebeat-*` to see the data ingested by {{filebeat}}.

    :::{image} images/migration-event-from-filebeat.png
    :alt: Screen showing event from {filebeat}
    :class: screenshot
    :::

    Next, filter on `logs-*`. Notice that the document contains `data_stream.*` fields that come from logs ingested by the {{agent}}.

    :::{image} images/migration-event-from-agent.png
    :alt: Screen showing event from {agent}
    :class: screenshot
    :::

    ::::{note}
    This duplication is superfluous and will consume extra storage space on your {{es}} deployment. After you’ve finished migrating all your configuration settings to {{agent}}, you’ll remove {{beats}} to prevent redundant messages.
    ::::



## Add integrations to the agent policy [_add_integrations_to_the_agent_policy]

Now that you’ve deployed an {{agent}} to your host and it’s successfully sending data to {{es}}, add another integration. For guidance on which integrations you need, look at the list you created earlier when you [prepared for the migration](#prepare-for-migration).

For example, if the agent policy you created earlier includes the System integration, but you also want to monitor Nginx:

1. From the main menu in {{kib}}, click **Add integrations** and add the Nginx integration.

    :::{image} images/migration-add-nginx-integration.png
    :alt: Screen showing the Nginx integration
    :class: screenshot
    :::

2. Configure the integration, then apply it to the agent policy you used earlier. Make sure you expand collapsed sections to see all the settings like log paths.

    :::{image} images/migration-add-integration-policy.png
    :alt: Screen showing Nginx configuration
    :class: screenshot
    :::

    When you save and deploy your changes, the agent policy is updated to include a new integration policy for Nginx. All {{agent}}s enrolled in the agent policy get the updated policy, and the {{agent}} running on your host will begin collecting Nginx data.

    ::::{note}
    Integration policy names must be globally unique across all agent policies.
    ::::

3. Go back to **{{fleet}} > Agents** and verify that the agent status is still healthy. Click the host name to drill down into the agent details. From there, you can see the agent policy and integration policies that are applied.

    If the agent status is not Healthy, click **Logs** to view the agent log and troubleshoot the problem.

4. Go back to the main **{{fleet}}** page, and click **Data streams** to inspect the data streams and navigate to the pre-built dashboards installed with the integration.

Notice again that the data is duplicated because you still have {{beats}} running and sending data.


## Migrate processor configurations [_migrate_processor_configurations]

Processors enable you to filter and enhance the data before it’s sent to the output. Each processor receives an event, applies a defined action to the event, and returns the event. If you define a list of processors, they are executed in the order they are defined. Elastic provides a [rich set of processors](beats://docs/reference/filebeat/defining-processors.md) that are supported by all {{beats}} and by {{agent}}.

Prior to migrating from {{beats}}, you defined processors in the configuration file for each Beat. After migrating to {{agent}}, however, the {{beats}} configuration files are redundant. All configuration is policy-driven from {{fleet}} (or for advanced use cases, specified in a standalone agent policy). Any processors you defined previously in the {{beats}} configuration need to be added to an integration policy; they cannot be defined in the {{beats}} configuration.

::::{important}
Globally-defined processors are not currently supported by {{agent}}. You must define processors in each integration policy where they are required.
::::


To add processors to an integration policy:

1. In {{fleet}}, open the **Agent policies** tab and click the policy name to view its integration policies.
2. Click the name of the integration policy to edit it.
3. Click the down arrow next to enabled streams, and under **Advanced options**, add the processor definition. The processor will be applied to the data set where it’s defined.

    :::{image} images/migration-add-processor.png
    :alt: Screen showing how to add a processor to an integration policy
    :class: screenshot
    :::

    For example, the following processor adds geographically specific metadata to host events:

    ```yaml
    - add_host_metadata:
        cache.ttl: 5m
        geo:
          name: nyc-dc1-rack1
          location: 40.7128, -74.0060
          continent_name: North America
          country_iso_code: US
          region_name: New York
          region_iso_code: NY
          city_name: New York
    ```


In {{kib}}, look at the data again to confirm it contains the fields you expect.


## Preserve raw events [_preserve_raw_events]

In some cases, {{beats}} modules preserve the original, raw event, which consumes more storage space, but may be a requirement for compliance or forensic use cases.

In {{agent}}, this behavior is optional and disabled by default.

If you must preserve the raw event, edit the integration policy, and for each enabled data stream, click the **Preserve original event** toggle.

:::{image} images/migration-preserve-raw-event.png
:alt: Screen showing how to add a processor to an integration policy
:class: screenshot
:::

Do this for every data stream with a raw event you want to preserve.


## Migrate custom dashboards [_migrate_custom_dashboards]

Elastic integration packages provide many assets, such as pre-built dashboards, to make it easier for you to visualize your data. In some cases, however, you might have custom dashboards you want to migrate.

Because {{agent}} uses different data streams, the fields exported by an {{agent}} are slightly different from those exported {{beats}}. Any custom dashboards that you created for {{beats}} need to be modified or recreated to use the new fields.

You have a couple of options for migrating custom dashboards:

* (Recommended) Recreate the custom dashboards based on the new data streams.
* [Create index aliases to point to the new data streams](#create-index-aliases) and continue using custom dashboards.


### Create index aliases to point to data streams [create-index-aliases]

You may want to continue using your custom dashboards if the dashboards installed with an integration are not adequate. To do this, use index aliases to feed data streams into your existing custom dashboards.

For example, custom dashboards that point to `filebeat-` or `metricbeat-` can be aliased to use the equivalent data streams, `logs-` and `metrics-`.

To use aliases:

1. Add a `filebeat` alias to the `logs-` data stream. For example:

    ```json
    POST _aliases
    {
      "actions": [
        {
          "add": {
            "index": "logs-*",
            "alias": "filebeat-"
          }
        }

     ]
    }
    ```

2. Add a `metribeat` alias to the `metrics-` data stream.

    ```json
    POST _aliases
    {
      "actions": [
        {
          "add": {
            "index": "metrics-*",
            "alias": "metricbeat-"
          }
        }
     ]
    }
    ```


::::{important}
These aliases must be added to both the index template and existing indices.
::::


Note that custom dashboards will show duplicated data until you remove {{beats}} from your hosts.

For more information, see the [Aliases documentation](/manage-data/data-store/aliases.md).


## Migrate index lifecycle policies [_migrate_index_lifecycle_policies]

{{ilm-cap}} ({{ilm}}) policies in {{es}} enable you to manage indices according to your performance, resiliency, and retention requirements. To learn more about {{ilm}}, refer to the [{{ilm}} documentation](/manage-data/lifecycle/index-lifecycle-management.md).

{{ilm}} is configured by default in {{beats}} (version 7.0 and later) and in {{agent}} (all versions). To view the index lifecycle policies defined in {{es}}, go to **Management > Index Lifecycle Policies**.

:::{image} images/migration-index-lifecycle-policies.png
:alt: Screen showing how to add a processor to an integration policy
:class: screenshot
:::

If you used {{ilm}} with {{beats}}, you’ll see index lifecycle policies like **filebeat** and **metricbeat** in the list. After migrating to {{agent}}, you’ll see polices named **logs** and **metrics**, which encapsulate the {{ilm}} policies for all `logs-*` and `metrics-*` index templates.

When you migrate from {{beats}} to {{agent}}, you have a couple of options for migrating index policy settings:

* **Modify the newly created index lifecycle policies (recommended).** As mentioned earlier, {{ilm}} is enabled by default when the {{agent}} is installed. Index lifecycle policies are created and added to the index templates for data streams created by integrations.

    If you have existing index lifecycle policies for {{beats}}, it’s highly recommended that you modify the lifecycle policies for {{agent}} to match your previous policy. To do this:

    1. In {{kib}}, go to **{{stack-manage-app}} > Index Lifecycle Policies** and search for a {{beats}} policy, for example, **filebeat**. Under **Linked indices**, notice you can view indices linked to the policy. Click the policy name to see the settings.
    2. Click the **logs** policy and, if necessary, edit the settings to match the old policy.
    3. Under **Index Lifecycle Policies**, search for another {{beats}} policy, for example, **metricbeat**.
    4. Click the **metrics** policy and edit the settings to match the old policy.

    Optionally delete the {{beats}} index lifecycle policies when they are no longer used by an index.

* **Keep the {{beats}} policy and apply it to the index templates created for data streams.** To preserve an existing policy, modify it, as needed, and apply it to all the index templates created for data streams:

    1. Under **Index Lifecycle Policies**, find the {{beats}} policy, for example, **filebeat**.
    2. In the **Actions** column, click the **Add policy to index template** icon.
    3. Under **Index template**, choose a data stream index template, then add the policy.
    4. Repeat this procedure, as required, to apply the policy to other data stream index templates.


::::{admonition} What if you’re not using {{ilm}} with {{beats}}?
You can begin to use {{ilm}} now with {{agent}}. Under **Index lifecycle policies**, click the policy name and edit the settings to meet your requirements.

::::



## Remove {{beats}} from your host [_remove_beats_from_your_host]

Any installed {{beats}} shippers will continue to work until you remove them. This allows you to roll out the migration in stages. You will continue to see duplicated data until you remove {{beats}}.

When you’re satisfied with your {{agent}} deployment, remove {{beats}} from your hosts. All the data collected before installing the {{agent}} will still be available in {{es}} until you delete the data or it’s removed according to the data retention policies you’ve specified for {{ilm}}.

To remove {{beats}} from your host:

1. Stop the service by using the correct command for your system.
2. (Optional) Back up your {{beats}} configuration files in case you need to refer to them in the future.
3. Delete the {{beats}} installation directory. If necessary, stop any orphan processes that are running after you stopped the service.
4. If you added firewall rules to allow {{beats}} to communicate on your network, remove them.
5. After you’ve removed all {{beats}}, revoke any API keys or remove privileges for any {{beats}} users created to send data to {{es}}.


