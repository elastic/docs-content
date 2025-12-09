---
navigation_title: Common problems
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-troubleshooting.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Common problems with {{fleet}} and {{agent}} [fleet-troubleshooting]

We have collected the most common known problems and listed them here. If your problem is not described here, review the open issues in the following GitHub repositories:

| Repository | To review or report issues about |
| --- | --- |
| [elastic/kibana](https://github.com/elastic/kibana/issues) | {{fleet}} and {{integrations}} UI |
| [elastic/elastic-agent](https://github.com/elastic/elastic-agent/issues) | {{agent}} |
| [elastic/beats](https://github.com/elastic/beats/issues) | {{beats}} shippers |
| [elastic/fleet-server](https://github.com/elastic/fleet-server/issues) | {{fleet-server}} |
| [elastic/package-registry](https://github.com/elastic/package-registry/issues) | {{package-registry}} |
| [elastic/docs-content](https://github.com/elastic/docs-content/issues) | Documentation issues |

Have a question? Read our [FAQ](frequently-asked-questions.md), or contact us in the [discuss forum](https://discuss.elastic.co/). Your feedback is valuable to us.

Running {{agent}} standalone? Also refer to [Debug standalone {{agent}}s](/reference/fleet/debug-standalone-agents.md).


## Troubleshooting contents [troubleshooting-contents]

Find troubleshooting information for {{fleet}}, {{fleet-server}}, and {{agent}} in the following documentation:

* [{{agent}} unenroll fails](#deleted-policy-unenroll)
* [illegal_argument_exception when TSDB is enabled](#tsdb-illegal-argument)
* [{{agent}}s hosted on {{ecloud}} are stuck in `Updating` or `Offline`](#agents-in-cloud-stuck-at-updating)
* [When using {{ecloud}}, {{fleet-server}} is not listed in {{kib}}](#fleet-server-not-in-kibana-cloud)
* [The `/api/fleet/setup` endpoint can’t reach the package registry](#fleet-setup-fails)
* [{{kib}} cannot connect to {{package-registry}} in air-gapped environments](#fleet-errors-tls)
* [{{fleet}} in {{kib}} crashes](#fleet-app-crashes)
* [{{agent}} enrollment fails on the host with `x509: certificate signed by unknown authority` message](#agent-enrollment-certs)
* [{{agent}} enrollment fails on the host with `x509: cannot validate certificate for x.x.x.x because it doesn't contain any IP SANs` message](#es-enrollment-certs)
* [{{agent}} enrollment fails on the host with `Client.Timeout exceeded` message](#agent-enrollment-timeout)
* [Many {{fleet-server}} problems can be triaged and fixed with the below tips](#general-fleet-server-triage)
* [Retrieve the {{agent}} version](#trb-retrieve-agent-version)
* [Check the {{agent}} status](#trb-check-agent-status)
* [Collect {{agent}} diagnostics bundle](#trb-collect-agent-diagnostics)
* [Some problems occur so early that insufficient logging is available](#not-installing-no-logs-in-terminal)
* [The {{agent}} is cited as `Healthy` but still has set up problems sending data to {{es}}](#agent-healthy-but-no-data-in-es)
* [{{agent}} is stuck in status `Updating`](#fleet-agent-stuck-on-updating)
* [{{fleet-server}} is running and healthy with data, but other Agents cannot use it to connect to {{es}}](#secondary-agent-not-connecting)
* [{{es}} authentication service fails with `Authentication using apikey failed` message](#es-apikey-failed)
* [{{agent}} fails with `Agent process is not root/admin or validation failed` message](#process-not-root)
* [Integration policy upgrade has too many conflicts](#upgrading-integration-too-many-conflicts)
* [{{agent}} hangs while unenrolling](#agent-hangs-while-unenrolling)
* [{{agent}} is automatically unenrolled after failed check-ins with 401 errors](#agent-auto-unenroll-401)
* [On {{fleet-server}} startup, ERROR seen with `State changed to CRASHED: exited with code: 1`](#ca-cert-testing)
* [Uninstalling {{elastic-endpoint}} fails](#endpoint-not-uninstalled-with-agent)
* [API key is unauthorized to send telemetry to `.logs-endpoint.diagnostic.collection-*` indices](#endpoint-unauthorized)
* [Hosted {{agent}} is offline](#hosted-agent-offline)
* [APM & {{fleet}} fails to upgrade to 8.x on {{ecloud}}](#hosted-agent-8-x-upgrade-fail)
* [Air-gapped {{agent}} upgrade can fail due to an inaccessible PGP key](#pgp-key-download-fail)
* [{{agent}} upgrade fails on Windows with exit status `0xc0000142`](#agent-upgrade-fail-windows)
* [{{agents}} are unable to connect after removing the {{fleet-server}} integration](#fleet-server-integration-removed)
* [{{agent}} Out of Memory errors on Kubernetes](#agent-oom-k8s)
* [Error when running {{agent}} commands with `sudo`](#agent-sudo-error)
* [Troubleshoot {{agent}} installation on Kubernetes, with Kustomize](#agent-kubernetes-kustomize)
* [Troubleshoot {{agent}} on Kubernetes seeing `invalid api key to authenticate with fleet` in logs](#agent-kubernetes-invalid-api-key)


## {{agent}} unenroll fails [deleted-policy-unenroll]

In {{fleet}}, if you delete an {{agent}} policy that is associated with one or more inactive enrolled agents, when the agent returns back to a `Healthy` or `Offline` state, it cannot be unenrolled. Attempting to unenroll the agent results in an `Error unenrolling agent` message, and the unenrollment fails.

To resolve this problem, you can use the [{{kib}} {{fleet}} APIs](/reference/fleet/fleet-api-docs.md) to force unenroll the agent.

To uninstall a single {{agent}}:

```shell
POST kbn:/api/fleet/agents/<agent_id>/unenroll
{
  "force": true,
  "revoke": true
}
```

To bulk uninstall a set of {{agents}}:

```shell
POST kbn:/api/fleet/agents/bulk_unenroll
{ "agents": ["<agent_id1>", "<agent-id2>"],
  "force": true,
  "revoke": true
}
```

We are also updating the {{fleet}} UI to prevent removal of an {{agent}} policy that is currently associated with any inactive agents.


## illegal_argument_exception when TSDB is enabled [tsdb-illegal-argument]

When you use an {{agent}} integration in which TSDB (Time Series Database) is enabled, you may encounter an `illegal_argument_exception` error in the {{fleet}} UI.

This can occur if you have a component template defined that includes a `_source` attribute, which conflicts with the `_source: synthetic` setting used when TSDB is enabled.

For details about the error and how to resolve it, refer to the section `Runtime fields cannot be used in TSDB indices` in the Innovation Hub article [TSDB enabled integrations for {{agent}}](https://support.elastic.co/knowledge/9363b9fd).


## {{agent}}s hosted on {{ecloud}} are stuck in `Updating` or `Offline` [agents-in-cloud-stuck-at-updating]

In {{ecloud}}, after [upgrading](/reference/fleet/upgrade-integration.md) {{fleet-server}} and its integration policies, agents enrolled in the {{ecloud}} agent policy may experience issues updating. To resolve this problem:

1. In a terminal window, run the following `cURL` request, providing your {{kib}} superuser credentials to reset the {{ecloud}} agent policy.

    * On {{kib}} versions 8.11 and later, run:

        ```shell
        curl -u <username>:<password> --request POST \
          --url <kibana_url>/internal/fleet/reset_preconfigured_agent_policies/policy-elastic-agent-on-cloud \
          --header 'content-type: application/json' \
          --header 'kbn-xsrf: xyz' \
          --header 'elastic-api-version: 1'
        ```

    * On {{kib}} versions earlier than 8.11, run:

        ```shell
        curl -u <username>:<password> --request POST \
          --url <kibana_url>/internal/fleet/reset_preconfigured_agent_policies/policy-elastic-agent-on-cloud \
          --header 'content-type: application/json' \
          --header 'kbn-xsrf: xyz'
        ```

2. Force unenroll the agent stuck in `Updating`:

    1. To find agent’s ID, go to **{{fleet}} > Agents** and click the agent to see its details. Copy the Agent ID.
    2. In a terminal window, run:

        ```shell
        curl -u <username>:<password> --request POST \
          --url <kibana_url>/api/fleet/agents/<agentID>/unenroll \
          --header 'content-type: application/json' \
          --header 'kbn-xsrf: xx' \
          --data-raw '{"force":true,"revoke":true}' \
          --compressed
        ```

        Where `<agentID>` is the ID you copied in the previous step.

3. Restart the {{integrations-server}}:

    In the {{ecloud}} console under {{integrations-server}}, click **Force Restart**.



## When using {{ecloud}}, {{fleet-server}} is not listed in {{kib}} [fleet-server-not-in-kibana-cloud]

If you are unable to see {{fleet-server}} in {{kib}}, make sure it’s set up.

To set up {{fleet-server}} on {{ecloud}}:

1. Go to your deployment on {{ecloud}}.
2. Follow the {{ecloud}} prompts to set up **{{integrations-server}}**. Once complete, the {{fleet-server}} {{agent}} will show up in {{fleet}}.

To enable {{fleet}} and set up {{fleet-server}} on a self-managed cluster:

1. In the {{es}} configuration file, [`config/elasticsearch.yml`](/deploy-manage/stack-settings.md), set the following security settings to enable security and API keys:

    ```yaml
    xpack.security.enabled: true
    xpack.security.authc.api_key.enabled: true
    ```

2. In the {{kib}} configuration file, [`config/kibana.yml`](/deploy-manage/stack-settings.md), enable {{fleet}} and specify your user credentials:

    ```yaml
    xpack.encryptedSavedObjects.encryptionKey: "something_at_least_32_characters"
    elasticsearch.username: "my_username" <1>
    elasticsearch.password: "my_password"
    ```

    1. Specify a user who is authorized to use {{fleet}}.


    To set up passwords, you can use the documented {{es}} APIs or the `elasticsearch-setup-passwords` command. For example, `./bin/elasticsearch-setup-passwords auto`

    After running the command:

    1. Copy the Elastic user name to the {{kib}} configuration file.
    2. Restart {{kib}}.
    3. Follow the documented steps for setting up a self-managed {{fleet-server}}. For more information, refer to [What is {{fleet-server}}?](/reference/fleet/fleet-server.md).



## The `/api/fleet/setup` endpoint can’t reach the package registry [fleet-setup-fails]

To install {{integrations}}, the {{fleet}} app requires a connection to an external service called the {{package-registry}}.

For this to work, the {{kib}} server must connect to `https://epr.elastic.co` on port `443`.


## {{kib}} cannot connect to {{package-registry}} in air-gapped environments [fleet-errors-tls]

In air-gapped environments, you may encounter the following error if you’re using a custom Certificate Authority (CA) that is not available to {{kib}}:

```json
{"type":"log","@timestamp":"2022-03-02T09:58:36-05:00","tags":["error","plugins","fleet"],"pid":58716,"message":"Error connecting to package registry: request to https://customer.server.name:8443/categories?experimental=true&include_policy_templates=true&kibana.version=7.17.0 failed, reason: self signed certificate in certificate chain"}
```

To fix this problem, add your CA certificate file path to the {{kib}} startup file by defining the `NODE_EXTRA_CA_CERTS` environment variable. More information about this in [TLS configuration of the {{package-registry}}](/reference/fleet/air-gapped.md#air-gapped-tls) section.


## {{fleet}} in {{kib}} crashes [fleet-app-crashes]

1. To investigate the error, open your browser’s development console.
2. Select the **Network** tab, and refresh the page.

    One of the requests to the {{fleet}} API will most likely have returned an error. If the error message doesn’t give you enough information to fix the problem, contact us in the [discuss forum](https://discuss.elastic.co/).



## {{agent}} enrollment fails on the host with `x509: certificate signed by unknown authority` message [agent-enrollment-certs]

To ensure that communication with {{fleet-server}} is encrypted, {{fleet-server}} requires {{agent}}s to present a signed certificate. In a self-managed cluster, if you don’t specify certificates when you set up {{fleet-server}}, self-signed certificates are generated automatically.

If you attempt to enroll an {{agent}} in a {{fleet-server}} with a self-signed certificate, you will encounter the following error:

```sh
Error: fail to enroll: fail to execute request to fleet-server: x509: certificate signed by unknown authority
Error: enroll command failed with exit code: 1
```

To fix this problem, pass the `--insecure` flag along with the `enroll` or `install` command. For example:

```sh
sudo ./elastic-agent install --url=https://<fleet-server-ip>:8220 --enrollment-token=<token> --insecure
```

Traffic between {{agent}}s and {{fleet-server}} over HTTPS will be encrypted; you’re simply acknowledging that you understand that the certificate chain cannot be verified.

Allowing {{fleet-server}} to generate self-signed certificates is useful to get things running for development, but not recommended in a production environment.

For more information, refer to [Configure SSL/TLS for self-managed {{fleet-server}}s](/reference/fleet/secure-connections.md).


## {{agent}} enrollment fails on the host with `x509: cannot validate certificate for x.x.x.x because it doesn't contain any IP SANs` message [es-enrollment-certs]

To ensure that communication with {{es}} is encrypted, {{fleet-server}} requires {{es}} to present a signed certificate.

This error occurs when you use self-signed certificates with {{es}} using IP as a Common Name (CN). With IP as a CN, {{fleet-server}} looks into subject alternative names (SANs), which is empty. To work around this situation, use the `--fleet-server-es-insecure` flag to disable certificate verification.

You will also need to set `ssl.verification_mode: none` in the Output settings in {{fleet}} and {{integrations}} UI.


## {{agent}} enrollment fails on the host with `Client.Timeout exceeded` message [agent-enrollment-timeout]

To enroll in {{fleet}}, {{agent}} must connect to the {{fleet-server}} instance. If the agent is unable to connect, you see the following failure:

```txt
fail to enroll: fail to execute request to Fleet Server:Post http://fleet-server:8220/api/fleet/agents/enroll?: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)
```

Here are several steps to help you troubleshoot the problem.

1. Check for networking problems. From the host, run the `ping` command to confirm that it can reach the {{fleet-server}} instance.
2. Additionally, `curl` the `/status` API of {{fleet-server}}:

    ```shell
    curl -f http://<fleet-server-url>:8220/api/status
    ```

3. Verify that you have specified the correct {{kib}} {{fleet}} settings URL and port for your environment.

    By default, HTTPS protocol and port 8220 is expected by {{fleet-server}} to communicate with {{es}} unless you have explicitly set it otherwise.

4. Check that you specified a valid enrollment key during enrollment. To do this:

    1. In {{fleet}}, select **Enrollment tokens**.
    2. To view the secret, click the eyeball icon. The secret should match the string that you used to enroll {{agent}} on your host.
    3. If the secret doesn’t match, create a new enrollment token and use this token when you run the `elastic-agent enroll` command.



## Many {{fleet-server}} problems can be triaged and fixed with the below tips [general-fleet-server-triage]

::::{important}
When creating an issue or sending a support forum communication, this section can help you identify what is required.
::::


{{fleet-server}} allows {{agent}} to connect to {{es}}, which is the same as the connection to {{kib}} in prior releases. However, because {{fleet-server}} is on the edge host, it may result in additional networking setup and troubleshooting.


### Retrieve the {{agent}} version [trb-retrieve-agent-version]

1. If you installed the {{agent}}, run the following command (the example is for POSIX based systems):

    ```shell
    elastic-agent version
    ```

2. If you have not installed the {{agent}} and you are running it as a temporary process, you can run:

    ```shell
    ./elastic-agent version
    ```

    ::::{note}
    Both of the above commands are accessible via Windows or macOS with their OS-specific slight variation in how you call them. If needed, refer to [*Install {{agent}}s*](/reference/fleet/install-elastic-agents.md) for examples of how to adjust them.
    ::::



### Check the {{agent}} status [trb-check-agent-status]

Run the following command to view the current status of the {{agent}}.

```shell
elastic-agent status
```

Based on the information returned, you can take further action.

If {{agent}} is running, but you do not see what you expect, here are some items to review:

1. In {{fleet}}, click **Agents**. Check which policy is associated with the running {{agent}}. If it is not the policy you expected, you can change it.
2. In {{fleet}}, click **Agents**, and then select the {{agent}} policy. Check for the integrations that should be included.

    For example, if you want to include system data, make sure the **System** integration is included in the policy.

3. Confirm if the **Collect agent logs** and **Collect agent metrics** options are selected.

    1. In {{fleet}}, click **Agents**, and then select the {{agent}} policy.
    2. Select the **Settings** tab. If you want to collect agent logs or metrics, select these options.

        ::::{important}
        The **{{ecloud}} agent policy** is created only in {{ecloud}} deployments and, by default, does not include the collection of logs of metrics.
        ::::



### Collect {{agent}} diagnostics bundle [trb-collect-agent-diagnostics]

The {{agent}} diagnostics bundle collects the following information:

1. {{agent}} versions numbers
2. {{beats}} (and other process) version numbers and process metadata
3. Local configuration, elastic-agent policy, and the configuration that is rendered and passed to {{beats}} and other processes
4. {{agent}}'s local log files
5. {{agent}} and {{beats}} pprof profiles

Note that the diagnostics bundle is intended for debugging purposes only, its structure may change between releases.

::::{important}
{{agent}} attempts to automatically redact credentials and API keys when creating diagnostics. Review the contents of the archive before sharing to ensure that there are no credentials in plain text.
::::


::::{important}
The ZIP archive containing diagnostics information will include the raw events of documents sent to the {{agent}} output. By default, it will log only the failing events as `warn`. When the `debug` logging level is enabled, all events are logged. Review the contents of the archive before sharing to ensure that no sensitive information is included.
::::


**Get the diagnostics bundle using the CLI**

Run the [`diagnostics` command](/reference/fleet/agent-command-reference.md#elastic-agent-diagnostics-command) to generate a zip archive containing diagnostics information that the Elastic team can use for debugging cases:

```shell
elastic-agent diagnostics
```

If you want to omit the raw events from the diagnostic, add the flag `--exclude-events`.

**Get the diagnostics bundle through {{fleet}}**

{{fleet}} provides the ability to remotely generate and gather an {{agent}}'s diagnostics bundle. An agent can gather and upload diagnostics if it is online in a `Healthy` or `Unhealthy` state. The diagnostics are sent to {{fleet-server}} which in turn adds it into {{es}}. Therefore, this works even with {{agents}} that are not using the {{es}} output. To download the diagnostics bundle for local viewing:

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


## Some problems occur so early that insufficient logging is available [not-installing-no-logs-in-terminal]

If some problems occur early and insufficient logging is available, run the following command:

```shell
./elastic-agent install -f
```

The stand-alone install command installs the {{agent}}, and all of the service configuration is set up. You can now run the *enrollment* command. For example:

```shell
elastic-agent enroll --fleet-server-es=https://<es-url>:443 --fleet-server-service-token=<token> --fleet-server-policy=<policy-id>
```

Note: Port `443` is commonly used in {{ecloud}}. However, with self-managed deployments, your {{es}} may run on port `9200` or something entirely different.

For information on where to find agent logs, refer to our [FAQ](frequently-asked-questions.md#where-are-the-agent-logs).


## The {{agent}} is cited as `Healthy` but still has set up problems sending data to {{es}} [agent-healthy-but-no-data-in-es]

1. To confirm that the {{agent}} is running and its status is `Healthy`, select the **Agents** tab.

    If you previously selected the **Collect agent logs** option, you can now look at the agent logs.

2. Click the agent name and then select the **Logs** tab.

    If there are no logs displayed, it suggests a communication problem between your host and {{es}}. The possible reason for this is that the port is already in use.

3. You can check the port usage using tools like Wireshark or netstat. On a POSIX system, you can run the following command:

    ```shell
    netstat -nat | grep :8220
    ```

    Any response data indicates that the port is in use. This could be correct or not if you had intended to uninstall the {{fleet-server}}. In which case, re-check and continue.



## {{agent}} is stuck in status `Updating` [fleet-agent-stuck-on-updating]

Beginning in {{stack}} version 8.11, a stuck {{agent}} upgrade should be detected automatically, and you can [restart the upgrade](/reference/fleet/upgrade-elastic-agent.md#restart-upgrade-single) from {{fleet}}.


## {{fleet-server}} is running and healthy with data, but other Agents cannot use it to connect to {{es}} [secondary-agent-not-connecting]

Some settings are only used when you have multiple {{agent}}s.  If this is the case, it may help to check that the hosts can communicate with the {{fleet-server}}.

From the non-{{fleet-server}} host, run the following command:

```shell
curl -f http://<fleet-server-ip>:8220/api/status
```

The response may yield errors that you can be debug further, or it may work and show that communication ports and networking are not the problems.

One common problem is that the default {{fleet-server}} port of `8220` isn’t open on the {{fleet-server}} host to communicate. You can review and correct this using common tools in alignment with any networking and security concerns you may have.


## {{es}} authentication service fails with `Authentication using apikey failed` message [es-apikey-failed]

To save API keys and encrypt them in {{es}}, {{fleet}} requires an encryption key.

To provide an API key, in the [`kibana.yml`](/deploy-manage/stack-settings.md) configuration file, set the `xpack.encryptedSavedObjects.encryptionKey` property.

```yaml
xpack.encryptedSavedObjects.encryptionKey: "something_at_least_32_characters"
```


## {{agent}} fails with `Agent process is not root/admin or validation failed` message [process-not-root]

Ensure the user running {{agent}} has root privileges as some integrations require root privileges to collect sensitive data.

If you’re running {{agent}} in the foreground (and not as a service) on Linux or macOS, run the agent under the root user: `sudo` or `su`.

If you’re using the {{elastic-defend}} integration, make sure you’re running {{agent}} under the SYSTEM account.

::::{tip}
If you install {{agent}} as a service as described in [*Install {{agent}}s*](/reference/fleet/install-elastic-agents.md), {{agent}} runs under the SYSTEM account by default.
::::


To run {{agent}} under the SYSTEM account, you can do the following:

1. Download [PsExec](https://docs.microsoft.com/en-us/sysinternals/downloads/psexec) and extract the contents to a folder. For example, `d:\tools`.
2. Open a command prompt as an Administrator (right-click the command prompt icon and select **Run As Administrator**).
3. From the command prompt, run {{agent}} under the SYSTEM account:

    ```sh
    d:\tools\psexec.exe -sid "C:\Program Files\Elastic-Agent\elastic-agent.exe" run
    ```



## Integration policy upgrade has too many conflicts [upgrading-integration-too-many-conflicts]

If you try to upgrade an integration policy that is several versions old, there may be substantial conflicts or configuration issues. Rather than trying to fix these problems, it might be faster to create a new policy, test it, and roll out the integration upgrade to additional hosts.

After [upgrading the integration](/reference/fleet/upgrade-integration.md):

1. [Create a new policy](/reference/fleet/agent-policy.md#create-a-policy).
2. [Add the integration to the policy](/reference/fleet/agent-policy.md#add-integration). The newer version is automatically used.
3. [Apply the policy](/reference/fleet/agent-policy.md#apply-a-policy) to an {{agent}}.

    ::::{tip}
    In larger deployments, you should test integration upgrades on a sample {{agent}} before rolling out a larger upgrade initiative. Only after a small trial is deemed successful should the updated policy be rolled out all hosts.
    ::::

4. Roll out the integration update to additional hosts:

    1. In {{fleet}}, click **Agent policies**. Click on the name of the policy you want to edit.
    2. Search or scroll to a specific integration. Open the **Actions** menu and select **Delete integration**.
    3. Click **Add integration** and re-add the freshly deleted integration. The updated version will be used and applied to all {{agent}}s.
    4. Repeat this process for each policy with the out-of-date integration.

        ::::{note}
        In some instances, for example, when there are hundreds or thousands of different {{agent}}s and policies that need to be updated, this upgrade path is not feasible. In this case, update one policy and use the [Copy a policy](/reference/fleet/agent-policy.md#copy-policy) action to apply the updated policy versions to additional policies. This method’s downside is losing the granularity of assessing the individual Integration version changes individually across policies.
        ::::



## {{agent}} hangs while unenrolling [agent-hangs-while-unenrolling]

When unenrolling {{agent}}, {{fleet}} waits for acknowledgment from the agent before it completes the unenroll process. If {{fleet}} doesn’t receive an acknowledgment, the status hangs at `unenrolling.`

You can unenroll an agent to invalidate all API keys related to the agent and change the status to `inactive` so that the agent no longer appears in {{fleet}}.

1. In {{fleet}}, select **Agents**.
2. Under Agents, choose **Unenroll agent** from the **Actions** menu next to the agent you want to unenroll.
3. Click **Force unenroll**.


## {{agent}} is automatically unenrolled after failed check-ins with 401 errors [agent-auto-unenroll-401]

In {{agent}} versions prior to 8.19.0 and 9.1.0, if an agent receives a 401 (Unauthorized) error on more than seven consecutive check-ins with {{fleet-server}}, the agent is automatically unenrolled.

To resolve the issue:

1. Re-enroll the agent that has been automatically unenrolled from {{fleet}}:

     1. If the agent is still installed on the host, uninstall it completely. Refer to [Uninstall {{agents}} from edge hosts](/reference/fleet/uninstall-elastic-agent.md) for detailed instructions.

     2. Reinstall and enroll the agent with a new enrollment token. Refer to [Install {{agents}}](/reference/fleet/install-elastic-agents.md) for detailed instructions.

2. Investigate the cause of the 401 errors, and resolve the underlying issues to ensure proper agent functionality.

    401 errors during check-in typically indicate authentication or authorization problems. Common causes include:

    * Expired or revoked API keys
    * Incorrect {{fleet-server}} configuration
    * Issues with {{es}} authentication settings

:::{admonition} Agents are no longer automatically unenrolled
:applies_to: stack: ga 8.19.0, ga 9.1.0

The automatic unenrollment behavior is removed in {{agent}} versions 8.19.0 and 9.1.0. Starting with these versions, {{agents}} are no longer automatically unenrolled due to repeated 401 errors during check-in.
:::

## On {{fleet-server}} startup, ERROR seen with `State changed to CRASHED: exited with code: 1` [ca-cert-testing]

You may see this error message for a number of different reasons. A common reason is when attempting production-like usage and the ca.crt file passed in cannot be found.  To verify if this is the problem, bootstrap {{fleet-server}} without passing a ca.crt file. This implies you would test any subsequent {{agent}} installs temporarily with {{fleet-server}}'s own self-signed cert.

::::{tip}
Ensure to pass in the full path to the ca.crt file. A relative path is not viable.
::::


You will know if your {{fleet-server}} is set up with its testing oriented self-signed certificate usage, when you see the following error during {{agent}} installs:

```sh
Error: fail to enroll: fail to execute request to fleet-server: x509: certificate signed by unknown authority
Error: enroll command failed with exit code: 1
```

To install or enroll against a self-signed cert {{fleet-server}} {{agent}}, add in the `--insecure` option to the command:

```sh
sudo ./elastic-agent install --url=https://<fleet-server-ip>:8220 --enrollment-token=<token> --insecure
```

For more information, refer to [{{agent}} enrollment fails on the host with `x509: certificate signed by unknown authority` message](#agent-enrollment-certs).


## Uninstalling {{elastic-endpoint}} fails [endpoint-not-uninstalled-with-agent]

When you uninstall {{agent}}, all the programs managed by {{agent}}, such as {{elastic-endpoint}}, are also removed. If uninstalling fails, {{elastic-endpoint}} might remain on your system.

To remove {{elastic-endpoint}}, run the following commands:

:::::::{tab-set}

::::::{tab-item} macOS
```shell
cd /tmp
cp /Library/Elastic/Endpoint/elastic-endpoint elastic-endpoint
sudo ./elastic-endpoint uninstall
rm elastic-endpoint
```
::::::

::::::{tab-item} Linux
```shell
cd /tmp
cp /opt/Elastic/Endpoint/elastic-endpoint elastic-endpoint
sudo ./elastic-endpoint uninstall
rm elastic-endpoint
```
::::::

::::::{tab-item} Windows
```shell
cd %TEMP%
copy "c:\Program Files\Elastic\Endpoint\elastic-endpoint.exe" elastic-endpoint.exe
.\elastic-endpoint.exe uninstall
del .\elastic-endpoint.exe
```
::::::

:::::::

## API key is unauthorized to send telemetry to `.logs-endpoint.diagnostic.collection-*` indices [endpoint-unauthorized]

By default, telemetry is turned on in the {{stack}} to helps us learn about the features that our users are most interested in. This helps us to focus our efforts on making features even better.

If you’ve recently upgraded from version `7.10` to `7.11`, you might see the following message when you view {{elastic-defend}} logs:

```sh
action [indices:admin/auto_create] is unauthorized for API key id [KbvCi3YB96EBa6C9k2Cm]
of user [fleet_enroll] on indices [.logs-endpoint.diagnostic.collection-default]
```

The above message indicates that {{elastic-endpoint}} does not have the correct permissions to send telemetry. This is a known problem in 7.11 that will be fixed in an upcoming patch release.

To remove this message from your logs, you can turn off telemetry for the {{elastic-defend}} integration until the next patch release is available.

1. In {{kib}}, click **Integrations**, and then select the **Manage** tab.
2. Click **{{elastic-defend}}**, and then select the **Policies** tab to view all the installed integrations.
3. Click the integration to edit it.
4. Under advanced settings, set `windows.advanced.diagnostic.enabled` to `false`, and then save the integration.


## Hosted {{agent}} is offline [hosted-agent-offline]

To scale the {{fleet-server}} deployment, {{ecloud}} starts new containers or shuts down old ones when hosted {{agent}}s are required or no longer needed. The old {{agent}}s will show in the Agents list for 24 hours then automatically disappear.


## {{agent}} fails to enroll with {{fleet-server}} running on localhost. [mac-file-sharing]

If you’re testing {{fleet-server}} locally on a macOS system using localhost (`https://127.0.0.1:8220`) as the Host URL, you may encounter this error:

```sh
Error: fail to enroll: fail to execute request to fleet-server:
lookup My-MacBook-Pro.local: no such host
```

This can occur on newer macOS software. To resolve the problem, [ensure that file sharing is enabled](https://support.apple.com/en-ca/guide/mac-help/mh17131/mac) on your local system.


## APM & {{fleet}} fails to upgrade to 8.x on {{ecloud}} [hosted-agent-8-x-upgrade-fail]

In some scenarios, upgrading APM & {{fleet}} to 8.x may fail if the {{ecloud}} agent policy was modified manually. The {{fleet}} app in {{kib}} may show a message like:

```sh
Unable to create package policy. Package 'apm' already exists on this agent policy
```

To work around this problem, you can reset the {{ecloud}} agent policy with an API call. Note that this will remove any custom integration policies that you’ve added to the policy, such as Synthetics monitors.

```sh
curl -u elastic:<password> --request POST \
  --url <kibana_url>/internal/fleet/reset_preconfigured_agent_policies/policy-elastic-agent-on-cloud \
  --header 'Content-Type: application/json' \
  --header 'kbn-xsrf: xyz'
```


## Air-gapped {{agent}} upgrade can fail due to an inaccessible PGP key [pgp-key-download-fail]

In versions 8.9 and above, an {{agent}} upgrade may fail when the upgrader can’t access a PGP key required to verify the binary signature. For details and a workaround, refer to the [PGP key download fails in an air-gapped environment](https://www.elastic.co/guide/en/fleet/8.9/release-notes-8.9.0.html#known-issue-3375) known issue in the version 8.9.0 Release Notes or to the [workaround documentation](https://github.com/elastic/elastic-agent/blob/main/docs/pgp-workaround.md) in the elastic-agent GitHub repository.


## {{agent}} upgrade fails on Windows with exit status `0xc0000142` [agent-upgrade-fail-windows]

During an {{agent}} upgrade on Windows, {{agent}} spawns a "watcher" process that monitors the upgrade process. Windows attempts to create a temporary console for this process. If Windows can't create this console, the watcher process initialization fails with error code `0xc0000142` (`STATUS_DLL_INIT_FAILED`), resulting in an upgrade failure. {{agent}} logs this error at the `info` level.

The error is caused by Windows [desktop heap exhaustion](https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/desktop-heap-limitation-out-of-memory). When {{agent}} runs as a [Windows service application](https://learn.microsoft.com/en-us/dotnet/framework/windows-services/introduction-to-windows-service-applications), it uses the service desktop, and shares the desktop heap with other running services. If a service process is using windowing resources, but is failing to release them, this may exhaust the desktop heap and affect {{agent}}.

:::{note}
Interactively-run instances of `elastic-agent.exe` are not subject to this limitation. Only instances running as a service are potentially affected.
:::

To resolve the issue, you can try the following:

- **Update {{agent}} immediately after a system reboot**

    A system reboot destroys and recreates the desktop heap, resolving any prior exhaustion.
    Because many memory leaks are gradual, updating {{agent}} immediately after a system reboot may allow {{agent}} to upgrade before the memory leaking application exhausts the desktop heap.

    :::{tip}
    A [cold startup](https://learn.microsoft.com/en-us/windows-hardware/drivers/kernel/distinguishing-fast-startup-from-wake-from-hibernation) resets kernel memory, but a fast startup or a wake from hibernation does not.
    A regular reboot (for example, `shutdown /r /t 0`) results in a cold startup, and resets the desktop heap.
    :::

- **Update third-party service applications**

    As standard Windows tools such as Task Manager and Process Explorer do not attribute desktop heap usage by application, you have to consider updating all third-party processes that are running as a service. To list these applications, use the following PowerShell command:

    ```powershell
    PS C:\> Get-Process | Where {$_.SI -eq 0} | Where {$_.MainModule.FileVersionInfo.ProductName -and (-not (($_.MainModule.FileVersionInfo.CompanyName -eq "Microsoft Corporation") -and ($_.MainModule.FileVersionInfo.ProductName -like "*Windows*"))) } | ForEach-Object { $_.MainModule.FileVersionInfo.ProductName + ' - ' + $_.Path }
    ```

    You can then install any updates from the listed applications' manufacturers.

- **Terminate or uninstall third-party service applications**

    You can try terminating or uninstalling non-critical third-party service applications before updating {{agent}}.
    Terminating a process releases its desktop heap resources.

    Note that the {{agent}} update process does not require a significant amount of desktop heap resources, so a successful {{agent}} update following the termination or uninstallation of a service application does not necessarily mean that the application was exhausting the desktop heap.

- **Resize the desktop heap**

    As a short-term solution, follow the steps described in the [Microsoft guide](https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/desktop-heap-limitation-out-of-memory) to increase the size of the desktop heap. Note that if a service application is causing a memory leak, increasing the size of the desktop heap may only postpone the desktop heap exhaustion.


## {{agents}} are unable to connect after removing the {{fleet-server}} integration [fleet-server-integration-removed]

When you use {{fleet}}-managed {{agent}}, at least one {{agent}} needs to be running the [{{fleet-server}} integration](https://docs.elastic.co/integrations/fleet_server). In case the policy containing this integration is accidentally removed from {{agent}}, all other agents will not be able to be managed. However, the {{agents}} will continue to send data to their configured output.

There are two approaches to fixing this issue, depending on whether or not the the {{agent}} that was running the {{fleet-server}} integration is still installed and healthy (but is now running another policy).

To recover the {{agent}}:

1. In {{fleet}}, open the **Agents** tab and click **Add agent**.
2. In the **Add agent** flyout, select an agent policy that contains the **Fleet Server** integration. On Elastic Cloud you can use the **Elastic Cloud agent policy** which includes the integration.
3. Follow the instructions in the flyout, and stop before running the CLI commands.
4. Depending on the state of the original {{fleet-server}} {{agent}}, do one of the following:

    * **The original {{fleet-server}} {{agent}} is still running and healthy**

        In this case, you only need to re-enroll the agent with {{fleet}}:

        1. Copy the `elastic-agent install` command from the {{kib}} UI.
        2. In the command, replace `install` with `enroll`.
        3. In the directory where {{agent}} is running (for example `/opt/Elastic/Agent/` on Linux), run the command as `root`.

            For example, if {{kib}} gives you the command:

            ```sh
            sudo ./elastic-agent install --url=https://fleet-server:8220 --enrollment-token=bXktc3VwZXItc2VjcmV0LWVucm9sbWVudC10b2tlbg==
            ```

            Instead run:

            ```sh
            sudo ./elastic-agent enroll --url=https://fleet-server:8220 --enrollment-token=bXktc3VwZXItc2VjcmV0LWVucm9sbWVudC10b2tlbg==
            ```

    * **The original {{fleet-server}} {{agent}} is no longer installed**

        In this case, you need to install the agent again:

        1. Copy the commands from the {{kib}} UI. The commands don’t need to be changed.
        2. Run the commands in order. The first three commands will download a new {{agent}} install package, expand the archive, and change directories.

            The final command will install {{agent}}. For example:

            ```sh
            sudo ./elastic-agent install --url=https://fleet-server:8220 --enrollment-token=bXktc3VwZXItc2VjcmV0LWVucm9sbWVudC10b2tlbg==
            ```


After running these steps your {{agents}} should be able to connect with {{fleet}} again.


## {{agent}} Out of Memory errors on Kubernetes [agent-oom-k8s]

In a Kubernetes environment, {{agent}} may be terminated with reason `OOMKilled` due to inadequate available memory.

To detect the problem, run the `kubectl describe pod` command and check the results for the following content:

```sh
       Last State:   Terminated
       Reason:       OOMKilled
       Exit Code:    137
```

To resolve the problem, allocate additional memory to the agent and then restart it.


## Error when running {{agent}} commands with `sudo` [agent-sudo-error]

On Linux systems, when you install {{agent}} [without administrative privileges](/reference/fleet/elastic-agent-unprivileged.md), that is, using the `--unprivileged` flag, {{agent}} commands should not be run with `sudo`. Doing so may result in an error due to the agent not having the required privileges.

For example, when you run {{agent}} with the `--unprivileged` flag, running the `elastic-agent inspect` command will result in an error like the following:

```sh
Error: error loading agent config: error loading raw config: fail to read configuration /Library/Elastic/Agent/fleet.enc for the elastic-agent: fail to decode bytes: cipher: message authentication failed
```

To resolve this, either install {{agent}} without the `--unprivileged` flag so that it has administrative access, or run the {{agent}} commands without the `sudo` prefix.


## Troubleshoot {{agent}} installation on Kubernetes, with Kustomize [agent-kubernetes-kustomize]

Potential issues during {{agent}} installation on Kubernetes can be categorized into two main areas:

1. [Problems related to the creation of objects within the manifest](#agent-kustomize-manifest).
2. [Failures occurring within specific components after installation](#agent-kustomize-after).


### Problems related to the creation of objects within the manifest [agent-kustomize-manifest]

When troubleshooting installations performed with [Kustomize](https://github.com/kubernetes-sigs/kustomize), it’s good practice to inspect the output of the rendered manifest. To do this, take the installation command provided by Kibana Onboarding and replace the final part, `| kubectl apply -f-`, with a redirection to a local file. This allows for easier analysis of the rendered output.

For example, the following command, originally provided by {{kib}} for an {{agent}} Standalone installation, has been modified to redirect the output for troubleshooting purposes:

```sh
kubectl kustomize https://github.com/elastic/elastic-agent/deploy/kubernetes/elastic-agent-kustomize/default/elastic-agent-standalone\?ref\=v8.15.3 | sed -e 's/JUFQSV9LRVkl/ZDAyNnZaSUJ3eWIwSUlCT0duRGs6Q1JfYmJoVFRUQktoN2dXTkd0FNMtdw==/g' -e "s/%ES_HOST%/https:\/\/7a912e8674a34086eacd0e3d615e6048.us-west2.gcp.elastic-cloud.com:443/g" -e "s/%ONBOARDING_ID%/db687358-2c1f-4ec9-86e0-8f1baa4912ed/g" -e "s/\(docker.elastic.co\/beats\/elastic-agent:\).*$/\18.15.3/g" -e "/{CA_TRUSTED}/c\ " > elastic_agent_installation_complete_manifest.yaml
```

The previous command generates a local file named `elastic_agent_installation_complete_manifest.yaml`, which you can use for further analysis. It contains the complete set of resources required for the {{agent}} installation, including:

* RBAC objects (`ServiceAccounts`, `Roles`, etc.)
* `ConfigMaps` and `Secrets` for {{agent}} configuration
* {{agent}} Standalone deployed as a `DaemonSet`
* [Kube-state-metrics](https://github.com/kubernetes/kube-state-metrics) deployed as a `Deployment`

The content of this file is equivalent to what you’d obtain by following the [Run {{agent}} Standalone on Kubernetes](/reference/fleet/running-on-kubernetes-standalone.md) steps, with the exception that `kube-state-metrics` is not included in the standalone method.

**Possible issues**

* If your user doesn’t have **cluster-admin** privileges, the RBAC resources creation might fail.
* Some Kubernetes security mechanisms (like [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)) could cause part of the manifest to be rejected, as `hostNetwork` access and `hostPath` volumes are required.
* If you already have an installation of `kube-state-metrics`, it could cause part of the manifest installation to fail or to update your existing resources without notice.


### Failures occurring within specific components after installation [agent-kustomize-after]

If the installation is correct and all resources are deployed, but data is not flowing as expected (for example, you don’t see any data on the **[Metrics Kubernetes] Cluster Overview** dashboard), check the following items:

1. Check resources status and ensure they are all in a `Running` state:

    ```sh
    kubectl get pods -n kube-system | grep elastic
    kubectl get pods -n kube-system | grep kube-state-metrics
    ```

    ::::{note}
    The default configuration assumes that both `kube-state-metrics` and the {{agent}} `DaemonSet` are deployed in the **same namespace** for communication purposes. If you change the namespace of any of the components, the agent configuration will need further policy updates.

    ::::

2. Describe the Pods if they are in a `Pending` state:

    ```sh
    kubectl describe -n kube-system <name_of_elastic_agent_pod>
    ```

3. Check the logs of elastic-agents and kube-state-metrics, and look for errors or warnings:

    ```sh
    kubectl logs -n kube-system <name_of_elastic_agent_pod>
    kubectl logs -n kube-system <name_of_elastic_agent_pod> | grep -i error
    kubectl logs -n kube-system <name_of_elastic_agent_pod> | grep -i warn
    ```

    ```sh
    kubectl logs -n kube-system <name_of_kube-state-metrics_pod>
    ```


**Possible issues**

* Connectivity, authorization, or authentication issues when connecting to {{es}}:

    Ensure the API Key and {{es}} destination endpoint used during the installation is correct and is reachable from within the Pods.

    In an already installed system, the API Key is stored in a `Secret` named `elastic-agent-creds-<hash>`, and the endpoint is configured in the `ConfigMap` `elastic-agent-configs-<hash>`.

* Missing cluster-level metrics (provided by `kube-state-metrics`):

    As described in [Run {{agent}} Standalone on Kubernetes](/reference/fleet/running-on-kubernetes-standalone.md), the {{agent}} Pod acting as `leader` is responsible for retrieving cluster-level metrics from `kube-state-metrics` and delivering them to [data streams](../../../manage-data/data-store/data-streams.md) prefixed as `metrics-kubernetes.state_<resource>`. In order to troubleshoot a situation where these metrics are not appearing:

    1. Determine which Pod owns the [leadership](/reference/fleet/kubernetes_leaderelection-provider.md) `lease` in the cluster, with:

        ```sh
        kubectl get lease -n kube-system elastic-agent-cluster-leader
        ```

    2. Check the logs of that Pod to see if there are errors when connecting to `kube-state-metrics` and if the `state_*` metrics are being sent to {{es}}.

        One way to check if `state_*` metrics are being delivered to {{es}} is to inspect log lines with the `"Non-zero metrics in the last 30s"` message and check the values of the `state_*` metrics within the line, with something like:

        ```sh
        kubectl logs -n kube-system elastic-agent-xxxx | grep "Non-zero metrics" | grep "state_"
        ```

        If the previous command returns `"state_pod":{"events":213,"success":213}` or similar for all `state_*` metrics, it means the metrics are being delivered.

    3. As a last resort, if you believe none of the Pods is acting as a leader, you can try deleting the `lease` to generate a new one:

        ```sh
        kubectl delete lease -n kube-system elastic-agent-cluster-leader
        # wait a few seconds and check for the lease again
        kubectl get lease -n kube-system elastic-agent-cluster-leader
        ```

* Performance problems:

    Monitor the CPU and Memory usage of the agents Pods and adjust the manifest requests and limits as needed. Refer to [Scaling {{agent}} on {{k8s}}](/reference/fleet/scaling-on-kubernetes.md) for more details about the needed resources.


Extra resources for {{agent}} on Kubernetes troubleshooting and information:

* [{{agent}} Out of Memory errors on Kubernetes](#agent-oom-k8s).
* [{{agent}} Kustomize Templates](https://github.com/elastic/elastic-agent/tree/main/deploy/kubernetes/elastic-agent-kustomize/default) documentation and resources.
* Other examples and manifests to deploy [{{agent}} on Kubernetes](https://github.com/elastic/elastic-agent/tree/main/deploy/kubernetes).


## Troubleshoot {{agent}} on Kubernetes seeing `invalid api key to authenticate with fleet` in logs [agent-kubernetes-invalid-api-key]

If an agent was unenrolled from a Kubernetes cluster, there might be data remaining in `/var/lib/elastic-agent-managed/kube-system/state` on the node(s). Reenrolling an agent later on the same nodes might then result in `invalid api key to authenticate with fleet` error messages.

To avoid these errors, make sure to delete this state-folder before enrolling a new agent.

For more information, refer to issue [#3586](https://github.com/elastic/elastic-agent/issues/3586).
