---
navigation_title: "Policies"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/agent-policy.html
---

# {{agent}} policies [agent-policy]


A policy is a collection of inputs and settings that defines the data to be collected by an {{agent}}. Each {{agent}} can only be enrolled in a single policy.

Within an {{agent}} policy is a set of individual integration policies. These integration policies define the settings for each input type. The available settings in an integration depend on the version of the integration in use.

{{fleet}} uses {{agent}} policies in two ways:

* Policies are stored in a plain-text YAML file and sent to each {{agent}} to configure its inputs.
* Policies provide a visual representation of an {{agent}}s configuration in the {{fleet}} UI.


## Policy benefits [policy-benefits]

{{agent}} policies have many benefits that allow you to:

* Apply a logical grouping of inputs aimed for a particular set of hosts.
* Maintain flexibility in large-scale deployments by quickly testing changes before rolling them out.
* Provide a way to group and manage larger swaths of your infrastructure landscape.

For example, it might make sense to create a policy per operating system type: Windows, macOS, and Linux hosts. Or, organize policies by functional groupings of how the hosts are used: IT email servers, Linux servers, user work-stations, etc. Or perhaps by user categories: engineering department, marketing department, etc.


## Policy types [agent-policy-types]

In most use cases, {{fleet}} provides complete central management of {{agent}}s. However some use cases, like running in Kubernetes or using {{ecloud}}, require {{agent}} infrastructure management outside of {{fleet}}. With this in mind, there are two types of {{agent}} policies:

* **regular policy**: The default use case, where {{fleet}} provides full central management for {{agent}}s. Users can manage {{agent}} infrastructure by adding, removing, or upgrading {{agent}}s. Users can also manage {{agent}} configuration by updating the {{agent}} policy.
* **hosted policy**: A policy where *something else* provides central management for {{agent}}s. For example, in Kubernetes, adding, removing, and upgrading {{agent}}s should be configured directly in Kubernetes. Allowing {{fleet}} users to manage {{agent}}s would conflict with any Kubernetes configuration.

    ::::{tip}
    Hosted policies also apply when using {{ech}}. {{ecloud}} is responsible for hosting {{agent}}s and assigning them to a policy. Platform operators, who create and manage Elastic deployments can add, upgrade, and remove {{agent}}s through the {{ecloud}} console.
    ::::


Hosted policies display a lock icon in the {{fleet}} UI, and actions are restricted. The following table illustrates the {{fleet}} user actions available to different policy types:

