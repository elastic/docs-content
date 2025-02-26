---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-faq.html
---

# Frequently asked questions [fleet-faq]

We have collected the most frequently asked questions here. If your question isn’t answered here, contact us in the [discuss forum](https://discuss.elastic.co/). Your feedback is very valuable to us.

Also read [Troubleshoot common problems](common-problems.md).

* [Why doesn’t my enrolled agent show up in the {{fleet}} app?](#enrolled-agent-not-showing-up)
* [Where does {{agent}} store logs after startup?](#where-are-the-agent-logs)
* [What policy is the {{agent}} running?](#what-is-my-agent-config)
* [Why can’t I see the data {{agent}} is sending?](#where-is-the-data-agent-is-sending)
* [How do I restore an {{agent}} that I deleted from {{fleet}}?](#i-deleted-my-agent)
* [How do I restart {{agent}} after rebooting my host?](#i-rebooted-my-host)
* [Does {{agent}} or {{kib}} download integration packages?](#does-agent-download-packages)
* [Does {{agent}} download anything from the Internet?](#does-agent-download-anything-from-internet)
* [Do I need to set up the {{beats}} managed by {{agent}}?](#do-i-need-to-setup-elastic-agent)
* [What is the {{elastic-defend}} integration in {{fleet}}?](#what-is-the-endpoint-package)
* [How are communications secured between {{elastic-sec}} and {{agent}}?](#how-are-security-to-agent-communications-secured)
* [How are secrets secured when entered into integration policies or agent policies in {{kib}}?](#how-are-secrets-secured)
* [Which {{es}} and {{kib}} ports need to be accessible?](#which-es-kibana-ports-are-needed)
* [If I delete an integration dashboard asset from {{kib}}, how do I get it back?](#how-do-i-reinstall-a-missing-dashboard-asset)


## Why doesn’t my enrolled agent show up in the {{fleet}} app? [enrolled-agent-not-showing-up]

If {{agent}} was successfully enrolled, but doesn’t show up in the **Agents** list, it might not be started. Make sure the `elastic-agent` process is running on the host. If it’s not running, use the [`run`](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/agent-command-reference.md#elastic-agent-run-command) command to start it.  The most common way to deploy an {{agent}} is by using the `install` command. This command starts the {{agent}} for you.


## Where does {{agent}} store logs after startup? [where-are-the-agent-logs]

The location of {{agent}} logs varies by platform. In general, {{agent}} stores logs under the `data` directory where {{agent}} was started. For example, on macOS, you’ll find logs for the running {{agent}} under path similar to:

`/Library/Elastic/Agent/data/elastic-agent-08e204/logs/elastic-agent-20220105.ndjson`

You’ll find logs for the {{beats}} shippers, such as {{metricbeat}}, under paths like:

`/Library/Elastic/Agent/data/elastic-agent-08e204/logs/default/metricbeat-20220105.ndjson`

If the log path does not exist, {{agent}} was unable to start {{metricbeat}}, which is a higher level problem to triage. Usually you can see these logs in the {{fleet}} UI, unless there are problems severe enough that the {{agent}} or its related  processes cannot send data to {{es}}.

See [Installation layout](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/installation-layout.md) to find out the exact paths for each platform.


## What policy is the {{agent}} running? [what-is-my-agent-config]

To find the policy file, inspect the `elastic-agent.yml` file in the directory where {{agent}} is running. Not sure where the agent is running? See [Installation layout](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/installation-layout.md).

If the agent is running in {{fleet}} mode, this file contains the following citation:

```yaml
fleet:
  enabled: true
```

The `state.yml` file (located under `data/elastic-agent-*`) contains the entire, unencrypted policy.

* To see the {{es}} location, look at the `hosts` setting under `outputs`. For example:

    ```json
    outputs:
      default:
        api_key: Aq-mPpcBDA7TmnriKCSD:Np6NAleNQ1mMpgN_JPYazw
        hosts:
        - https://3m63533c175a4036b3d8bbe7bd462fa3.us-east-1.aws.found.io:443
        type: elasticsearch
    ```

    This file also shows the version of all packages used by the current policy.

* To see the {{agent}} version, run:

    ```shell
    elastic-agent version
    ```



## Why can’t I see the data {{agent}} is sending? [where-is-the-data-agent-is-sending]

If {{elastic-agent}} is set up and running, but you don’t see data in {{kib}}:

1. Go to **Management > {{dev-tools-app}}** in {{kib}}, and in the Console, search your index for data. For example:

    ```console
    GET metrics-*/_search
    ```

    Or if you prefer, go to the **Discover** app.

2. Look at the data that {{elastic-agent}} has sent and see if the `name.host` field contains your host machine name.

If you don’t see data for your host, it’s possible that the data is blocked in the network, or that a firewall or security problem is preventing the {{agent}} from sending the data.

Although it’s redundant to install stand-alone {{metricbeat}}, you might want to try installing it to see if it’s able to send data successfully to {{es}}. For more information, see [{{metricbeat}} quick start](asciidocalypse://docs/beats/docs/reference/metricbeat/metricbeat-installation-configuration.md).

If {{metricbeat}} is able to send data to {{es}}, there is possibly a bug or problem with {{agent}}, and you should report it.


## How do I restore an {{agent}} that I deleted from {{fleet}}? [i-deleted-my-agent]

It’s okay, we’ve got your back! The data is still in {{es}}. To add {{agent}} to {{fleet}} again, [Stop {{agent}}](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/start-stop-elastic-agent.md#stop-elastic-agent-service), re-enroll it on the host, then run {{agent}}.


## How do I restart {{agent}} after rebooting my host? [i-rebooted-my-host]

{{agent}} should restart automatically when you reboot your host. If it doesn’t, you can start it manually by running:

```shell
elastic-agent run
```

If the process is already running, you can restart it by running:

```shell
elastic-agent restart
```


## Does {{agent}} or {{kib}} download integration packages? [does-agent-download-packages]

{{agent}} does not download integration packages. When you add an integration in {{fleet}}, {{kib}} connects to the {{package-registry}} at `epr.elastic.co`, downloads the integration package, and stores its assets in {{es}}. This means that you no longer have to run a manual setup command to load integrations as you did previously with {{beats}} modules.

By default, {{kib}} requires an internet connection to download integration packages from the {{package-registry}}. If network restrictions prevent {{kib}} from reaching the public {{package-registry}}, you can use a proxy server or host your own {{package-registry}}. To learn more, refer to [Air-gapped environments](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/air-gapped.md).


## Does {{agent}} download anything from the Internet? [does-agent-download-anything-from-internet]

* In version 7.10 and later, a fully capable artifact can be installed with no connection to the Elastic download site. However, if it is in use, the {{elastic-defend}} process is instructed to attempt to download newer released versions of the integration-specific artifacts it uses. Some of those are, for example, the malware model, trusted applications artifact, exceptions list artifact, and others. {{elastic-endpoint}} will continue to protect the host even if it’s unable to download updates. However, it won’t receive updates to protections until {{agent}} is upgraded to a new version. For more information, refer to the [{{elastic-sec}} documentation](/solutions/security.md).
* {{agent}} requires internet access to download artifacts for binary upgrades. In air-gapped environments, you can host your own artifact registry. For more information, refer to [Air-gapped environments](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/air-gapped.md).


## Do I need to set up the {{beats}} managed by {{agent}}? [do-i-need-to-setup-elastic-agent]

You might have noticed that {{agent}} runs {{beats}} under the hood. But note that the {{beats}} managed by {{agent}} are set up and run differently from standalone {{beats}}.

For example, standalone {{beats}} use modules and require you to run a setup command on the host to load assets, such as ingest pipelines and dashboards. In contrast, {{beats}} managed by {{agent}} use integration packages that {{kib}} downloads from the {{package-registry}} at `epr.elastic.co`. This means that {{agent}} does not need extra privileges to set up assets because {{fleet}} manages the assets.


## What is the {{elastic-defend}} integration in {{fleet}}? [what-is-the-endpoint-package]

The {{elastic-defend}} integration provides protection on your {{agent}} controlled host. The integration monitors your host for security-related events, allowing for investigation of security data through the {{security-app}} in {{kib}}. The {{elastic-defend}} integration is managed by {{agent}} in the same way as other integrations. Try it out! For more information, refer to the [{{elastic-sec}} documentation](/solutions/security.md).


## How are communications secured between {{elastic-sec}} and {{agent}}? [how-are-security-to-agent-communications-secured]

{{elastic-sec}} connects to the agent over loopback TLS on port 6788. {{elastic-sec}} validates that the agent has root (Linux and macOS) or SYSTEM (Windows) permissions.


## How are secrets secured when entered into integration policies or agent policies in {{kib}}? [how-are-secrets-secured]

Credentials that you provide for an agent or integration policy are stored in {{es}}. They can be read by any user who has read permissions to the `.fleet-*` and `.kibana*` indices in {{es}}. By default these are the superuser, `fleet-server` service account tokens, and the `kibana_system` user. These secrets are also included in agent policies and shared with agents via {{fleet}} through TLS. When you use the {{agent}} installer and enroll agents in {{fleet}}, the policies are stored on the host file system and, by default, can only be read by root.


## Which {{es}} and {{kib}} ports need to be accessible? [which-es-kibana-ports-are-needed]

The policy generated by {{fleet}} already contains the correct {{es}} address and port for your setup. If you run everything locally, the address is `127.0.0.1:9200`. If you use [{{ech}}](https://www.elastic.co/cloud/elasticsearch-service?page=docs&placement=docs-body), you can copy the {{es}} endpoint URL from the overview page of your deployment. If you’re not running in {{ecloud}}, make sure the {{kib}} and {{es}} HTTPS ports are both accessible; by default these are `5601` and `9200` respectively.


## If I delete an integration dashboard asset from {{kib}}, how do I get it back? [how-do-i-reinstall-a-missing-dashboard-asset]

To reinstall the assets for a specific integration, you can use the {{fleet}} UI. For more information, see [Reinstall integration assets](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/install-uninstall-integration-assets.md#reinstall-integration-assets).

Alternatively, you can use the {{fleet}} API using the package name and version. This needs to be run against the {{kib}} API and not the {{es}} API to be successful. To reinstall package assets, execute the following call with the `force` parameter in the body:

```bash
POST api/fleet/epm/packages/[package name]/[package version]
{ "force": true }
```

So, for example, to reinstall the system v1.0.0 package, POST:

```bash
POST api/fleet/epm/packages/system/1.0.0
{ "force": true }
```

The package version is shown in the Integrations view in {{kib}}.
