---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/filter-agent-list-by-tags.html
---

# Add tags to filter the Agents list [filter-agent-list-by-tags]

You can add tags to {{agent}} during or after enrollment, then use the tags to filter the Agents list shown in {{fleet}}.

Tags are useful for capturing information that is specific to the installation environment, such machine type, location, operating system, environment, and so on. Tags can be any arbitrary information that will help you filter and perform operations on {{agent}}s with the same attributes.

To filter the Agents list by tag, in {{kib}}, go to **{{fleet}} > Agents** and click **Tags**. Select the tags to filter on. The tags are also available in the KQL field for autocompletion.

:::{image} images/agent-tags.png
:alt: Agents list filtered to show agents with the staging tag
:class: screenshot
:::

If you haven’t added tags to any {{agent}}s yet, the list will be empty.


## Add, remove, rename, or delete tags in {{fleet}} [add-tags-in-fleet]

You can use {{fleet}} to add, remove, or rename tags applied to one or more {{agent}}s.

Want to add tags when enrolling from a host instead? See [Add tags during agent enrollment](#add-tags-at-enrollment).

To manage tags in {{fleet}}:

1. On the **Agents** tab, select one or more agents.
2. From the **Actions** menu, click **Add / remove tags**.

    :::{image} images/add-remove-tags.png
    :alt: Screenshot of add / remove tags menu
    :class: screenshot
    :::

    ::::{tip}
    Make sure you use the correct **Actions** menu. To manage tags for a single agent, click the ellipsis button under the **Actions** column. To manage tags for multiple agents, click the **Actions** button to open the bulk actions menu.
    ::::

3. In the tags menu, perform an action:

    | To…​ | Do this…​ |
    | --- | --- |
    | Create a new tag | Type the tag name and click **Create new tag…​**. Notice the tag name hasa check mark to show that the tag has been added to the selected agents. |
    | Rename a tag | Hover over the tag name and click the ellipsis button. Type a new name and press Enter.The tag will be renamed in all agents that use it, even agents that are notselected. |
    | Delete a tag | Hover over the tag name and click the ellipsis button. Click **Delete tag**.The tag will be deleted from all agents, even agents that are not selected. |
    | Add or remove a tag from an agent | Click the tag name to add or clear the check mark. In the **Tags** column,notice that the tags are added or removed. Note that the menu only showstags that are common to all selected agents. |



## Add tags during agent enrollment [add-tags-at-enrollment]

When you install or enroll {{agent}} in {{fleet}}, you can specify a comma-separated list of tags to apply to the agent, then use the tags to filter the Agents list shown in {{fleet}}.

The following command applies the `macOS` and `staging` tags during installation:

```shell
sudo ./elastic-agent install \
  --url=<Fleet Server host URL> \
  --enrollment-token=<enrollment token> \
  --tag macOS,staging
```

For the full command synopsis, refer to [elastic-agent install](/reference/ingestion-tools/fleet/agent-command-reference.md#elastic-agent-install-command) and [elastic-agent enroll](/reference/ingestion-tools/fleet/agent-command-reference.md#elastic-agent-enroll-command).

The following command applies the `docker` and `dev` tags to {{agent}} running in a Docker container:

```yaml
docker run \
  --env FLEET_ENROLL=1 \
  --env FLEET_URL=<Fleet Server host URL> \
  --env FLEET_ENROLLMENT_TOKEN=<enrollment token> \
  --env ELASTIC_AGENT_TAGS=docker,dev
  --rm docker.elastic.co/elastic-agent/elastic-agent:9.0.0-beta1
```

For more information about running on containers, refer to the guides under [Install {{agent}}s in a containerized environment](/reference/ingestion-tools/fleet/install-elastic-agents-in-containers.md).
