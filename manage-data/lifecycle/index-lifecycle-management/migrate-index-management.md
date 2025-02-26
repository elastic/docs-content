---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-migrate-index-management.html
  - https://www.elastic.co/guide/en/cloud/current/ec-configure-index-management.html
  - https://www.elastic.co/guide/en/cloud/current/ec-migrate-index-management.html
applies_to:
  stack: ga
  serverless: ga
---

# Migrate to index lifecycle management

::::{important}
Index curation is deprecated. Any deployments using index curation are prompted to migrate to ILM.
::::

The index lifecycle management (ILM) feature of the {{stack}} provides an integrated and streamlined way to manage time-based data, making it easier to follow best practices for managing your indices. Compared to index curation, migrating to ILM gives you more fine-grained control over the lifecycle of each index.

For existing hot-warm deployments that are currently using index curation, there are a couple of options for migrating to index lifecycle management (ILM). You can:

* Use the migration process in the console to change an existing deployment to ILM.
* Take a snapshot and restore your data to a new Elastic Stack deployment that has ILM enabled.

To configure ILM Migration in the console:

::::{tab-set}

:::{tab-item} {{ech}}
1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From the **Deployments** page, select your deployment.

    On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. Near the top of the deployment overview, you should get a message to migrate from index curation to index lifecycle management (ILM) along with a **Start migration** button.
4. Select which index curation pattern you wish to migrate.
5. Set the ILM policy name for each data view (formerly *index pattern*).
:::

:::{tab-item} Elastic Cloud Enterprise
1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. From the **Deployments** page, select your deployment.

    On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. Near the top of the deployment overview, you should get a message to migrate from index curation to index lifecycle management (ILM) along with a **Start migration** button.
4. Select which index curation pattern you wish to migrate.
5. Set the ILM policy name for each data view (formerly *index pattern*).
:::

::::

::::{note}
Beginning with Elastic Stack version 8.0, Kibana *index patterns* have been renamed to *data views*. To learn more, check the Kibana [What’s new in 8.0](https://www.elastic.co/guide/en/kibana/8.0/whats-new.html#index-pattern-rename) page.
::::

1. Set the shard allocation attribute for the data view.

    * You can set different node attributes per data view to allow for more in-depth configuration in Kibana, or
    * You may choose to add one node attribute that applies to all data views.
    * If you do not wish to migrate a certain data view to ILM, you can deselect the checkbox in the associated row.
    * You may also wish to migrate to ILM without carrying over any of your current data views by deselecting all patterns. This means that those data views will no longer be curated, and you will have the option to set up new ILM policies in Kibana.

2. Select **Migrate**.

After you get the notification that confirms that migration was completed successfully, you can view your ILM policies in Kibana.

