---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-unprivileged.html
---

# Run Elastic Agent without administrative privileges [elastic-agent-unprivileged]

Beginning with {{stack}} version 8.15, {{agent}} is no longer required to be run by a user with superuser privileges. You can now run agents in an `unprivileged` mode that does not require `root` access on Linux or macOS, or `admin` access on Windows. Being able to run agents without full administrative privileges is often a requirement in organizations where this kind of access is often very limited.

In general, agents running without full administrative privileges will perform and behave exactly as those run by a superuser. There are certain integrations and datastreams that are not available, however. If an integration requires root access, this is [indicated on the integration main page](#unprivileged-integrations).

You can also [change the privilege mode](#unprivileged-change-mode) of an {{agent}} after it has been installed.

Refer to [Agent and dashboard behaviors in unprivileged mode](#unprivileged-command-behaviors) and [Run {{agent}} in `unprivileged` mode](#unprivileged-running) for the requirements and steps associated with running an agent without full `root` or `admin` superuser privileges.

* [Run {{agent}} in `unprivileged` mode](#unprivileged-running)
* [Agent and dashboard behaviors in unprivileged mode](#unprivileged-command-behaviors)
* [Using Elastic integrations](#unprivileged-integrations)
* [Viewing an {{agent}} privilege mode](#unprivileged-view-mode)
* [Changing an {{agent}}'s privilege mode](#unprivileged-change-mode)
* [Using `unprivileged` mode with a pre-existing user and group](#unprivileged-preexisting-user)


## Run {{agent}} in `unprivileged` mode [unprivileged-running]

To run {{agent}} without administrative privileges you use exactly the same commands that you use for {{agent}} otherwise, with one exception. When you run the [`elastic-agent install`](/reference/ingestion-tools/fleet/agent-command-reference.md#elastic-agent-install-command) command, add the `--unprivileged` flag. For example:

```shell
elastic-agent install \
  --url=https://cedd4e0e21e240b4s2bbbebdf1d6d52f.fleet.eu-west-1.aws.cld.elstc.co:443 \
  --enrollment-token=NEFmVllaa0JLRXhKebVKVTR5TTI6N2JaVlJpSGpScmV0ZUVnZVlRUExFQQ== \
  --unprivileged
```

::::{important}
Note the following current restrictions for running {{agent}} in `unprivileged` mode:

* On Linux systems, after {{agent}} has been installed with the `--unprivileged` flag, all {{agent}} commands can be run without being the root user.

    * The `sudo` option is still required for the `elastic-agent install` command. Only `root` can install new services. The installed service will not run as the root user.

* Using `sudo` without specifying an alternate non-root user with `sudo -u` in a command may result in [an error](/troubleshoot/ingest/fleet/common-problems.md#agent-sudo-error) due to the agent not having the required privileges.
* Using `sudo -u elastic-agent-user` will run commands as the user running the {{agent}} service and will always work.
* For files that allow users in the `elastic-agent` group access, using an alternate user that has been added to that group will also work. There are still some commands that are only accessible to the `elastic-agent-user` that runs the service.

    * For example, `elastic-agent inspect` requires you to prefix the command with `sudo -u elastic-agent-user`.

        ```shell
        sudo -u elastic-agent-user elastic-agent inspect
        ```


::::



## Agent and dashboard behaviors in unprivileged mode [unprivileged-command-behaviors]

In addition to the [integrations that are not available](#unprivileged-integrations) when {{agent}} is run in unpriviledged mode, certain data streams are also not available. The following tables show, for different operating systems, the impact when the agent does not have full administrative privileges. In most cases the limitations can be mediated by granting permissions for a user or group to the files indicated.

| Action | Behavior in unprivileged mode | Resolution |
| --- | --- | --- |
| Run {{agent}} with the System integration | Log file error: `Unexpected file opening error: Failed opening /var/log/system.log: open /var/log/system.log: permission denied`. | Give read permission to the `elastic-agent` group for the `/var/log/system.log` file to fix this error. |
| Run {{agent}} with the System integration | On the `[Logs System] Syslog` dashboard, the `Syslog events by hostname`, `Syslog hostnames and processes` and `Syslog logs` visualizations are are missing data. | Give read permission to the `elastic-agent` group for the `/var/log/system.log` file to fix the missing visualizations. |
| Run {{agent}} with the System integration | On the `[Metrics System] Host overview` dashboard, only the processes run by the `elastic-agent-user` user are shown in the CPU and memory usage lists. | To fix the missing processes in the visualization lists you can add add the `elastic-agent-user` user to the system `admin` group. Note that while this mitigates the issue, it also grants `elastic-agent user` with more permissions than may be desired. |
| Run {{agent}} and access the {{agent}} dashboards | On the `[Elastic Agent] Agents info` dashboard, visualizations including `Most Active Agents` and `Integrations per Agent` are missing data. | To fix the missing data in the visualizations you can add add the `elastic-agent-user` user to the system `admin` group. Note that while this mitigates the issue it also grants `elastic-agent user` with more permissions than may be desired. |
| Run {{agent}} and access the {{agent}} dashboards | On the `[Elastic Agent] Integrations` dashboard, visualizations including `Integration Errors Table`, `Events per integration` and `Integration Errors` are missing data. | To fix the missing data in the visualizations you can add add the `elastic-agent-user` user to the system `admin` group. Note that while this mitigates the issue it also grants `elastic-agent user` with more permissions than may be desired. |

| Action | Behavior in unprivileged mode | Resolution |
| --- | --- | --- |
| Run {{agent}} with the System integration | Log file error: `[elastic_agent.filebeat][error] Harvester could not be started on new file: /var/log/auth.log.1, Err: error setting up harvester: Harvester setup failed. Unexpected file opening error: Failed opening /var/log/auth.log.1: open /var/log/auth.log.1: permission denied` | To avoid the error you can add add the `elastic-agent-user` user to the `adm` group. Note that while this mitigates the issue it also grants `elastic-agent user` with more permissions than may be desired. |
| Run {{agent}} with the System integration | Log file error: `[elastic_agent.metricbeat][error] error getting filesystem usage for /run/user/1000/gvfs: error in Statfs syscall: permission denied` | To avoid the error you can add add the `elastic-agent-user` user to the `adm` group. Note that while this mitigates the issue it also grants `elastic-agent user` with more permissions than may be desired. |
| Run {{agent}} with the System integration | On the `[Logs System] Syslog` dashboard, the `Syslog events by hostname`, `Syslog hostnames and processes` and `Syslog logs` visualizations are are missing data. | To fix the missing data in the visualizations you can add add the `elastic-agent-user` user to the `adm` group. Note that while this mitigates the issue it also grants `elastic-agent user` with more permissions than may be desired. |
| Run {{agent}} and access the {{agent}} dashboards | On the `[Elastic Agent] Agents info` dashboard, visualizations including `Most Active Agents` and `Integrations per Agent` are missing data. | Giving read permission to the `elastic-agent` group for the `/var/log/system.log` file will partially fix the visualizations, but errors may still occur because the `elastic-agent-user` does not have read access to files in the `/run/user/1000/` directory. |
| Run {{agent}} and access the {{agent}} dashboards | On the `[Elastic Agent] Integrations` dashboard, visualizations including `Integration Errors Table`, `Events per integration` and `Integration Errors` are missing data. | Give read permission to the `elastic-agent` group for the `/var/log/system.log` file to fix the missing visualizations. |

| Action | Behavior in unprivileged mode | Resolution |
| --- | --- | --- |
| Run {{agent}} with the System integration | Log file error: `failed to open Windows Event Log channel "Security": Access is denied` | Add the `elastic-agent-user` user to the `Event Log Users` group to fix this error. |
| Run {{agent}} with the System integration | Log file error: `cannot open new key in the registry in order to enable the performance counters: Access is denied` | Update the permissions for the `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\PartMgr` registry to fix this error. |
| Run {{agent}} with the System integration | Most of the System and {{agent}} dashboard visualizations are missing all data. | Add the `elastic-agent-user` user to the `Event Log Users` group and update the permissions for the `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\PartMgr` registry to fix the missing visualizations.<br>Note that the `elastic-agent-user` user may still not have access to all processes, so the lists in the `Top processes by CPU usage` and `Top processes by memory usage` visualizations may be incomplete. |
| Run {{agent}} with the System integration | On the `[Metrics System] Host overview` dashboard, the `Disk usage` visualizations are missing data. | This occurs because direct access to the disk or a volume is restricted and not available to users without administrative privileges. Refer to [Running with Special Privileges](https://learn.microsoft.com/en-us/windows/win32/secbp/running-with-special-privileges) in the Microsoft documentation for details. |


## Using Elastic integrations [unprivileged-integrations]

Most Elastic integrations support running {{agent}} in unprivileged mode. For the exceptions, any integration that requires {{agent}} to have root privileges has the requirement indicated at the top of the integration page in {{kib}}:

:::{image} images/integration-root-requirement.png
:alt: Elastic Defend integration page showing root requirement
:class: screenshot
:::

As well, a warning is displayed in {{kib}} if you try to add an integration that requires root privileges to an {{agent}} policy that has agents enrolled in unprivileged mode.

:::{image} images/unprivileged-agent-warning.png
:alt: Warning indicating that root privileged agent is required for an integration
:class: screenshot
:::

Examples of integrations that require {{agent}} to have administrative privileges are:

* [{{elastic-defend}}](integration-docs://docs/reference/endpoint.md)
* [Auditd Manager](integration-docs://docs/reference/auditd_manager.md)
* [File Integrity Monitoring](integration-docs://docs/reference/fim.md)
* [Network Packet Capture](integration-docs://docs/reference/network_traffic.md)
* [System Audit](integration-docs://docs/reference/system_audit.md)
* [Universal Profiling Agent](integration-docs://docs/reference/profiler_agent.md)


## Viewing an {{agent}} privilege mode [unprivileged-view-mode]

The **Agent details** page shows you the privilege mode for any running {{agent}}.

To view the status of an {{agent}}:

1. In {{fleet}}, open the **Agents** tab.
2. Select an agent and click **View agent** in the actions menu.
3. The **Agent details** tab shows whether the agent is running in `privileged` or `unprivileged` mode.

    :::{image} images/agent-privilege-mode.png
    :alt: Agent details tab showing the agent is running as non-root
    :class: screenshot
    :::


As well, for any {{agent}} policy you can view the number of agents that are currently running in privileged or unprivileged mode:

1. In {{fleet}}, open the **Agent policies** tab.
2. Click the agent policy to view the policy details.

The number of agents enrolled with the policy is shown. Hover over the link to view the number of privileged and unpriviled agents.

:::{image} images/privileged-and-unprivileged-agents.png
:alt: Agent policy tab showing 1 unprivileged agent and 0 privileged enrolled agents
:class: screenshot
:::

In the event that the {{agent}} policy has integrations installed that require root privileges, but there are agents running without root privileges, this is shown in the tooltip.

:::{image} images/root-integration-and-unprivileged-agents.png
:alt: Agent policy tab showing 1 unprivileged agent and 0 privileged enrolled agents
:class: screenshot
:::


## Changing an {{agent}}'s privilege mode [unprivileged-change-mode]

For any installed {{agent}} you can change the mode that it’s running in by running the `privileged` or `unprivileged` subcommand.

Change mode from privileged to unprivileged:

```shell
sudo elastic-agent unprivileged
```

Note that changing to `unprivileged` mode is prevented if the agent is currently enrolled in a policy that includes an integration that requires administrative access, such as the {{elastic-defend}} integration.

Change mode from unprivileged to privileged:

```shell
sudo elastic-agent privileged
```

When an agent is running in `unprivileged` mode, if it doesn’t have the right level of privilege to read a data source, you can also adjust the agent’s privileges by adding `elastic-agent-user` to the user group that has privileges to read the data source.

As background, when you run {{agent}} in `unprivileged` mode, one user and one group are created on the host. The same names are used for all operating systems:

* `elastic-agent-user`: The user that is created and that the {{agent}} service runs as.
* `elastic-agent`: The group that is created. Any user in this group has access to control and communicate over the control protocol to the {{agent}} daemon.

For example:

1. When you install {{agent}} with the `--unprivileged` setting, the `elastic-agent-user` user and the `elastic-agent` group are created automatically.
2. If you then want your user `myuser` to be able to run an {{agent}} command such as `elastic-agent status`, add the `myuser` user to the `elastic-agent` group.
3. Then, once added to the group, the `elastic-agent status` command will work. Prior to that, the user `myuser` running the command will result in a permission error that indicates a problem communicating with the control socket.


## Using `unprivileged` mode with a pre-existing user and group [unprivileged-preexisting-user]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


In certain cases you may want to install {{agent}} in `unprivileged` mode, with the agent running as a pre-existing user or as part of a pre-existing group. For example, on a Windows system you may have a service account in Active Directory and you’d like {{agent}} to run under that account.

To install {{agent}} in `unprivileged` mode as a specific user, add the `--user` and `--password` parameters to the install command:

```shell
elastic-agent install --unprivileged  --user="my.path\username" --password="mypassword"
```

To install {{agent}} in `unprivileged` mode as part of a specific group, add the `--group` and `--password` parameters to the install command:

```shell
elastic-agent install --unprivileged  --group="my.path\groupname" --password="mypassword"
```

Alternatively, if you have {{agent}} already installed with administrative privileges, you can change the agent to use `unprivileged` mode and to run as a specific user or in a specific group. For example:

```shell
elastic-agent unprivileged --user="my.path\username" --password="mypassword"
```

```shell
elastic-agent unprivileged --group="my.path\groupname" --password="mypassword"
```
