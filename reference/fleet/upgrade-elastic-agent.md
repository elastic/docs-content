---
navigation_title: Upgrade {{agent}}s
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/upgrade-elastic-agent.html
applies_to:
  stack: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Upgrade {{fleet}}-managed {{agent}}s [upgrade-elastic-agent]


::::{tip}
Want to upgrade a standalone agent instead? See [Upgrade standalone {{agent}}s](/reference/fleet/upgrade-standalone.md).
::::


With {{fleet}} upgrade capabilities, you can view and select agents that are out of date, and trigger selected agents to download, install, and run the new version. You can trigger upgrades to happen immediately, or specify a maintenance window during which the upgrades will occur. If your {{stack}} subscription level supports it, you can schedule upgrades to occur at a specific date and time.

In most failure cases the {{agent}} may retry an upgrade after a short wait. The wait durations between retries are: 1m, 5m, 10m, 15m, 30m, and 1h. During this time, the {{agent}} may show up as "retrying" in the {{fleet}} UI. As well, if agent upgrades have been detected to have stalled, you can restart the upgrade process for a [single agent](#restart-upgrade-single) or in bulk for [multiple agents](#restart-upgrade-multiple).

This approach simplifies the process of keeping your agents up to date. It also saves you time because you don’t need third-party tools or processes to manage upgrades.

By default, {{agent}}s require internet access to perform binary upgrades from {{fleet}}. However, you can host your own artifacts repository and configure {{agent}}s to download binaries from it. For more information, refer to [Air-gapped environments](/reference/fleet/air-gapped.md).

::::{note}
The upgrade feature is not supported for upgrading DEB/RPM packages or Docker images. Refer to [Upgrade RPM and DEB system packages](#upgrade-system-packages) to upgrade a DEB or RPM package manually.
::::


For a detailed view of the {{agent}} upgrade process and the interactions between {{fleet}}, {{agent}}, and {{es}}, refer to the [Communications amongst components](https://github.com/elastic/elastic-agent/blob/main/docs/upgrades.md) diagram in the `elastic-agent` GitHub repository.


## Restrictions [upgrade-agent-restrictions]

Note the following restrictions with upgrading an {{agent}}:

* {{agent}} cannot be upgraded to a minor version higher than the currently installed minor version of {{fleet-server}}. For example, you can enroll 9.1.5 {{agents}} with a 9.1.0 {{fleet-server}}, but not 9.2.0 {{agents}}. So while you can install newer maintenance releases, you cannot install newer minor versions. Before you upgrade {{agents}} to a newer minor version, you should first upgrade any agents that are acting as a [{{fleet-server}}](/reference/fleet/fleet-server.md) (any agents associated with a {{fleet-server}} policy).
* To be upgradeable, {{agent}} must not be running inside a container.
* To be upgradeable in a Linux environment, {{agent}} must be running as a service. The Linux Tar install instructions for {{agent}} provided in {{fleet}} include the commands to run it as a service. {{agent}} RPM and DEB system packages cannot be upgraded through {{fleet}}.

These restrictions apply whether you are upgrading {{agents}} individually or in bulk. In the event that an upgrade isn’t eligible, {{fleet}} generates a warning message when you attempt the upgrade.


## Upgrading {{agent}} [upgrade-agent]

To upgrade your {{agents}}, go to **Management** → **{{fleet}}** → **Agents** in {{kib}}. You can perform the following upgrade-related actions:

| User action | Result |
| --- | --- |
| [Upgrade a single {{agent}}](#upgrade-an-agent) | Upgrade a single agent to a specific version. |
| [Do a rolling upgrade of multiple {{agent}}s](#rolling-agent-upgrade) | Do a rolling upgrade of multiple agents over a specific time period. |
| [Schedule an upgrade](#schedule-agent-upgrade) | Schedule an upgrade of one or more agents to begin at a specific time. |
| [View upgrade status](#view-upgrade-status) | View the detailed status of an agent upgrade, including upgrade metrics and agent logs. |
| [Restart an upgrade for a single agent](#restart-upgrade-single) | Restart an upgrade process that has stalled for a single agent. |
| [Restart an upgrade for multiple agents](#restart-upgrade-multiple) | Do a bulk restart of the upgrade process for a set of agents. |

With an [Elastic subscription level](https://www.elastic.co/subscriptions) that supports **automatic agent binary upgrades**, you can also configure an automatic upgrade of a percentage of the {{agents}} enrolled in an {{agent}} policy. For more information, refer to [Auto-upgrade agents enrolled in a policy](#auto-upgrade-agents). {applies_to}`stack: ga 9.1.0`


## Upgrade a single {{agent}} [upgrade-an-agent]

1. On the **Agents** tab, agents that can be upgraded are identified with an **Upgrade available** indicator.

    :::{image} images/upgrade-available-indicator.png
    :alt: Indicator on the UI showing that the agent can be upgraded
    :screenshot:
    :::

    You can also click the **Upgrade available** button to filter the list agents to only those that currently can be upgraded.

2. From the **Actions** menu next to the agent, choose **Upgrade agent**.

    :::{image} images/upgrade-single-agent.png
    :alt: Menu for upgrading a single {{agent}}
    :screenshot:
    :::

3. In the Upgrade agent window, select or specify an upgrade version and click **Upgrade agent**.

    {{kib}} provides a list of the {{agent}} versions available for upgrade. A version number ending with a build identifier in the format `+build{yyyymmddhhmm}` indicates an [independent {{agent}} release version](./fleet-agent-release-process.md#independent-agent-releases).

    In certain cases, the latest available {{agent}} version may not be recognized by {{kib}}. For instance, this occurs when the {{kib}} version is lower than the {{agent}} version. You can specify a custom version for {{agent}} to upgrade to by entering the version into the **Upgrade version** text field.

    :::{image} images/upgrade-agent-custom.png
    :alt: Menu for upgrading a single {{agent}}
    :screenshot:
    :::


## Do a rolling upgrade of multiple {{agent}}s [rolling-agent-upgrade]

You can do rolling upgrades to avoid exhausting network resources when updating a large number of {{agent}}s.

1. On the **Agents** tab, select multiple agents, and click **Actions**.
2. From the **Actions** menu, choose to upgrade the agents.
3. In the Upgrade agents window, select an upgrade version.
4. Select the amount of time available for the maintenance window. The upgrades are spread out uniformly across this maintenance window to avoid exhausting network resources.

    To force selected agents to upgrade immediately when the upgrade is triggered, select **Immediately**. Avoid using this setting for batches of more than 10 agents.

5. Upgrade the agents.

Agents in a rollout period have the status `Updating` until the upgrade is complete, even if the upgrade has not started yet.

## Schedule an upgrade [schedule-agent-upgrade]

::::{note}
This feature is available only for certain subscription levels. For more information, check **Scheduled agent binary upgrades** on the [Elastic subscriptions](https://www.elastic.co/subscriptions) page.
::::

1. On the **Agents** tab, select one or more agents, and click **Actions**.
2. From the **Actions** menu, choose to schedule an upgrade.

    :::{image} images/schedule-upgrade.png
    :alt: Menu for scheduling {{agent}} upgrades
    :screenshot:
    :::

3. In the Upgrade window, select an upgrade version.
4. Select a maintenance window. For more information, refer to [Do a rolling upgrade of multiple {{agent}}s](#rolling-agent-upgrade).
5. Set the date and time when you want the upgrade to begin.
6. Click **Schedule**.


## View upgrade status [view-upgrade-status]

On the Agents tab, when you trigger an upgrade, agents that are upgrading have the status `Updating` until the upgrade is complete, and then the status changes back to `Healthy`.

Agents on version 8.12 and higher that are currently upgrading additionally show a detailed upgrade status indicator.

:::{image} images/upgrade-states.png
:alt: Detailed state of an upgrading agent
:screenshot:
:::

The following table explains the upgrade states in the order that they can occur.

| State | Description |
| --- | --- |
| Upgrade requested | {{agent}} has received the upgrade notice from {{fleet}}. |
| Upgrade scheduled | {{agent}} has received the upgrade notice from {{fleet}} and the upgrade will start at the indicated time. |
| Upgrade downloading | {{agent}} is downloading the archive containing the new version artifact. |
| Upgrade extracting | {{agent}} is extracting the new version artifact from the downloaded archive. |
| Upgrade replacing | {{agent}} is currently replacing the former, pre-upgrade agent artifact with the new one. |
| Upgrade restarting | {{agent}} has been replaced with a new version and is now restarting in order to apply the update. |
| Upgrade monitoring | The newly upgraded {{agent}} has started and is being monitored for errors. |
| Upgrade rolled back | The upgrade was unsuccessful. {{agent}} is being rolled back to the former, pre-upgrade version. |
| Upgrade failed | An error has been detected in the newly upgraded {{agent}} and the attempt to roll the upgrade back to the previous version has failed. |

Under routine circumstances, an {{agent}} upgrade happens quickly. You typically will not see the agent transition through each of the upgrade states. The detailed upgrade status can be a useful tool especially if you need to diagnose the state of an agent that may have become stuck, or appears to have become stuck, during the upgrade process.

Beside the upgrade status indicator, you can hover your cursor over the information icon to get more detail about the upgrade.

:::{image} images/upgrade-detailed-state01.png
:alt: Granular upgrade details shown as hover text (agent has requested an upgrade)
:screenshot:
:::

:::{image} images/upgrade-detailed-state02.png
:alt: Granular upgrade details shown as hover text (agent is restarting to apply the update)
:screenshot:
:::

When you upgrade agents from versions below 8.12, the upgrade details are not provided.

:::{image} images/upgrade-non-detailed.png
:alt: An earlier release agent showing only the updating state without additional details
:screenshot:
:::

When upgrading many agents, you can fine tune the maintenance window by viewing stats and metrics about the upgrade:

1. On the **Agents** tab, click the host name to view agent details. If you don’t see the host name, try refreshing the page.
2. Click **View more agent metrics** to open the **[{{agent}}] Agent metrics** dashboard.

If an upgrade appears to have stalled, you can [restart it](#restart-upgrade-single).

If an upgrade fails, you can view the agent logs to find the reason:

1. In {{fleet}}, in the Host column, click the agent’s name.
2. Open the **Logs** tab.
3. Search for failures.

    :::{image} images/upgrade-failure.png
    :alt: Agent logs showing upgrade failure
    :screenshot:
    :::


## Restart an upgrade for a single agent [restart-upgrade-single]

An {{agent}} upgrade process may sometimes stall. This can happen for various reasons, including, for example, network connectivity issues or a delayed shutdown.

When an {{agent}} upgrade has been detected to be stuck, a warning indicator appears on the UI. When this occurs, you can restart the upgrade from either the **Agents** tab on the main {{fleet}} page or from the details page for any individual agent.

There is a required 10 minute cooldown period in between restart attempts. After launching a restart action you need to wait for the cooldown to complete before initiating another restart.

Restart from main {{fleet}} page:

1. From the **Actions** menu next to an agent that is stuck in an `Updating` state, choose **Restart upgrade**.
2. In the **Restart upgrade** window, select an upgrade version and click **Upgrade agent**.

Restart from an agent details page:

1. In {{fleet}}, in the **Host** column, click the agent’s name. On the **Agent details** tab, a warning notice appears if the agent is detected to have stalled during an upgrade.
2. Click **Restart upgrade**.
3. In the **Restart upgrade** window, select an upgrade version and click **Upgrade agent**.


## Restart an upgrade for multiple agents [restart-upgrade-multiple]

When the upgrade process for multiple agents has been detected to have stalled, you can restart the upgrade process in bulk. As with [restarting an upgrade for a single agent](#restart-upgrade-single), a 10 minute cooldown period is enforced between restarts.

1. On the **Agents** tab, select any set of the agents that are indicated to be stuck, and click **Actions**.
2. From the **Actions** menu, select **Restart upgrade <number> agents**.
3. In the **Restart upgrade…** window, select an upgrade version.
4. Select the amount of time available for the maintenance window. The upgrades are spread out uniformly across this maintenance window to avoid exhausting network resources.

    To force selected agents to upgrade immediately when the upgrade is triggered, select **Immediately**. Avoid using this setting for batches of more than 10 agents.

5. Restart the upgrades.


## Auto-upgrade agents enrolled in a policy [auto-upgrade-agents]

```{applies_to}
stack: ga 9.1.0
```

::::{note}
This feature is available only for certain subscription levels. For more information, check **Automatic agent binary upgrades** on the [Elastic subscriptions](https://www.elastic.co/subscriptions) page.
::::

To configure an automatic rollout of a new minor or patch version to a percentage of the agents enrolled in your {{agent}} policy. follow these steps:

1. In {{kib}}, go to **Management** → **{{fleet}}** → **Agent policies**.
2. Select the agent policy for which you want to configure an automatic agent upgrade.
3. On the agent policy's details page, find **Auto-upgrade agents**, and select **Manage** next to it.
4. In the **Manage auto-upgrade agents** window, click **Add target version**.
5. From the **Target agent version** dropdown, select the minor or patch version to which you want to upgrade a percentage of your agents.
6. In the **% of agents to upgrade** field, enter the percentage of active agents you want to upgrade to this target version.
   
   Note that:
   - Unenrolling, unenrolled, inactive, and uninstalled agents are not included in the count. For example, if you set the target upgrade percentage to 50% for a policy with 10 active agents and 10 inactive agents, the target is met when 5 active agents are upgraded.
   - Rounding is applied, and the actual percentage of the upgraded agents may vary slightly. For example, if you set the target upgrade percentage to 30% for a policy with 25 active agents, the target is met when 8 active agents are upgraded (32%).

7. You can then add a different target version, and specify the percentage of agents you want to be upgraded to that version. The total percentage of agents to be upgraded cannot exceed 100%.
8. Click **Save**.

Once the configuration is saved, an asynchronous task runs every 30 minutes, upgrading the agents in the policy to the specified target version.

If the number of agents to be upgraded is greater than or equal to 10, a rollout period is automatically applied. The rollout duration is either 10 minutes or `nAgents * 0.03` seconds, whichever is greater.

In case of any failed upgrades, the upgrades are retried with exponential backoff mechanism until the upgrade is successful, or the maximum number of retries is reached. Note that the maximum number of retries is the number of [configured retry delays](#auto-upgrade-settings).

::::{note}
Only active agents enrolled in the policy are considered for the automatic upgrade.

If new agents are assigned to the policy, the number of {{agents}} to be upgraded is adjusted according to the set percentages.
::::

### Configure the auto-upgrade settings [auto-upgrade-settings]

On self-managed and cloud deployments of {{stack}}, you can configure the default task interval and the retry delays of the automatic upgrade in the [{{kib}} {{fleet}} settings](kibana://reference/configuration-reference/fleet-settings.md). For example:

```yml
xpack.fleet.autoUpgrades.taskInterval: 15m <1>
xpack.fleet.autoUpgrades.retryDelays: ['5m', '10m', '20m'] <2>
```
1. The time interval at which the auto-upgrade task should run. Defaults to `30m`.
2. Array indicating how much time should pass before a failed auto-upgrade is retried. The array's length indicates the maximum number of retries. Defaults to `['30m', '1h', '2h', '4h', '8h', '16h', '24h']`.

For more information, refer to the [Kibana configuration reference](kibana://reference/configuration-reference.md).

### View the status of the automatic upgrade [auto-upgrade-view-status]

You can view the status of the automatic upgrade in the following ways:

- On the agent policy's details page, find **Auto-upgrade agents**, and select **Manage** to open the **Manage auto-upgrade agents** window.
  
  The status of the upgrade is displayed next to the specified target version and percentage, and includes the percentage of agents that have already been upgraded.

  To view any failed upgrades, hover over the **Upgrade failed** status, then click **Go to upgrade**.

- On the **{{fleet}}** → **Agents** page, click **Agent activity** to open a flyout showing logs of the {{agent}} activity and the progress of the automatic agent upgrade.


## Upgrade RPM and DEB system packages [upgrade-system-packages]

If you have installed and enrolled {{agent}} using either a DEB (for a Debian-based Linux distribution) or RPM (for a RedHat-based Linux distribution) install package, the upgrade cannot be managed by {{fleet}}. Instead, you can perform the upgrade using these steps.

For installation steps refer to [Install {{fleet}}-managed {{agent}}s](/reference/fleet/install-fleet-managed-elastic-agent.md).


### Upgrade a DEB {{agent}} installation: [_upgrade_a_deb_agent_installation]

1. Download the {{agent}} Debian install package for the release that you want to upgrade to:

    ```bash subs=true
    curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-amd64.deb
    ```

2. Upgrade {{agent}} to the target release:

    ```bash subs=true
    sudo dpkg -i elastic-agent-{{version.stack}}-amd64.deb
    ```

3. Confirm in {{fleet}} that the agent has been upgraded to the target version. Note that the **Upgrade agent** option in the **Actions** menu next to the agent will be disabled since [fleet]-managed upgrades are not supported for this package type.


### Upgrade an RPM {{agent}} installation: [_upgrade_an_rpm_agent_installation]

1. Download the {{agent}} RPM install package for the release that you want to upgrade to:

    ```bash subs=true
    curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-x86_64.rpm
    ```

2. Upgrade {{agent}} to the target release:

    ```bash subs=true
    sudo rpm -U elastic-agent-{{version.stack}}-x86_64.rpm
    ```

3. Confirm in {{fleet}} that the agent has been upgraded to the target version. Note that the **Upgrade agent** option in the **Actions** menu next to the agent will be disabled since {{fleet}}-managed upgrades are not supported for this package type.
