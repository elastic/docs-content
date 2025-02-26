---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/start-stop-elastic-agent.html
---

# Start and stop Elastic Agents on edge hosts [start-stop-elastic-agent]

You can start and stop the {{agent}} service on the host where it’s running, and it will no longer send data to {{es}}.


## Start {{agent}} [start-elastic-agent-service]

If you’ve stopped the {{agent}} service and want to restart it, use the commands that work with your system:

:::::::{tab-set}

::::::{tab-item} macOS
```shell
sudo launchctl load /Library/LaunchDaemons/co.elastic.elastic-agent.plist
```
::::::

::::::{tab-item} Linux
```shell
sudo service elastic-agent start
```
::::::

::::::{tab-item} Windows
```shell
Start-Service Elastic Agent
```
::::::

::::::{tab-item} DEB
The DEB package includes a service unit for Linux systems with systemd. On these systems, you can manage {{agent}} by using the usual systemd commands.

Use `systemctl` to start the agent:

```shell
sudo systemctl start elastic-agent
```

Otherwise, use:

```shell
sudo service elastic-agent start
```
::::::

::::::{tab-item} RPM
The RPM package includes a service unit for Linux systems with systemd. On these systems, you can manage {{agent}} by using the usual systemd commands.

Use `systemctl` to start the agent:

```shell
sudo systemctl start elastic-agent
```

Otherwise, use:

```shell
sudo service elastic-agent start
```
::::::

:::::::

## Stop {{agent}} [stop-elastic-agent-service]

To stop {{agent}} and its related executables, stop the {{agent}} service. Use the commands that work with your system:

:::::::{tab-set}

::::::{tab-item} macOS
```shell
sudo launchctl unload /Library/LaunchDaemons/co.elastic.elastic-agent.plist
```

::::{note}
{{agent}} will restart automatically if the system is rebooted.
::::
::::::

::::::{tab-item} Linux
```shell
sudo service elastic-agent stop
```

::::{note}
{{agent}} will restart automatically if the system is rebooted.
::::
::::::

::::::{tab-item} Windows
```shell
Stop-Service Elastic Agent
```

If necessary, use Task Manager on Windows to stop {{agent}}. This will kill the `elastic-agent` process and any sub-processes it created (such as {{beats}}).

::::{note}
{{agent}} will restart automatically if the system is rebooted.
::::
::::::

::::::{tab-item} DEB
The DEB package includes a service unit for Linux systems with systemd. On these systems, you can manage {{agent}} by using the usual systemd commands.

Use `systemctl` to stop the agent:

```shell
sudo systemctl stop elastic-agent
```

Otherwise, use:

```shell
sudo service elastic-agent stop
```

::::{note}
{{agent}} will restart automatically if the system is rebooted.
::::
::::::

::::::{tab-item} RPM
The RPM package includes a service unit for Linux systems with systemd. On these systems, you can manage {{agent}} by using the usual systemd commands.

Use `systemctl` to stop the agent:

```shell
sudo systemctl stop elastic-agent
```

Otherwise, use:

```shell
sudo service elastic-agent stop
```

::::{note}
{{agent}} will restart automatically if the system is rebooted.
::::
::::::

:::::::
