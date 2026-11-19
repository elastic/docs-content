---
navigation_title: Add and manage agent tags
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/filter-agent-list-by-tags.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Add and manage {{agent}} tags [filter-agent-list-by-tags]

You can add tags to {{agent}} during enrollment or later in {{fleet}}, then use the tags to filter the Agents list shown in {{fleet}}.

Tags are useful for capturing information that is specific to the installation environment, such as machine type, location, operating system, or environment. Tags can be any information that helps you filter and perform operations on {{agent}}s with the same attributes.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` You can also add the tags to the data that {{agent}}s collect, so you can filter it by tag in Discover, dashboards, alerting rules, and detection rules. Refer to [Include agent tags in events](/reference/fleet/agent-policy.md#agent-policy-include-agent-tags).

:::{note}
You can't add, remove, rename, or delete tags in {{fleet}} for agents enrolled in a [hosted agent policy](/reference/fleet/agent-policy.md#agent-policy-types), such as the {{ecloud}} agent policy.
:::

## Add, remove, rename, or delete tags in {{fleet}} [add-tags-in-fleet]

To manage tags in {{fleet}}:

1. Find **Fleet** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). On the **Agents** tab, select one or more agents.
2. Select **Actions** → **Add / remove tags**.

    :::{image} images/add-remove-tags.png
    :alt: Actions menu with the Add / remove tags option and the tag list
    :screenshot:
    :::

    ::::{tip}
    To manage tags for a single agent, you don't need to select it first. In the agent's row, select the actions menu {icon}`ellipsis`, then select **Add / remove tags**.
    ::::

3. The tag list shows all tags in {{fleet}}. The tags that the agents already have are checked. If you selected several agents, only the tags they all share are checked. Do one of the following:

    | Action | Steps |
    | --- | --- |
    | Create a tag | In the search field, enter the tag name, then select **Create a new tag "<tag name>"**. The new tag is checked, which shows that it's added to the selected agents. |
    | Add or remove a tag | Select a tag to add it to or remove it from the selected agents. The tags shown with each agent's host name in the **Host** column update to match. |
    | Rename a tag | Hover over the tag and select the tag options icon {icon}`ellipsis`. Enter a new name and press **Enter**. {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` You can also select **Save**. The tag is renamed for all agents that have it, including agents that aren't selected. |
    | Delete a tag | Hover over the tag, select the tag options icon {icon}`ellipsis`, then select **Delete tag**. The tag is removed from all agents that have it, including agents that aren't selected. |


## Add tags during agent enrollment [add-tags-at-enrollment]

When you install or enroll {{agent}} in {{fleet}}, use the `--tag` option to specify a comma-separated list of tags to apply to the agent.

The following command applies the `macOS` and `staging` tags during installation:

```shell
sudo ./elastic-agent install \
  --url=<Fleet Server host URL> \
  --enrollment-token=<enrollment token> \
  --tag macOS,staging
```

For all command options, refer to [elastic-agent install](/reference/fleet/agent-command-reference.md#elastic-agent-install-command) and [elastic-agent enroll](/reference/fleet/agent-command-reference.md#elastic-agent-enroll-command).

When you run {{agent}} in a container, set the [`ELASTIC_AGENT_TAGS`](/reference/fleet/agent-environment-variables.md#env-enroll-elastic-agent-tag) environment variable to a comma-separated list of tags. For example, the following command applies the `docker` and `dev` tags to {{agent}} running in a Docker container:

```shell subs=true
docker run \
  --env FLEET_ENROLL=1 \
  --env FLEET_URL=<Fleet Server host URL> \
  --env FLEET_ENROLLMENT_TOKEN=<enrollment token> \
  --env ELASTIC_AGENT_TAGS=docker,dev \
  --rm docker.elastic.co/elastic-agent/elastic-agent:{{version.stack}}
```

For more information about running {{agent}} in containers, refer to the guides under [Install {{agent}}s in a containerized environment](/reference/fleet/install-elastic-agents-in-containers.md).


## Filter the Agents list by tag [filter-agents-by-tag]

On the **Agents** tab in {{fleet}}, select the tags you want from the **Tags** filter. You can also use a KQL query in the search bar, such as `fleet-agents.tags : "production"`.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.1+` To find agents that don't have any tags, select **No tags** in the **Tags** filter.

:::{image} images/agent-tags.png
:alt: Tags filter on the Fleet Agents tab
:screenshot:
:::
