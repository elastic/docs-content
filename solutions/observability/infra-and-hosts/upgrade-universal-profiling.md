---
navigation_title: Upgrade
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/profiling-upgrade.html
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: observability
---



# Upgrade Universal Profiling [profiling-upgrade]


This section is specific to upgrading Universal Profiling on {{ecloud}} or {{ece}}.

For self-hosted installations, refer to [Upgrade Universal Profiling in self-hosted installations](operate-universal-profiling-backend.md#profiling-self-managed-upgrade).


## Upgrade process [profiling-upgrade-process]

To upgrade from all versions earlier than 8.10 (GA), you need to:

1. Perform a stack upgrade in {{ecloud}}
2. Stop profiling data ingestion
3. Delete existing profiling data
4. Setup Universal Profiling from scratch
5. Start profiling data ingestion

To upgrade from version 8.10 or later, you need to:

1. Perform a stack upgrade in {{ecloud}}


### Perform a stack upgrade in the {{ecloud}} Console [profiling-upgrade-in-cloud]

To perform a stack upgrade in {{ecloud}}:

1. Locate the deployment you wish to upgrade in [{{ecloud}}](https://cloud.elastic.co).
2. Click the **Manage deployment** icon next to your deployment to open the deployment settings.
3. Find **Deployment version** on the right side of the page.
4. Click **Upgrade**, and choose the desired version.
5. Verify the upgrade was successful under **Your deployment → Activity** in the navigation menu.


### Stop profiling data ingestion [profiling-stop-ingestion]

During the Universal Profiling upgrade, you must stop data ingestion.

If you have an automated Universal Profiling Agent setup and control of the **full** fleet of machines where the Universal Profiling Agent is installed, deleting all Universal Profiling Agent deployments stops ingestion.

If you do not have direct control of all Universal Profiling Agent deployments, you can stop data ingestion by stopping incoming requests to the Integrations Server. To do this:

1. From the deployment settings, scroll down to the **Instances** section and locate all Integrations Server instances.
2. Click the three vertical dots in the upper-right corner of the Integrations Server card.
3. Select **Stop routing requests**.
4. Repeat this process for all Integrations Server instances.

::::{note}
When stopping incoming requests, Universal Profiling Agent replicas back off and retry connecting to the {{ecloud}} endpoint at increasing time intervals.
::::



### Delete existing profiling data [profiling-delete-data]

You can delete existing profiling data in Kibana:

1. If you’re upgrading from 8.9.0 or later, go to **Console** and execute the following snippet. (To open **Console**, find `Dev Tools` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).) If you’re upgrading from an earlier version, skip this step.

    ```console
    PUT /_cluster/settings
    {
      "persistent": {
        "xpack.profiling.templates.enabled": false
      }
    }
    ```

2. Open **Index Management** by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
3. Make sure you’re in the **Data Streams** tab, and search for `profiling-` in the search bar.
4. Select all resulting data streams, and click the **Delete data streams** button.
5. Switch to the **Indices** tab, enable **Include hidden indices**, and  search for `profiling-` in the search bar.
6. Select all resulting indices, click the **Manage indices** button, and select **Delete indices** from the drop-down menu.
7. Switch to the **Index Templates** tab, and  search for `profiling-` in the search bar.
8. Select all resulting index templates, and click the **Delete templates** button.
9. Switch to the **Component Templates** tab, and  search for `profiling-` in the search bar.
10. Select all resulting component templates, and click the **Delete component templates** button.
11. From the navigation menu, go to **Index Lifecycle Policies**, search for `profiling` in the search bar, and click the trash icon in the **Actions** column.

Verify that no ingestion is happening by reloading the **Data Streams** and **Indices** pages and ensuring that there are no data streams or indices with the `profiling-` prefix.


### Set up Universal Profiling from scratch [profiling-from-scratch]

Refer to [Configure data ingestion](get-started-with-universal-profiling.md#profiling-configure-data-ingestion) to set up Universal Profiling from scratch.


### Start profiling data ingestion [profiling-start-data-ingestion]

If you stopped ingesting data by stopping routing requests to the Integrations Server, re-enable traffic following the same steps but click **Start routing requests** instead of **Stop routing requests**.


### Verify the update succeeds [profiling-verify-upgrade-success]

Click any subheadings under Universal Profiling in the navigation menu. You should see incoming data.

If you see instructions on how to deploy the Universal Profiling Agent like in the [examples](get-started-with-universal-profiling.md#profiling-install-profiling-agent) from the [Get Started](get-started-with-universal-profiling.md) documentation, the agents did not reconnect to the Integrations Server replicas.

Refer to the [troubleshooting](/troubleshoot/observability/troubleshoot-your-universal-profiling-agent-deployment.md) documentation and the [Get Started](get-started-with-universal-profiling.md) documentation to investigate the issue.
