---
navigation_title: Osquery manager integration
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/manage-osquery-integration.html
description: Configure and customize the Osquery Manager integration, including advanced configuration options, custom Osquery versions, and debugging.
applies_to:
  stack: 
  serverless:
    security:
products:
  - id: kibana
---

# Manage the integration [manage-osquery-integration]


## System requirements [_system_requirements]

* [{{fleet}}](/reference/fleet/index.md) is enabled on your cluster, and one or more [{{agents}}](/reference/fleet/install-elastic-agents.md) is enrolled.
* The [Osquery Manager](https://docs.elastic.co/en/integrations/osquery_manager) integration has been added and configured for an agent policy through {{fleet}}. This integration supports x64 architecture on Windows, macOS, and Linux platforms, and ARM64 architecture on Linux.

::::{note}
* The original [Filebeat Osquery module](beats://reference/filebeat/filebeat-module-osquery.md) and the [Osquery](https://docs.elastic.co/en/integrations/osquery) integration collect logs from self-managed Osquery deployments. The **Osquery Manager** integration manages Osquery deployments and supports running and scheduling queries from {{kib}}.
* **Osquery Manager** cannot be integrated with an {{agent}} in standalone mode.

::::



## Customize Osquery sub-feature privileges [_customize_osquery_sub_feature_privileges]

Depending on your [subscription level](https://www.elastic.co/pricing) or [{{serverless-short}} project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md), you can customize the sub-feature privileges for **Osquery Manager**:

* Run live queries
* Run saved queries
* Save queries
* Schedule packs

For example, you can create roles for users who can only run live or saved queries, but who cannot save or schedule queries. This is useful for teams who need granular access control.

## Customize Osquery configuration [osquery-custom-config]

By default, all Osquery Manager integrations share the same Osquery configuration. However, you can customize how Osquery is configured by editing the Osquery Manager integration for each agent policy you want to adjust. The custom configuration is then applied to all agents in the policy. This powerful feature allows you to configure [File Integrity Monitoring](https://osquery.readthedocs.io/en/stable/deployment/file-integrity-monitoring), [Process auditing](https://osquery.readthedocs.io/en/stable/deployment/process-auditing), and [others](https://osquery.readthedocs.io/en/stable/deployment/configuration/#configuration-specification).

::::{important}
* Take caution when editing this configuration. The changes you make are distributed to all agents in the policy.
* Take caution when editing `packs` using the Advanced **Osquery config** field. Any changes you make to `packs` from this field are not reflected in the UI on the Osquery **Packs** page in {{kib}}, however, these changes are deployed to agents in the policy. While this allows you to use advanced Osquery functionality like pack discovery queries, you do lose the ability to manage packs defined this way from the Osquery **Packs** page.

::::


1. Go to **Fleet** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then open the **Agent policies** tab.
2. Click the name of the agent policy where you want to adjust the Osquery configuration. The configuration changes you make only apply to the policy you select.
3. Click the name of the **Osquery Manager** integration, or add the integration first if the agent policy does not yet have it.
4. From the **Edit Osquery Manager integration** page, expand the **Advanced** section.
5. Edit the **Osquery config** JSON field to apply your preferred Osquery configuration. Note the following:

    * The field may already have content if you’ve scheduled packs for this agent policy. To keep these packs scheduled, do not remove the `packs` section. The `shard` field value is the percentage of agents in the policy using the pack.
    * Refer to the [Osquery documentation](https://osquery.readthedocs.io/en/stable/) for configuration options.
    * Some fields are protected and cannot be set. A warning is displayed with details about which fields should be removed.
    * (Optional) To load a full configuration file, drag and drop an Osquery `.conf` file into the area at the bottom of the page.

6. Click **Save integration** to apply the custom configuration to all agents in the policy.

    As an example, the following configuration disables two tables.

```json
{
   "options": {
      "disable_tables":"file,process_envs"
   }
}
```



### Enabling the `curl` table [enable-curl-table]

By default, the [curl table](https://osquery.io/schema/#curl) is disabled. If preferred, you can enable it using the Advanced **Osquery config**.

**Why is the `curl` table disabled?**

When you query the [curl table](https://osquery.io/schema/#curl), this results in an HTTP request. The query results include the response to the request. As a simple example, if you run the query `SELECT * FROM curl WHERE url='https://www.elastic.co/';`, the `result` field contains the webpage content.

This table can be misused in some environments, for example, when used to issue HTTP requests to an AWS metadata service or to services on your internal network.

Out of an abundance of caution, we have opted to disable access to this table by default. However, if you need access to the table for your own monitoring purposes, you can enable it as needed.

**How to enable the `curl` table:**

For each agent policy where you want to allow `curl` table queries, edit the Osquery Manager integration to add the following Advanced **Osquery config**:

```json
{
   "options": {
      "enable_tables":"curl"
   }
}
```


## Upgrade Osquery versions [_upgrade_osquery_versions] 

The [Osquery version](https://github.com/osquery/osquery/releases) available on an {{agent}} is associated to the version of Osquery Beat on the Agent. To get the latest version of Osquery Beat, [upgrade your {{agent}}](/reference/fleet/upgrade-elastic-agent.md).


## Use a custom Osquery version [osquery-custom-version]
```{applies_to}
stack: ga 9.4 
serverless:
   security:
```

You can provide a custom Osquery binary to override the version bundled with {{agent}}. This allows you to run newer or custom versions of Osquery.

::::{warning}
This feature is **use at your own risk**. Elastic does not provide support or maintenance for custom Osquery binaries. Custom versions may introduce compatibility issues, including:

* Differences in the Osquery schema that affect queries and packs
* Breaking changes in flags or behavior
* Incompatibility with Elastic-managed configurations

Elastic's Osquery extensions might not work properly with custom binaries. You are responsible for validating stability and compatibility within your environment.
::::

To configure a custom Osquery version, add an `elastic_options.install` block to the Advanced **Osquery config** with platform-specific artifact URLs and SHA-256 checksums. The following example configures a custom Osquery binary for Linux:

```json
{
   "elastic_options": {
      "install": {
         "linux": {
            "amd64": {
               "artifact_url": "https://example.org/osquery-5.22.1.linux_x86_64.tar.gz",
               "sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
            },
            "arm64": {
               "artifact_url": "https://example.org/osquery-5.22.1.linux_aarch64.tar.gz",
               "sha256": "fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210"
            }
         }
      }
   }
}
```

The custom Osquery binary is installed in the bundled Osquery directory.

The following table lists the supported package formats for each platform:

| Platform | Architectures | Supported formats |
|----------|---------------|-------------------|
| Linux    | amd64, arm64  | `.tar.gz`         |
| macOS    | amd64, arm64  | `.pkg`            |
| Windows  | amd64, arm64  | `.msi`, `.zip`    |

Configuration options:

* `artifact_url`: (Required) The URL to the custom Osquery binary package. HTTPS is required by default.
* `sha256`: (Required) The SHA-256 checksum (64-character hex string) used to verify the downloaded artifact. Both `artifact_url` and `sha256` must be provided together.
* `allow_insecure_url`: (Optional) Defaults to `false`. Set to `true` to allow HTTP URLs (not recommended).
* `ssl.verification_mode`: (Optional) TLS verification mode for HTTPS downloads.

If a platform or architecture is not configured, the bundled Osquery version is used. If custom artifact installation or validation fails, the agent fails to start rather than silently falling back to the bundled version.

For complete configuration examples for macOS and Windows, refer to the [osquerybeat.reference.yml](https://github.com/elastic/beats/blob/main/x-pack/osquerybeat/osquerybeat.reference.yml) file.

## Debug issues [_debug_issues]

If you encounter issues with **Osquery Manager**, find the relevant logs for {{agent}} and Osquerybeat in the agent directory. Refer to the [Fleet Installation layout](/reference/fleet/installation-layout.md) to find the log file location for your OS.

```ts
../data/elastic-agent-*/logs/elastic-agent-json.log-*
../data/elastic-agent-*/logs/default/osquerybeat-json.log
```

To get more details in the logs, change the agent logging level to debug:

1. Go to **{{fleet}}** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select the agent that you want to debug.
3. On the **Logs** tab, change the **Agent logging level** to **debug**, and then click **Apply changes**.

    `agent.logging.level` is updated in `fleet.yml`, and the logging level is changed to `debug`.

If you configured a [custom Osquery version](#osquery-custom-version) and the agent fails to start, check the logs for artifact download or checksum validation errors.