| {{fleet}} user action | Regular policy | Hosted policy |
| --- | --- | --- |
| [Create a policy](#create-a-policy) | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") |
| [Add an integration](#add-integration) | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") |
| [Apply a policy](#apply-a-policy) | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") |
| [Edit or delete an integration](#policy-edit-or-delete) | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") |
| [Copy a policy](#copy-policy) | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") |
| [Edit or delete a policy](#policy-main-settings) | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") |
| [Add custom fields](#add-custom-fields) | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") |
| [Configure agent monitoring](#change-policy-enable-agent-monitoring) | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") |
| [Change the output of a policy](#change-policy-output) | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") |
| [Add a {{fleet-server}} to a policy](#add-fleet-server-to-policy) | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") |
| [Configure secret values in a policy](#agent-policy-secret-values) | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") |
| [Set the maximum CPU usage](#agent-policy-limit-cpu) | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") |
| [Set the {{agent}} log level](#agent-policy-log-level) | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") |
| [Change the {{agent}} binary download location](#agent-binary-download-settings) | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") |
| [Set the {{agent}} host name format](#fleet-agent-hostname-format-settings) | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") |
| [Set an unenrollment timeout for inactive agents](#fleet-agent-unenrollment-timeout) | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") |

See also the [recommended scaling options](#agent-policy-scale) for an {{agent}} policy.


## Create a policy [create-a-policy]

To manage your {{agent}}s and the data they collect, create a new policy:

In {{fleet}}, open the **Agent policies** tab and click **Create agent policy**.

1. Name your policy. All other fields are optional and can be modified later. By default, each policy enables the *system* integration, which collects system information and metrics.
2. Create the agent policy:

    * To use the UI, click **Create agent policy**.
    * To use the {{fleet}} API, click **Preview API request** and run the request.


Also see [Create an agent policy without using the UI](/reference/ingestion-tools/fleet/create-policy-no-ui.md).


## Add an integration to a policy [add-integration]

An {{agent}} policy consists of one or more integrations that are applied to the agents enrolled in that policy. When you add an integration, the policy created for that integration can be shared with multiple {{agent}} policies. This reduces the number of integrations policies that you need to actively manage.

To add a new integration to one or more {{agent}} policies:

1. In {{fleet}}, click **Agent policies**. Click the name of a policy you want to add an integration to.
2. Click **Add <integration>**.
3. The Integrations page shows {{agent}} integrations along with other types, such as {{beats}}. Scroll down and select **Elastic Agent only** to view only integrations that work with {{agent}}.
4. You can opt to install an {{agent}} if you haven’t already, or choose **Add integration only** to proceed.
5. In Step 1 on the **Add <integration>** page, you can select the configuration settings specific to the integration.
6. In Step 2 on the page, you have two options:

    1. If you’d like to create a new policy for your {{agent}}s, on the **New hosts** tab specify a name for the new agent policy and choose whether or not to collect system logs and metrics. Collecting logs and metrics will add the System integration to the new agent policy.
    2. If you already have an {{agent}} policy created, on the **Existing hosts** tab use the drop-down menu to specify one or more agent policies that you’d like to add the integration to. Please note this this feature, known as "reusable integrations", requires an [Enterprise subscription](https://www.elastic.co/subscriptions).

7. Click **Save and continue** to confirm your settings.

This action installs the integration and adds it to the {{agent}} policies that you specified. {{fleet}} distributes the new integration policy to all {{agent}}s that are enrolled in the agent policies.

You can update the settings for an installed integration at any time:

1. In {{kib}}, go to the **Integrations** page.
2. On the **Integration policies** tab, for the integration that you like to update open the **Actions** menu and select **Edit integration**.
3. On the **Edit <integration>** page you can update any configuration settings and also update the list of {{agent}} polices to which the integration is added.

    If you clear the **Agent policies** field, the integration will be removed from any {{agent}} policies to which it had been added.

    To identify any integrations that have been "orphaned", that is, not associated with any {{agent}} policies, check the **Agent polices** column on the **Integration policies** tab. Any integrations that are installed but not associated with an {{agent}} policy are as labeled as `No agent policies`.



## Apply a policy [apply-a-policy]

You can apply policies to one or more {{agent}}s. To apply a policy:

1. In {{fleet}}, click **Agents**.
2. Select the {{agent}}s you want to assign to the new policy.

    After selecting one or more {{agent}}s, click **Assign to new policy** under the Actions menu.

    :::{image} images/apply-agent-policy.png
    :alt: Assign to new policy dropdown
    :class: screenshot
    :::

    Unable to select multiple agents? Confirm that your subscription level supports selective agent policy reassignment in {{fleet}}. For more information, refer to [{{stack}} subscriptions](https://www.elastic.co/subscriptions).

3. Select the {{agent}} policy from the dropdown list, and click **Assign policy**.

The {{agent}} status indicator and {{agent}} logs indicate that the policy is being applied. It may take a few minutes for the policy change to complete before the {{agent}} status updates to "Healthy".


## Edit or delete an integration policy [policy-edit-or-delete]

Integrations can easily be reconfigured or deleted. To edit or delete an integration policy:

1. In {{fleet}}, click **Agent policies**. Click the name of the policy you want to edit or delete.
2. Search or scroll to a specific integration. Open the **Actions** menu and select **Edit integration** or **Delete integration**.

    Editing or deleting an integration is permanent and cannot be undone. If you make a mistake, you can always re-configure or re-add an integration.


Any saved changes are immediately distributed and applied to all {{agent}}s enrolled in the given policy.

To update any secret values in an integration policy, refer to [Configure secret values in a policy](#agent-policy-secret-values).


## Copy a policy [copy-policy]

Policy definitions are stored in a plain-text YAML file that can be downloaded or copied to another policy:

1. In {{fleet}}, click **Agent policies**. Click the name of the policy you want to copy or download.
2. To copy a policy, click **Actions → Copy policy**. Name the new policy, and provide a description. The exact policy definition is copied to the new policy.

    Alternatively, view and download the policy definition by clicking **Actions → View policy**.



## Edit or delete a policy [policy-main-settings]

You can change high-level configurations like a policy’s name, description, default namespace, and agent monitoring status as necessary:

1. In {{fleet}}, click **Agent policies**. Click the name of the policy you want to edit or delete.
2. Click the **Settings** tab, make changes, and click **Save changes**

    Alternatively, click **Delete policy** to delete the policy. Existing data is not deleted. Any agents assigned to a policy must be unenrolled or assigned to a different policy before a policy can be deleted.



## Add custom fields [add-custom-fields]

Use this setting to add a custom field and value set to all data collected from the {{agents}} enrolled in an {{agent}} policy. Custom fields are useful when you want to identify or visualize all of the data from a group of agents, and possibly manipulate the data downstream.

To add a custom field:

1. In {{fleet}}, click **Agent policies**. Select the name of the policy you want to edit.
2. Click the **Settings** tab and scroll to **Custom fields**.
3. Click **Add field**.
4. Specify a field name and value.

    :::{image} images/agent-policy-custom-field.png
    :alt: Sceen capture showing the UI to add a custom field and value
    :class: screenshot
    :::

5. Click **Add another field** for additional fields. Click **Save changes** when you’re done.

To edit a custom field:

1. In {{fleet}}, click **Agent policies**. Select the name of the policy you want to edit.
2. Click the **Settings** tab and scroll to **Custom fields**. Any custom fields that have been configured are shown.
3. Click the edit icon to update a field or click the delete icon to remove it.

Note that adding custom tags is not supported for a small set of inputs:

* `apm`
* `cloudbeat` and all `cloudbeat/*` inputs
* `cloud-defend`
* `fleet-server`
* `pf-elastic-collector`, `pf-elastic-symbolizer`, and `pf-host-agent`
* `endpoint` inputs. Instead, use the advanced settings (`*.advanced.document_enrichment.fields`) of the {{elastic-defend}} Integration.


## Configure agent monitoring [change-policy-enable-agent-monitoring]

Use these settings to collect monitoring logs and metrics from {{agent}}. All monitoring data will be written to the specified **Default namespace**.

1. In {{fleet}}, click **Agent policies**. Select the name of the policy you want to edit.
2. Click the **Settings** tab and scroll to **Agent monitoring**.
3. Select whether to collect agent logs, agent metrics, or both, from the {{agents}} that use the policy.

    When this setting is enabled an {{agent}} integration is created automatically.

4. Expand the **Advanced monitoring options** section to access [advanced settings](#advanced-agent-monitoring-settings).
5. Save your changes for the updated monitoring settings to take effect.


### Advanced agent monitoring settings [advanced-agent-monitoring-settings]

**HTTP monitoring endpoint**

Enabling this setting exposes a `/liveness` API endpoint that you can use to monitor {{agent}} health according to the following HTTP codes:

* `200`: {{agent}} is healthy. The endpoint returns a `200` OK status as long as {{agent}} is responsive and can process configuration changes.
* `500`: A component or unit is in a failed state.
* `503`: The agent coordinator is unresponsive.

You can pass a `failon` parameter to the `/liveness` endpoint to determine what component state will result in a `500` status. For example, `curl 'localhost:6792/liveness?failon=degraded'` will return `500` if a component is in a degraded state.

The possible values for `failon` are:

* `degraded`: Return an error if a component is in a degraded state or failed state, or if the agent coordinator is unresponsive.
* `failed`: Return an error if a unit is in a failed state, or if the agent coordinator is unresponsive.
* `heartbeat`: Return an error only if the agent coordinator is unresponsive.

If no `failon` parameter is provided, the default `failon` behavior is `heartbeat`.

The HTTP monitoring endpoint can also be [used with Kubernetes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-a-liveness-http-request), to restart the container for example.

When you enable this setting, you need to provide the host URL and port where the endpoint can be accessed. Using the default `localhost` is recommended.

When the HTTP monitoring endpoint is enabled you can also select to **Enable profiling at `/debug/pprof`**. This controls whether the {{agent}} exposes the `/debug/pprof/` endpoints together with the monitoring endpoints.

The heap profiles available from `/debug/pprof/` are included in [{{agent}} diagnostics](/reference/ingestion-tools/fleet/agent-command-reference.md#elastic-agent-diagnostics-command) by default. CPU profiles are also included when the `--cpu-profile` option is included. For full details about the profiles exposed by `/debug/pprof/` refer to the [pprof package documentation](https://pkg.go.dev/net/http/pprof).

Profiling at `/debug/pprof` is disabled by default. Data produced by these endpoints can be useful for debugging but present a security risk. It’s recommended to leave this option disabled if the monitoring endpoint is accessible over a network.

**Diagnostics rate limiting**

You can set a rate limit for the action handler for diagnostics requests coming from {{fleet}}. The setting affects only {{fleet}}-managed {{agents}}. By default, requests are limited to an interval of `1m` and a burst value of `1`. This setting does not affect diagnostics collected through the CLI.

**Diagnostics file upload**

This setting configures retries for the file upload client handling diagnostics requests coming from {{fleet}}. The setting affects only {{fleet}}-managed {{agents}}. By default, a maximum of `10` retries are allowed with an initial duration of `1s` and a backoff duration of `1m`. The client may retry failed requests with exponential backoff.


## Change the output of a policy [change-policy-output]

Assuming your [{{stack}} subscription level](https://www.elastic.co/subscriptions) supports per-policy outputs, you can change the output of a policy to send data to a different output.

1. In {{fleet}}, click **Settings** and view the list of available outputs. If necessary, click **Add output** to add a new output with the settings you require. For more information, refer to [Output settings](/reference/ingestion-tools/fleet/fleet-settings.md#output-settings).
2. Click **Agent policies**. Click the name of the policy you want to change, then click **Settings**.
3. Set **Output for integrations** and (optionally) **Output for agent monitoring** to use a different output, for example, {{ls}}. You might need to scroll down to see these options.

    Unable to select a different output? Confirm that your subscription level supports per-policy outputs in {{fleet}}.

    :::{image} images/agent-output-settings.png
    :alt: Screen capture showing the {{ls}} output policy selected in an agent policy
    :class: screenshot
    :::

4. Save your changes.

Any {{agent}}s enrolled in the agent policy will begin sending data to the specified outputs.


## Add a {{fleet-server}} to a policy [add-fleet-server-to-policy]

If you want to connect multiple agents to a specific on-premises {{fleet-server}}, you can add that {{fleet-server}} to a policy.

:::{image} images/add-fleet-server-to-policy.png
:alt: Screen capture showing how to add a {{fleet-server}} to a policy when creating or updating the policy.
:class: screenshot
:::

When the policy is saved, all agents assigned to the policy are configured to use the new {{fleet-server}} as the controller.

Make sure that the {{agent}}s assigned to this policy all have connectivity to the {{fleet-server}} that you added. Lack of connectivity will prevent the {{agent}} from checking in with the {{fleet-server}} and receiving policy updates, but the agents will still forward data to the cluster.


## Configure secret values in a policy [agent-policy-secret-values]

When you create an integration policy you often need to provide sensitive information such as an API key or a password. To help ensure that data can’t be accessed inappropriately, any secret values used in an integration policy are stored separately from other policy details.

As well, after you’ve saved a secret value in {{fleet}}, the value is hidden in both the {{fleet}} UI and in the agent policy definition. When you view the agent policy (**Actions → View policy**), an environment variable is displayed in place of any secret values, for example `${SECRET_0}`.

::::{warning}
In order for sensitive values to be stored secretly in {{fleet}}, all configured {{fleet-server}}s must be on version 8.10.0 or higher.
::::


Though secret values stored in {{fleet}} are hidden, they can be updated. To update a secret value in an integration policy:

1. In {{fleet}}, click **Agent policies**. Select the name of the policy you want to edit.
2. Search or scroll to a specific integration. Open the **Actions** menu and select **Edit integration**. Any secret information is marked as being hidden.
3. Click the link to replace the secret value with a new one.

    :::{image} images/fleet-policy-hidden-secret.png
    :alt: Screen capture showing a hidden secret value as part of an integration policy
    :class: screenshot
    :::

4. Click **Save integration**. The original secret value is overwritten in the policy.


## Set the maximum CPU usage [agent-policy-limit-cpu]

You can limit the amount of CPU consumed by {{agent}}. This parameter limits the number of operating system threads that can be executing Go code simultaneously in each Go process. You can specify an integer value not less than `0`, which is the default value that stands for "all available CPUs".

This limit applies independently to the agent and each underlying Go process that it supervises. For example, if {{agent}} is configured to supervise two {{beats}} with a CPU usage limit of `2` set in the policy, then the total CPU limit is six, where each of the three processes (one {{agent}} and two {{beats}}) may execute independently on two CPUs.

This setting is similar to the {{beats}} [`max_procs`](beats://docs/reference/filebeat/configuration-general-options.md#_max_procs) setting. For more detail, refer to the [GOMAXPROCS](https://pkg.go.dev/runtime#GOMAXPROCS) function in the Go runtime documentation.

1. In {{fleet}}, click **Agent policies**. Select the name of the policy you want to edit.
2. Click the **Settings** tab and scroll to **Advanced settings**.
3. Set **Limit CPU usage** as needed. For example, to limit Go processes supervised by {{agent}} to two operating system threads each, set this value to `2`.


## Set the {{agent}} log level [agent-policy-log-level]

You can set the minimum log level that {{agents}} using the selected policy will send to the configured output. The default setting is `info`.

1. In {{fleet}}, click **Agent policies**. Select the name of the policy you want to edit.
2. Click the **Settings** tab and scroll to **Advanced settings**.
3. Set the **Agent logging level**.
4. Save your changes.

You can also set the log level for an individual agent:

1. In {{fleet}}, click **Agents**. Under the **Host** header, select the {{agent}} you want to edit.
2. On the **Logs** tab, set the **Agent logging level** and apply your changes. Or, you can choose to reset the agent to use the logging level specified in the agent policy.


## Change the {{agent}} binary download location [agent-binary-download-settings]

{{agent}}s must be able to access the {{artifact-registry}} to download binaries during upgrades. By default {{agent}}s download artifacts from the artifact registry at `https://artifacts.elastic.co/downloads/`.

For {{agent}}s that cannot access the internet, you can specify agent binary download settings, and then configure agents to download their artifacts from the alternate location. For more information about running {{agent}}s in a restricted environment, refer to [Air-gapped environments](/reference/ingestion-tools/fleet/air-gapped.md).

To change the binary download location:

1. In {{fleet}}, click **Agent policies**. Select the name of the policy you want to edit.
2. Click the **Settings** tab and scroll to **Agent binary download**.
3. Specify the address where you are hosting the artifacts repository or select the default to use the location specified in the {{fleet}} [agent binary download settings](/reference/ingestion-tools/fleet/fleet-settings.md#fleet-agent-binary-download-settings).


## Set the {{agent}} host name format [fleet-agent-hostname-format-settings]

The **Host name format** setting controls the format of information provided about the current host through the [host.name](/reference/ingestion-tools/fleet/host-provider.md) key, in events produced by {{agent}}.

1. In {{fleet}}, click **Agent policies**. Select the name of the policy you want to edit.
2. Click the **Settings** tab and scroll to **Host name format**.
3. Select one of the following:

    * **Hostname**: Information about the current host is in a non-fully-qualified format (`somehost`, rather than `somehost.example.com`). This is the default reporting format.
    * **Fully Qualified Domain Name (FQDN)**: Information about the current host is in FQDN format (`somehost.example.com` rather than `somehost`). This helps you to distinguish between hosts on different domains that have similar names. The fully qualified hostname allows each host to be more easily identified when viewed in {{kib}}, for example.

4. Save your changes.

::::{note}
FQDN reporting is not currently supported in APM.
::::


For FQDN reporting to work as expected, the hostname of the current host must either:

* Have a CNAME entry defined in DNS.
* Have one of its corresponding IP addresses respond successfully to a reverse DNS lookup.

If neither pre-requisite is satisfied, `host.name` continues to report the hostname of the current host in a non-fully-qualified format.


## Set an unenrollment timeout for inactive agents [fleet-agent-unenrollment-timeout]

You can configure a length of time after which any inactive {{agent}}s are automatically unenrolled and their API keys invalidated. This setting is useful when you have agents running in an ephemeral environment, such as Docker or {{k8s}}, and you want to prevent inactive agents from consuming unused API keys.

To configure an unenrollment timeout for inactive agents:

1. In {{fleet}}, click **Agent policies**. Select the name of the policy you want to edit.
2. Click the **Settings** tab and scroll to **Inactive agent unenrollment timeout**.
3. Specify an unenrollment timeout period in seconds.
4. Save your changes.

After you set an unenrollment timeout, any inactive agents are unenrolled automatically after the specified period of time. The unenroll task runs every ten minutes, and it unenrolls a maximum of one thousand agents at a time.


## Policy scaling recommendations [agent-policy-scale]

A single instance of {{fleet}} supports a maximum of 1000 {{agent}} policies. If more policies are configured, UI performance might be impacted. The maximum number of policies is not affected by the number of spaces in which the policies are used.

If you are using {{agent}} with [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md), the maximum supported number of {{agent}} policies is 500.
