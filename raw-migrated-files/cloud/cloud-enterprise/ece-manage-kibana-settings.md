# Add Kibana user settings [ece-manage-kibana-settings]

Elastic Cloud Enterprise supports most of the standard Kibana and X-Pack settings. Through a YAML editor in the console, you can append Kibana properties to the `kibana.yml` file. Your changes to the configuration file are read on startup.

::::{important}
Be aware that some settings that could break your cluster if set incorrectly and that the syntax might change between major versions. Before upgrading, be sure to review the full list of the [latest Kibana settings and syntax](asciidocalypse://docs/kibana/docs/reference/configuration-reference/general-settings.md).
::::


To change Kibana settings:

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From your deployment menu, go to the **Edit** page.
4. In the **Kibana** section, select **Edit user settings**. For deployments with existing user settings, you may have to expand the **Edit kibana.yml** caret instead.
5. Update the user settings.
6. Select **Save changes**.

Saving your changes initiates a configuration plan change that restarts Kibana automatically for you.

::::{note}
If a setting is not supported by Elastic Cloud Enterprise, you will get an error message when you try to save. We suggest changing one setting with each save, so you know which one is not supported.
::::


::::{tip}
If you have a license from 2018 or earlier, you might receive a warning that your cluster license is about to expire. Don’t panic, it isn’t really. Elastic Cloud Enterprise manages the cluster licenses so that you don’t have to. In rare cases, such as when a cluster is overloaded, it can take longer for Elastic Cloud Enterprise to reapply the cluster license. If you have a license from 2019 and later, you’ll receive a warning only when your full platform license is about to expire, which you’ll need to renew.
::::



## Example: Increase the timeout for creating reports [ece_example_increase_the_timeout_for_creating_reports]

When creating reports, you can adjust the number of milliseconds before a worker times out. This is particularly helpful for instances with a slow or heavy load.

```sh
xpack.reporting.queue.timeout: "150000"
```


## Example: Change the truncation point for CSV exports [ece_example_change_the_truncation_point_for_csv_exports]

If large exports are causing performance or storage issues, you can increase the number of bytes before the report truncates from the default 250 MB. For stack versions before 8.10, the default is 10 MB.

```sh
xpack.reporting.csv.maxSizeBytes: "20971520"
```


