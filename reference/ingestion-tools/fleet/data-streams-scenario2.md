---
navigation_title: "Scenario 2"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/data-streams-scenario2.html
---

# Scenario 2: Apply an ILM policy to specific data streams generated from Fleet integrations across all namespaces [data-streams-scenario2]


Mappings and settings for data streams can be customized through the creation of `*@custom` component templates, which are referenced by the index templates created by the {{es}} apm-data plugin. The easiest way to configure a custom index lifecycle policy per data stream is to edit this template.

This tutorial explains how to apply a custom index lifecycle policy to the `logs-system.auth` data stream.


## Step 1: Create an index lifecycle policy [data-streams-scenario2-step1]

1. To open **Lifecycle Policies**, find **Stack Management** in the main menu or use the [global search field](/get-started/the-stack.md#kibana-navigation-search).
2. Click **Create policy**.

Name your new policy. For this tutorial, you can use `my-ilm-policy`. Customize the policy to your liking, and when you’re done, click **Save policy**.


## Step 2: View index templates [data-streams-scenario2-step2]

The **Index Templates** view in {{kib}} shows you all of the index templates available to automatically apply settings, mappings, and aliases to indices:

1. To open **Index Management**, find **Stack Management** in the main menu or use the [global search field](/get-started/the-stack.md#kibana-navigation-search).
2. Select **Index Templates**.
3. Search for `system` to see all index templates associated with the System integration.
4. Select the index template that matches the data stream for which you want to set up an ILM policy. For this example, you can select the `logs-system.auth` index template.

    :::{image} images/index-template-system-auth.png
    :alt: List of component templates available for the logs-system.auth index template
    :class: screenshot
    :::

5. In the **Summary**, select `logs-system.auth@custom` from the list to view the component template properties.
6. For a newly added integration, the component template won’t exist yet. Select **Create component template** to create it. If the component template already exists, click **Manage** to update it.

    1. On the **Logistics** page, keep all defaults and click **Next**.
    2. On the **Index settings** page, in the **Index settings** field, specify the ILM policy that you created. For example:

        ```json
        {
            "index": {
                "lifecycle": {
                    "name": "my-ilm-policy"
                }
            }
        }
        ```

    3. Click **Next**.
    4. For both the **Mappings** and **Aliases** pages, keep all defaults and click **Next**.
    5. Finally, on the **Review** page, review the summary and request. If everything looks good, select **Create component template**.

        :::{image} images/review-component-template02.png
        :alt: Review details for the new component template
        :class: screenshot
        :::



## Step 3: Roll over the data streams (optional) [data-streams-scenario2-step3]

To confirm that the index template is using the `logs@custom` component template with your custom ILM policy:

1. Reopen the **Index Management** page and open the **Component Templates** tab.
2. Search for `system` and select the `logs-system.auth@custom` component template.
3. The **Summary** shows the list of all data streams that use the component template, and the **Settings** view shows your newly configured ILM policy.

New ILM policies only take effect when new indices are created, so you either must wait for a rollover to occur (usually after 30 days or when the index size reaches 50 GB), or force a rollover of the data stream using the {{ref}}/indices-rollover-index.html[{{es}} rollover API:

```bash
POST /logs-system.auth/_rollover/
```


## Step 4: Repeat these steps for other data streams [data-streams-scenario2-step4]

You’ve now applied a custom index lifecycle policy to the `logs-system.auth` data stream in the `System` integration. Repeat these steps for any other data streams for which you’d like to configure a custom ILM policy.
