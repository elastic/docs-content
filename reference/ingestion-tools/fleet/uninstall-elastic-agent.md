---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/uninstall-elastic-agent.html
---

# Uninstall Elastic Agents from edge hosts [uninstall-elastic-agent]


## Uninstall on macOS, Linux, and Windows [_uninstall_on_macos_linux_and_windows]

To uninstall {{agent}}, run the `uninstall` command from the directory where {{agent}} is running.

::::{important}
Be sure to run the `uninstall` command from a directory outside of where {{agent}} is installed.

For example, on a Windows system the install location is `C:\Program Files\Elastic\Agent`. Run the uninstall command from `C:\Program Files\Elastic` or `\tmp`, or even your default home directory:

```shell
C:\"Program Files"\Elastic\Agent\elastic-agent.exe uninstall
```

::::


:::::::{tab-set}

::::::{tab-item} macOS
::::{tip}
You must run this command as the root user.
::::


```shell
sudo /Library/Elastic/Agent/elastic-agent uninstall
```
::::::

::::::{tab-item} Linux
::::{tip}
You must run this command as the root user.
::::


```shell
sudo /opt/Elastic/Agent/elastic-agent uninstall
```
::::::

::::::{tab-item} Windows
Open a PowerShell prompt as an Administrator (right-click the PowerShell icon and select **Run As Administrator**).

From the PowerShell prompt, run:

```shell
C:\"Program Files"\Elastic\Agent\elastic-agent.exe uninstall
```
::::::

:::::::
Follow the prompts to confirm that you want to uninstall {{agent}}. The command stops and uninstalls any managed programs, such as {{beats}} and {{elastic-endpoint}}, before it stops and uninstalls {{agent}}.

If you run into problems, refer to [Troubleshoot common problems](/troubleshoot/ingest/fleet/common-problems.md).

If you are using DEB or RPM, you can use the package manager to remove the installed package.

::::{note}
For hosts enrolled in the {{elastic-defend}} integration with Agent tamper protection enabled, you’ll need to include the uninstall token in the command, using the `--uninstall-token` flag. Refer to the [Agent tamper protection docs](/reference/security/elastic-defend/agent-tamper-protection.md) for more information.
::::



## Remove {{agent}} files manually [_remove_agent_files_manually]

You might need to remove {{agent}} files manually if there’s a failure during installation.

To remove {{agent}} manually from your system:

1. [Unenroll the agent](/reference/ingestion-tools/fleet/unenroll-elastic-agent.md) if it’s managed by {{fleet}}.
2. For standalone agents, back up any configuration files you want to preserve.
3. On your host, [stop the agent](/reference/ingestion-tools/fleet/start-stop-elastic-agent.md#stop-elastic-agent-service). If any {{agent}}-related processes are still running, stop them too.

    ::::{tip}
    Search for these processes and stop them if they’re still running: `filebeat`, `metricbeat`, `fleet-server`, and `elastic-endpoint`.
    ::::

4. Manually remove the {{agent}} files from your system. For example, if you’re running {{agent}} on macOS, delete `/Library/Elastic/Agent/*`. Not sure where the files are installed? Refer to [Installation layout](/reference/ingestion-tools/fleet/installation-layout.md).
5. If you’ve configured the {{elastic-defend}} integration, also remove the files installed for endpoint protection. The directory structure is similar to {{agent}}, for example, `/Library/Elastic/Endpoint/*`.

    ::::{note}
    When you remove the {{elastic-defend}} integration from a macOS host (10.13, 10.14, or 10.15), the Endpoint System Extension is left on disk intentionally. If you want to remove the extension, refer to the documentation for your operating system.
    ::::
