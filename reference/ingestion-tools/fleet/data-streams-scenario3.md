---
navigation_title: "Scenario 3"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/data-streams-scenario3.html
---

# Scenario 3: Apply an ILM policy with integrations using multiple namespaces [data-streams-scenario3]


In this scenario, you have {{agent}}s collecting system metrics with the System integration in two environments—​one with the namespace `development`, and one with `production`.

**Goal:** Customize the {{ilm-init}} policy for the `system.network` data stream in the `production` namespace. Specifically, apply the built-in `90-days-default` {{ilm-init}} policy so that data is deleted after 90 days.

::::{note}
* This scenario involves cloning an index template. We strongly recommend repeating this procedure on every minor {{stack}} upgrade in order to avoid missing any possible changes to the structure of the managed index template(s) that are shipped with integrations.
* If you cloned an index template to customize the data retention policy on an {{es}} version prior to 8.13, you must update the index template in the clone to use the `ecs@mappings` component template on {{es}} version 8.13 or later. See [Update index template cloned before {{es}} 8.13](#data-streams-pipeline-update-cloned-template-before-8.13) for the step-by-step instructions.

::::



## Step 1: View data streams [data-streams-ilm-one]

The **Data Streams** view in {{kib}} shows you the data streams, index templates, and {{ilm-init}} policies associated with a given integration.

1. Navigate to **{{stack-manage-app}}** > **Index Management** > **Data Streams**.
2. Search for `system` to see all data streams associated with the System integration.
3. Select the `metrics-system.network-{{namespace}}` data stream to view its associated index template and {{ilm-init}} policy. As you can see, the data stream follows the [Data stream naming scheme](/reference/ingestion-tools/fleet/data-streams.md#data-streams-naming-scheme) and starts with its type, `metrics-`.

    :::{image} images/data-stream-info.png
    :alt: Data streams info
    :class: screenshot
    :::



## Step 2: Create a component template [data-streams-ilm-two]

For your changes to continue to be applied in future versions, you must put all custom index settings into a component template. The component template must follow the data stream naming scheme, and end with `@custom`:

```text
<type>-<dataset>-<namespace>@custom
```

For example, to create custom index settings for the `system.network` data stream with a namespace of `production`, the component template name would be:

```text
metrics-system.network-production@custom
```

1. Navigate to **{{stack-manage-app}}** > **Index Management** > **Component Templates**
2. Click **Create component template**.
3. Use the template above to set the name—​in this case, `metrics-system.network-production@custom`. Click **Next**.
4. Under **Index settings**, set the {{ilm-init}} policy name under the `lifecycle.name` key:

    ```json
    {
      "lifecycle": {
        "name": "90-days-default"
      }
    }
    ```

5. Continue to **Review** and ensure your request looks similar to the image below. If it does, click **Create component template**.

    :::{image} images/create-component-template.png
    :alt: Create component template
    :class: screenshot
    :::



## Step 3: Clone and modify the existing index template [data-streams-ilm-three]

Now that you’ve created a component template, you need to create an index template to apply the changes to the correct data stream. The easiest way to do this is to duplicate and modify the integration’s existing index template.

::::{warning}
Please note the following: * When duplicating the index template, do not change or remove any managed properties. This may result in problems when upgrading. Cloning the index template of an integration package involves some risk as any changes made to the original index template when it is upgraded will not be propagated to the cloned version. * These steps assume that you want to have a namespace specific ILM policy, which requires index template cloning. Cloning the index template of an integration package involves some risk because any changes made to the original index template as part of package upgrades are not propagated to the cloned version. See [Cloning the index template of an integration package](/reference/ingestion-tools/fleet/integrations-assets-best-practices.md#assets-restrictions-cloning-index-template) for details.

+ If you want to change the ILM Policy, the number of shards, or other settings for the datastreams of one or more integrations, but **the changes do not need to be specific to a given namespace**, it’s strongly recommended to use a `@custom` component template, as described in [Scenario 1](/reference/ingestion-tools/fleet/data-streams-scenario1.md) and [Scenario 2](/reference/ingestion-tools/fleet/data-streams-scenario2.md), so as to avoid the problems mentioned above. See the [ILM](/reference/ingestion-tools/fleet/data-streams.md#data-streams-ilm) section for details.

::::


1. Navigate to **{{stack-manage-app}}** > **Index Management** > **Index Templates**.
2. Find the index template you want to clone. The index template will have the `<type>` and `<dataset>` in its name, but not the `<namespace>`. In this case, it’s `metrics-system.network`.
3. Select **Actions** > **Clone**.
4. Set the name of the new index template to `metrics-system.network-production`.
5. Change the index pattern to include a namespace—​in this case, `metrics-system.network-production*`. This ensures the previously created component template is only applied to the `production` namespace.
6. Set the priority to `250`. This ensures that the new index template takes precedence over other index templates that match the index pattern.
7. Under **Component templates**, search for and add the component template created in the previous step. To ensure your namespace-specific settings are applied over other custom settings, the new template should be added below the existing `@custom` template.
8. Create the index template.

:::{image} images/create-index-template.png
:alt: Create index template
:class: screenshot
:::


## Step 4: Roll over the data stream (optional) [data-streams-ilm-four]

To confirm that the data stream is now using the new index template and {{ilm-init}} policy, you can either repeat Step 1, or navigate to **{{dev-tools-app}}** and run the following:

```bash
GET /_data_stream/metrics-system.network-production <1>
```

1. The name of the data stream we’ve been hacking on


The result should include the following:

```json
{
  "data_streams" : [
    {
      ...
      "template" : "metrics-system.network-production", <1>
      "ilm_policy" : "90-days-default", <2>
      ...
    }
  ]
}
```

1. The name of the custom index template created in step three
2. The name of the {{ilm-init}} policy applied to the new component template in step two


New {{ilm-init}} policies only take effect when new indices are created, so you either must wait for a rollover to occur (usually after 30 days or when the index size reaches 50 GB), or force a rollover using the [{{es}} rollover API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-rollover):

```bash
POST /metrics-system.network-production/_rollover/
```


## Update index template cloned before {{es}} 8.13 [data-streams-pipeline-update-cloned-template-before-8.13]

If you cloned an index template to customize the data retention policy on an {{es}} version prior to 8.13, you must update the index cloned index template to add the `ecs@mappings` component template on {{es}} version 8.13 or later.

To update the cloned index template:

1. Navigate to **{{stack-manage-app}}** > **Index Management** > **Index Templates**.
2. Find the index template you cloned. The index template will have the `<type>` and `<dataset>` in its name.
3. Select **Manage** > **Edit**.
4. Select **(2) Component templates**
5. In the **Search component templates** field, search for `ecs@mappings`.
6. Click on the **+ (plus)** icon to add the `ecs@mappings` component template.
7. Move the `ecs@mappings` component template right below the `@package` component template.
8. Save the index template.

Roll over the data stream to apply the changes.
