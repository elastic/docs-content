---
navigation_title: Diagnostics
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Capture {{agent}} diagnostics [agent-diagnostic]

Elastic's diagnostic tools capture point-in-time snapshots of {{fleet}} and {{agent}} related statistics and logs. They work against all product versions.

Their information can be used to troubleshoot problems with your setup. You can generate diagnostic information using this tool before [escalating to us](/troubleshoot/ingest/fleet/fleet-elastic-agent.md#troubleshooting-intro-escalate) to minimize turnaround time.

## Which information do I need? [agent-diagnostic-type]

For [{{fleet}}-managed {{agent}}](/reference/fleet/install-fleet-managed-elastic-agent.md), related settings and states can by surfaced by:

* {{kib}} from the [{{kib}} {{fleet}} APIs](/reference/fleet/fleet-api-docs.md)
* {{agent}} and {{fleet}} from their [command reference](/reference/fleet/agent-command-reference.md)

[Standalone {{agent}}s](/reference/fleet/install-standalone-elastic-agent.md) are not associated to {{kib}} nor {{fleet}}, but their diagnostics are still accessible from the CLI.

To pull data from the respective applicable locations, refer to:

* [Capture {{kib}} diagnostics](/troubleshoot/kibana/capturing-diagnostics.md)
* [Collect {{agent}} diagnostics](#agent-diagnostics-collect)
  * [Using the CLI](#agent-diagnostics-cli)
  * [Using the {{fleet}} UI](#agent-diagnostics-ui)

    :::{note}
    :applies_to: ess: ga
    To pull {{agent}} diagnostics for the managed [{{fleet-server}}](/reference/fleet/fleet-server.md) on your hosted deployment, you have to use the {{fleet}} UI. The {{fleet-server}} agent is associated with a managed agent policy named "Elastic Cloud agent policy".
    :::

You need to determine which diagnostic types are needed to investigate your specific issue. This table shows common troubleshooting situations and which diagnostics are commonly associated:

| Situation | {{kib}} | {{agent}} | {{fleet}} |
| --- | --- | --- | --- |
| {{kib}} reports there's no {{fleet-server}} | Yes | No | Yes |
| {{agent}} is unable to connect to {{fleet}} | No | Yes | Yes |
| {{agent}} component or integration errors | No | Yes | No |
| {{agent}} update issues or desynced status | Yes | Yes | No |

When in doubt, start with the {{kib}} and {{agent}} diagnostics.

:::{tip}
Some {{agent}} configuration issues only appear in the agent's start-up debug logs. This is more common for cloud-connecting [Elastic integrations](https://www.elastic.co/docs/reference/integrations) which maintain checkpoints. This can cause later logs to only document that the subprocess has stopped or that it has not changed state after an earlier error. In these situations, follow these steps:

1. Enable [`debug` logging](/reference/fleet/monitor-elastic-agent.md#change-logging-level).
2. [Restart {{agent}}](/reference/fleet/agent-command-reference.md#elastic-agent-restart-command).
3. Wait 10 minutes for the changes to sync from the {{fleet-server}} to the {{agent}} and for the {{agent}} to restart.
4. Pull the {{agent}} diagnostics using your preferred method.
5. Disable `debug` logging.
:::

## Collect {{agent}} diagnostics [agent-diagnostics-collect] 

{{agent}} comes bundled with a [`diagnostics` command](/reference/fleet/agent-command-reference.md#elastic-agent-diagnostics-command) which generates a zip archive containing troubleshooting diagnostic information. This export is intended only for debugging purposes and its structure can change between releases.

The {{fleet}} UI provides the ability to remotely generate and gather an {{agent}}'s diagnostics bundle if it is online in a [`Healthy` or `Unhealthy` status](/reference/fleet/monitor-elastic-agent.md#view-agent-status). For {{agent}}s in other statuses, you must use the CLI to grab their diagnostic.

:::{warning}
Diagnostics and logs mainly emit product metadata and settings, but they might expose sensitive data which needs to be redacted before being shared outside of your organization. For more details, refer to [Sanitize](#agent-diagnostics-sanitize).
:::

### Using the {{fleet}} UI [agent-diagnostics-ui]

The diagnostics are sent to {{fleet-server}} which in turn sends it to {{es}}. Therefore, this works even with {{agents}} that are not using the {{es}} output. To download the diagnostics bundle for local viewing:

1. In {{fleet}}, open the **Agents** tab.
2. In the **Host** column, click the agent’s name.
3. Select the **Diagnostics** tab and click the **Request diagnostics .zip** button.

    :::{image} /troubleshoot/images/fleet-collect-agent-diagnostics1.png
    :alt: Collect agent diagnostics under agent details
    :screenshot:
    :::

4. In the **Request diagnostics** pop-up, select **Collect additional CPU metrics** if you’d like detailed CPU data.

    :::{image} /troubleshoot/images/fleet-collect-agent-diagnostics2.png
    :alt: Collect agent diagnostics confirmation pop-up
    :screenshot:
    :::

5. Click the **Request diagnostics** button.

When it is available, the new diagnostics bundle is listed on the **Diagnostics** tab along with any in-progress or previously collected bundles for the {{agent}}.

The diagnostics bundles are stored in {{es}} and are removed automatically after 7 days. You can also delete any previously created bundles by clicking the trash can icon.

### Using the CLI [agent-diagnostics-cli]

Run the [`diagnostics` command](/reference/fleet/agent-command-reference.md#elastic-agent-diagnostics-command) in the {{agent}}'s [install directory](/reference/fleet/installation-layout.md). Depending on your operating system, run:

* Linux-based systems

  ```shell
  cd /opt/Elastic/Agent
  .elastic-agent diagnostics
  ```

* Windows Powershell 

  ```shell
  cd "C:\Program Files\Elastic\Agent"
  .\elastic-agent.exe diagnostics
  ```

* Apple MacOS

  ```shell
  sudo -i
  cd /Library/Elastic/Agent
  ./elastic-agent diagnostics
  ```

* Docker

  1. Determine the container ID with Docker [`ps`](https://docs.docker.com/reference/cli/docker/container/ps/).

    ```shell
    docker ps | grep "beats/elastic-agent"
    ```

  2. Use Docker [`exec`](https://docs.docker.com/reference/cli/docker/container/exec/) to run the diagnostics, replacing the `CONTAINER_ID` placeholder.

    ```shell
    docker exec -it CONTAINER_ID elastic-agent diagnostics
    ```

    Note the filename and location of the output file.

  3. Use Docker [`cp`](https://docs.docker.com/reference/cli/docker/container/cp/) to copy the diagnostic file to your local machine, replacing the `CONTAINER_ID` and `FILE_NAME` placeholders:

    ```shell
    docker cp CONTAINER_ID:/usr/share/elastic-agent/FILE_NAME FILE_NAME
    ```

* Kubernetes

  1. Determine the container ID with [`get`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/).

    ```shell
    kubectl get pods --all-namespaces | grep agent
    ```

  2. Run the diagnostics with [`exec`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_exec/), replacing the `NAMESPACE` and `POD_NAME` placeholders:

    ```shell
    kubectl exec --stdin --tty POD_NAME -n NAMESPACE -- elastic-agent diagnostics
    ```

    Note the filename and location of the output file. 

  3. Use [`cp`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_cp/) to copy the diagnostic file to your local machine, replacing the `NAMESPACE`, `POD_NAME`, and `FILE_NAME` placeholders.

    ```shell
    kubectl cp NAMESPACE/POD_NAME:FILE_NAME FILE_NAME
    ```

### Sanitize [agent-diagnostics-sanitize]

{{agent}} attempts to automatically redact credentials and API keys when creating [its diagnostic files](/reference/fleet/agent-command-reference.md#elastic-agent-diagnostics-command). Review the contents of the archive before sharing it to ensure that all forms of organizational private information is censored as needed. For example, ensure:

* There are no credentials in plain text in the [`*.yaml` diagnostic files](/reference/fleet/agent-command-reference.md#elastic-agent-diagnostics-command).

* The raw form of events failing to output is shown in `*.ndjson`. By default, only `warn` logs are registered. To log all events, enable the `debug` logging level. If you want to omit the raw events from the diagnostics, add the flag `--exclude-events`.
