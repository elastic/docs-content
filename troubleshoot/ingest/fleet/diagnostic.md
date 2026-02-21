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

As explained under [What is {{fleet}} Server?](/reference/fleet/fleet-server.md), for [{{fleet}}-managed {{agent}}](/reference/fleet/install-fleet-managed-elastic-agent.md), related settings and states can by surfaced by:

* {{kib}} from the [{{kib}} {{fleet}} APIs](/reference/fleet/fleet-api-docs.md)
* {{agent}} and {{fleet}} from their [command reference](/reference/fleet/agent-command-reference.md)

[Standalone {{agent}}s](/reference/fleet/install-standalone-elastic-agent.md) are not associated to {{kibana}} nor {{fleet}}, but their diagnostics are still accessible from the CLI.

To pull data from the respective applicable locations, you will refer to:

* [Capture {{kib}} diagnostics](/troubleshoot/kibana/capturing-diagnostics.md) {applies_to}`stack: ga` 
* Collect {{agent}} diagnostics (below) {applies_to}`stack: ga` {applies_to}`serverless: ga`
  * [Using the CLI](#agent-diagnostics-cli)
  * [Using the {{fleet}} UI](#agent-diagnostics-ui)

    :::{note}{applies_to}`ess: ga`
    If you need to pull an {{agent}} diagnostic for the [Fleet Server](/reference/fleet/fleet-server.md), as a hosted service you cannot access the CLI directly so will need to grab the diagnostic using the {{fleet}} UI. The {{fleet}} agent will be associated to the managed Agent policy named "Elastic Cloud agent policy".
    :::

You will need to determine which diagnostic types are needed to investigate your specific issue.  The following are common troubleshooting situations and which diagnostics are commonly associated:

| Situation | {{kib}} | {{agent}} | {{fleet}} |
| --- | --- | --- | --- |
| {{kib}} reports no {{fleet}} server | Yes | No | Yes |
| {{agent}} unable to connect to {{fleet}} | No | Yes | Yes |
| {{agent}} component or integration errors | No | Yes | No |
| {{agent}} update issues or desynced status | Yes | Yes | No |

When in doubt, start with the {{kib}} and {{agent}} diagnostics.

:::{tip}
Some {{agent}} configuration issues only appear in their start-up debug logs. This is more common for cloud-connecting [{{elastic}} Integrations](https://www.elastic.co/docs/reference/integrations) which maintain checkpoints. This can cause later logs to only note that the subprocess has stopped or that it has not changed state from an earlier error. In these situations, you will want to

1. Enable [`debug` logging](/reference/fleet/monitor-elastic-agent.md#change-logging-level).
2. [Restart {{agent}}](/reference/fleet/agent-command-reference.md#elastic-agent-restart-command).
3. Wait 10 minutes for changes to sync from {{fleet}} server to {{agent}} and for it to restart.
4. Pull the {{agent}} diagnostic using prefered method.
5. Disable `debug` logging.
:::

## Collect {{agent}} diagnostics [agent-diagnostics-collect] 

{{agent}} comes bundled with a [`diagnostics` command](/reference/fleet/agent-command-reference.md#elastic-agent-diagnostics-command) which generates a zip archive containing troubleshooting diagnostic information. This export is intended only for debugging purposes and its structure can change between releases.

The {{fleet}} UI provides the ability to remotely generate and gather an {{agent}}'s diagnostics bundle if it is online in a [`Healthy` or `Unhealthy` status](/reference/fleet/monitor-elastic-agent.md#view-agent-status). For {{agent}}s in other statuses, you must use the CLI to grab their diagnostic.

:::{warning}
Diagnostics and logs mainly emit product metadata and settings, but they may expose sensitive data which needs to be redacted before being shared outside of your organization. See [Sanitize](#agent-diagnostics-sanitize)
:::

### Using the {{fleet}} UI [agent-diagnostics-ui]

The diagnostics are sent to {{fleet-server}} which in turn adds it into {{es}}. Therefore, this works even with {{agents}} that are not using the {{es}} output. To download the diagnostics bundle for local viewing:

1. In {{fleet}}, open the **Agents** tab.
2. In the **Host** column, click the agent’s name.
3. Select the **Diagnostics** tab and click the **Request diagnostics .zip** button.

    :::{image} /troubleshoot/images/fleet-collect-agent-diagnostics1.png
    :alt: Collect agent diagnostics under agent details
    :screenshot:
    :::

4. In the **Request Diagnostics** pop-up, select **Collect additional CPU metrics** if you’d like detailed CPU data.

    :::{image} /troubleshoot/images/fleet-collect-agent-diagnostics2.png
    :alt: Collect agent diagnostics confirmation pop-up
    :screenshot:
    :::

5. Click the **Request diagnostics** button.

When available, the new diagnostic bundle will be listed on this page, as well as any in-progress or previously collected bundles for the {{agent}}.

Note that the bundles are stored in {{es}} and are removed automatically after 7 days. You can also delete any previously created bundle by clicking the `trash can` icon.

### Using the CLI [agent-diagnostics-cli]

Run the [`diagnostics` command](/reference/fleet/agent-command-reference.md#elastic-agent-diagnostics-command) in the {{agent}}'s [install directory](/reference/fleet/installation-layout.md). For your convenience, we have outlined pulling the {{agent}} diagnostic with default install directory for the most common Operating Systems:

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

  2. Docker [`exec`](https://docs.docker.com/reference/cli/docker/container/exec/) run the diagnostic, replacing placeholder `CONTAINER_ID`.

    ```shell
    docker exec -it CONTAINER_ID elastic-agent diagnostics
    ```

    Take note of the output diagnostic filename and location. 

  3. Docker [`cp`](https://docs.docker.com/reference/cli/docker/container/cp/) the outputted diagnostic filename to your local machine, replacing placeholders `CONTAINER_ID` and `FILE_NAME`.

    ```shell
    docker cp CONTAINER_ID:/usr/share/elastic-agent/FILE_NAME FILE_NAME
    ```

* Kubernetes

  1. Determine the container ID with [`get`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/).

    ```shell
    kubectl get pods --all-namespaces | grep agent
    ```

  2. Run the diagnostic with [`exec`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_exec/), replacing placeholders `NAMESPACE` and `POD_NAME`.

    ```shell
    kubectl exec --stdin --tty POD_NAME -n NAMESPACE -- elastic-agent diagnostics
    ```

    Take note of the output diagnostic filename and location. 

  3. [`cp`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_cp/) the outputted diagnostic filename to your local machine, replacing placeholders `NAMESPACE`, `POD_NAME`. and `FILE_NAME`.

    ```shell
    kubectl cp NAMESPACE/POD_NAME:FILE_NAME FILE_NAME
    ```

### Sanitize [agent-diagnostics-sanitize]

{{agent}} attempts to automatically redact credentials and API keys when creating [its diagnostic files](/reference/fleet/agent-command-reference.md#elastic-agent-diagnostics-command). Review the contents of the archive before sharing to ensure that all forms of organizationally-private information is censored as needed. For example, ensure:

* There are no credentials in plain text in [its `*.yaml` diagnostic files](/reference/fleet/agent-command-reference.md#elastic-agent-diagnostics-command).

* The raw form of event's failing to output may show under `*.ndjson`. By default only `warn` log. When the `debug` logging level is enabled, all events are logged. If you want to omit the raw events from the diagnostic, add the flag `--exclude-events`.
