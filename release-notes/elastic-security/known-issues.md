---
navigation_title: Known issues
products:
  - id: security
  - id: kibana
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# {{elastic-sec}} known issues [elastic-security-known-issues]
Known issues are significant defects or limitations that may impact your implementation. These issues are actively being worked on and will be addressed in a future release. Review the {{elastic-sec}} known issues to help you make informed decisions, such as upgrading to a new version.

% Use the following template to add entries to this page.

% :::{dropdown} Title of known issue
% Applies to: Applicable versions for the known issue
% Description of the known issue.
% For more information, check [Issue #](Issue link).
% **Impact**<br> Impact of the known issue.
% **Workaround**<br> Steps for a workaround until the known issue is fixed.

% :::

:::{dropdown} Response actions fail and endpoints do not appear for agents on version-specific policies
**Applies to: {{stack}} 9.4.0, 9.4.1, 9.4.2, 9.4.3**

**Impact**<br>
Certain {{agent}} integration packages and inputs can trigger the creation of a version-specific {{agent}} policy in {{fleet}}. When a version-specific policy includes the {{elastic-defend}} integration, response actions against the affected endpoints fail. In addition, the corresponding endpoints are not visible on the **Assets** → **Endpoints** and **Assets** → **Endpoints** → **Policies** pages.

For more information, refer to [#276295](https://github.com/elastic/kibana/issues/276295).

**Workaround**<br>
There is currently no workaround available. A fix will be included in a future 9.4.x release.
:::

:::{dropdown} Osquery cannot target agents on version-specific policies
**Applies to: {{stack}} 9.4.0, 9.4.1, 9.4.2, 9.4.3**

**Impact**<br>
Certain {{agent}} integration packages and inputs can trigger the creation of a version-specific {{agent}} policy. When a version-specific policy includes the Osquery integration, the corresponding agents do not appear in the Osquery agent or policy selector, so they cannot be targeted. Live queries against an affected policy fail with a `No agents found for selection` error, and agent grouping and counts in the selector are inaccurate.

**Workaround**<br>
There is currently no workaround available. A fix will be included in a future 9.4.x release.
:::

:::{dropdown} Problem Child and DGA integrations fail to install
**Applies to: {{stack}} 9.3.6**

**Impact**<br>
The [ProblemChild](https://www.elastic.co/docs/reference/integrations/problemchild) (Living off the Land Detection) and [DGA](https://www.elastic.co/docs/reference/integrations/dga) integration packages fail to install. This is caused by an {{es}} validation that limits field names in trained models to 100 characters.

**Workaround**<br>
Upgrade to {{stack}} 9.3.7.

**Resolved**<br>

Resolved in {{stack}} 9.3.7.
:::

:::{dropdown} Upgrading to 9.3.x fails when a rule action contains oversized content
**Applies to: {{stack}} 9.3.0, 9.3.1, 9.3.2, 9.3.3, 9.3.4**

**Impact**<br>
Upgrading from 9.2.x to 9.3.x can fail if any rule (including detection rules) has a connector action whose parameter values are larger than 32,766 bytes. Common examples include email message bodies or HTML templates, large webhook payloads, or Slack messages built from verbose templates.

During the upgrade, {{kib}} migrates rule saved objects to a new internal mapping. Any oversized action parameter value causes the migration to abort with an error similar to:

```
Flattened field [alert.actions.params] contains one immense field whose keyed encoding is longer than the allowed max length of 32766 bytes
```

**Workaround**<br>

Upgrade to 9.3.5 or 9.4.2.

If the upgrade has failed with this error, identify rules that use connectors with large content (particularly email, webhook, and Slack connectors) and shorten the action parameter values, such as message bodies or HTML templates. Then retry the upgrade.


For more information, refer to [#268982](https://github.com/elastic/kibana/issues/268982).


**Resolved**

This issue is resolved in {{stack}} 9.3.5 and 9.4.2.
:::

:::{dropdown} Detection Rule run failures due to failed Entity Analytics enrichment
**Applies to: 9.4.0**

**Impact**<br>


After you upgrade to v9.4, any Detection Rules created by users without access to the `.entities.v2.latest.security_*` index (i.e., the entity store) do not enrich their alerts with entity analytics data. This means that alerts which contain user or host entities and were created from rules authored by users without access to the index show as failures. The alert document still generates, but without entity analytics data.

When a rule fires successfully and generates an alert, Asset Criticality and Entity Risk score values enrich the alert document. In 9.4, these values come from the entity store index `.entities.v2.latest.security_*` , which is a feature on by default in the default space.

Detection Rules use their author’s permissions to enrich alerts with entity data. When rules are created or modified, those permissions are stored as a "snapshot" in an API key. If the author lacks access to the `.entities.v2.latest.security_*` index, enrichment fails and the rule reports a failure status (though alerts still generate and actions are still scheduled).

**Workaround**<br>

Give appropriate `read` index-level permissions for the entity store index and alias in the appropriate space (`.entities.v2.latest.security_${spaceId}*` and `entities-latest-${spaceId}*`)  to a user, and have that user perform a no-op bulk update to all rules in the space. The rule will succeed on subsequent runs.

**Resolved**<br>

Resolved in {{stack}} 9.4.1
:::

:::{dropdown} SentinelOne response actions fail in Elastic Agent 9.3.4
**Applies to: {{agent}} 9.3.4**

**Impact**<br>
If you use the SentinelOne integration, response actions such as host isolation fail with a `500 Internal Server Error` (`search_phase_execution_exception`). This is caused by a bug in {{agent}} 9.3.4 where a performance optimization incorrectly serializes certain timestamp fields from Beats-based inputs and integrations to an empty `{}` JSON object instead of a valid timestamp value.

The affected field is `event.created`. When this field is empty, {{kib}} cannot execute the underlying search that response actions depend on. For example, SentinelOne alert documents are written with `event.created` set to `{}` instead of a timestamp:

```json
  "event": {
    "dataset": "sentinel_one.agent",
    "created": {}
  }
```

This does not affect the primary `@timestamp` field.

**Workaround**<br>
Upgrade to {{agent}} 9.3.5, which is not affected by this issue.

**Resolved**<br>

Resolved in {{agent}} 9.3.5. For more information, refer to [#266355](https://github.com/elastic/kibana/issues/266355).
:::

:::{dropdown} Details about gap fills aren't properly updated

Applies to: 9.3

**Impact**

After upgrading to 9.3 from a {{stack}} version earlier than 8.9, you might encounter the following issues with gap fill functionality:

* **Gap fills**: Manual runs are scheduled to fill gaps, but gap statuses aren't updated to `Filled` after the manual runs complete.

* **Rule deletion**: If a rule has gaps and you delete the rule, the rule is removed but the gaps are not marked as deleted. You may see incorrect numbers when viewing total rules with gaps.

**Root cause**

When upgrading from {{stack}} versions earlier than 8.9, the old event log index is reindexed with a new name:

* Old index: `.reindexed-v8-kibana-event-log-{version}-000001`
* Aliases: `.kibana-event-log-{version}`, `.kibana-event-log-{version}-000001`

Starting in {{stack}} 8.9.0, a new data stream (`.kibana-event-log-ds`) was introduced for event log storage.

The `elastic/kibana` service account has permissions to access the new data stream but does not have permissions to access the old reindexed indices. When {{kib}} queries `.kibana-event-log-*`, it matches both the new data stream and the old reindexed index, causing Point-in-Time (PIT) operations to fail.

**Workaround**

Migrate data from the old reindexed index to the new data stream, then delete the old index.

1. **Identify the old index**:

    ```console
    GET .kibana-event-log-*
    ```

    Look for indices with names like `.reindexed-v8-kibana-event-log-{version}-*`.

2. **Reindex data to the new data stream**:

    ```console
    POST _reindex
    {
      "source": {
        "index": ".reindexed-v8-kibana-event-log-7.17.29-000001" <1>
      },
      "dest": {
        "index": ".kibana-event-log-ds",
        "op_type": "create"
      }
    }
    ```

    1. Replace `7.17.29` with your version number.

3. **Delete the old index**:

    ```console
    DELETE .reindexed-v8-kibana-event-log-7.17.29-000001
    ```

4. **Verify**:

    ```console
    GET .kibana-event-log-*
    ```

    Only the data stream (`.kibana-event-log-ds`) and its backing indices (`.ds-.kibana-event-log-ds-*`) should remain.

:::{important}
* **Backup**: Consider backing up your data before performing these operations in production environments.
* **Event log retention**: Event log data has a default retention of 90 days. If you don't need historical data, you can skip the reindex step and simply delete the old index and its aliases.
:::

:::

:::{dropdown} Intermittent blue screen due to conflict with Windows ODX in {{elastic-defend}}
Applies to: 8.19.8, 8.19.9, 9.1.8, 9.1.9, 9.2.2, and 9.2.3

**Impact**<br>
An issue in {{elastic-defend}} on Windows can result in `KERNEL_AUTO_BOOST_LOCK_ACQUISITION_WITH_RAISED_IRQL` or `PAGE_FAULT_IN_NONPAGED_AREA` bug checks (blue screens) when [Offloaded Data Transfer (ODX)](https://learn.microsoft.com/en-us/windows-hardware/drivers/storage/offloaded-data-transfer) is used to copy files.

**Workaround**<br>

If you're unable to upgrade to a fixed version, you can disable the affected code by setting the `windows.advanced.kernel.filewrite` [advanced setting](/reference/security/defend-advanced-settings.md) to `false` in your {{elastic-defend}} integration policy.

**Resolved**<br>

Resolved in {{agent}} 8.19.10, 9.1.10 and 9.2.4

:::{tip}
As long as the major and minor versions match, you can run a newer patch version of {{agent}} than the {{stack}}. For example, you can use 9.1.10 {{agent}} with 9.1.8 {{stack}}.
:::

:::


:::{dropdown} Deploying integrations using AWS CloudFormation doesn't work
Applies to: 9.2.0 and 9.2.1

**Impact**<br>
New deployments of integrations that collect data from cloud service providers, such as Asset Discovery and Cloud Security Posture Management, do not work when deployed to AWS using agent-based deployment and the AWS CloudFormation deployment option. The problem results from a malformed CloudFormation parameter: `ElasticAgentVersion`. The default value for `ElasticAgentVersion` has a space instead of a `+`. This produces an invalid agent version value.

For more information, check [#14627](https://github.com/elastic/kibana/pull/242365).


**Workaround**<br>

To work around this issue, update the default CloudFormation template by replacing the space in the `ElasticAgentVersion` parameter with a `+`.

**Resolved**<br>

Resolved in {{stack}} 9.2.2.

:::

:::{dropdown} Entity store transform is unavailable

Applies to: 9.2.0

**Impact**

A new feature introduced to the entity store in 9.2.0 caused the transform to scan for nonexistent indices.

**Workaround**

Restart the entity store:
1. Find **Entity Store** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. On the **Entity Store** page, turn the toggle off.
3. Turn the toggle back on.

**Resolved**<br>

Resolved in {{stack}} 9.2.1

::::

:::{dropdown} CSPM and Asset Management integrations don't ingest data when deployed using agent-based technology if {{kib}} is hosted on AWS
Applies to: ECH 9.2.0 deployments hosted on AWS

**Impact**

If your ECH deployment is hosted on AWS, new Cloud Security Posture Management (CSPM) and Asset Inventory integrations will fail to produce findings when deployed using agent-based deployment. ECH deployments hosted on GCP or Azure are not affected. Integrations that use agentless deployment are not affected.

**Workaround**

Two workarounds are available:

1. Turn off the **Enable Cloud Connector** advanced setting.
    1. Go to the **Advanced Settings** menu using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
    2. In the **Security Solution** section, turn off the **Enable Cloud Connector** option.
    3. Your agent-based integration deployments will work as expected.
2. Use agentless deployment.
    1. Instead of using agent-based deployment, use agentless deployment. Agentless deployment works as expected.

**Resolved**<br>

Resolved in {{stack}} 9.2.1

::::


::::{dropdown} Filters may not apply correctly on the Alerts page
Applies to: 9.1.0, 9.1.1, 9.1.2, and 9.1.3

**Impact**

After upgrading to 9.1.0 and later, some users may experience inconsistent results when applying filters to the Alerts page.

**Workaround**

You can turn off the {{kib}} `courier:ignoreFilterIfFieldNotInIndex` [advanced setting](kibana://reference/advanced-settings.md#kibana-search-settings), which only applies to the current space. However, turning off this setting might prevent dashboards and visualizations with applied filters from displaying properly. If you have important dashboards that this will impact, you can temporarily move them to a new space by doing the following:

1. Create a [new space](/deploy-manage/manage-spaces.md#spaces-managing).
2. Turn on the {{kib}} `courier:ignoreFilterIfFieldNotInIndex` [advanced setting](kibana://reference/advanced-settings.md#kibana-search-settings) so that filters  apply to visualizations only if the index contains the filtering field.
3. Use the [import saved objects tool](/explore-analyze/find-and-organize/saved-objects.md#saved-objects-import-and-export) to move the dashboards or visualizations to the space you just created.

:::{note}
Ensure you give any users who will need access to the new space the appropriate permissions.
:::

**Resolved**<br>

Resolved in {{stack}} 9.1.4

::::

:::{dropdown} "Write role required to generate data" error when Data View Management is turned off for a space

Applies to: 9.0

**Impact**

When the **Data View Management** feature is turned off for a {{kib}} space, users with write access to that space can encounter the following error in some {{elastic-sec}} apps, even when they have all the required [detections privileges](/solutions/security/detect-and-alert/detections-privileges.md):

```txt
Write role required to generate data: Users with write permission need to access the Elastic Security App to initialize the app source data
```

The error typically appears once per session until {{kib}} is fully reloaded.

For more information, check [#4493](https://github.com/elastic/security-docs/issues/4493).

**Workaround**

Turn on the **Data View Management** feature for the affected space:

1. Go to **Stack Management** → **Kibana** → **Spaces**.
2. Edit the affected space.
3. In the **Features** section, under **Management**, select the **Data View Management** checkbox.
4. Save the space.

**Resolved**<br>

Resolved in {{stack}} 9.1.0.

:::

:::{dropdown} The {{agent}} Docker image is not available at `docker.elastic.co/beats/elastic-agent:9.0.0`

Applies to: 9.0.0

**Impact**

The {{agent}} image is not available from `docker.elastic.co/beats/elastic-agent:9.0.0`. The default manifests for integrations that run {{agent}} on Kubernetes—such as CSPM or CNVM—use this image location, resulting in an error.

**Workaround**

Instead of trying to pull the image from `docker.elastic.co/beats/elastic-agent:9.0.0`, edit the manifests to pull it from `docker.elastic.co/elastic-agent/elastic-agent:9.0.0`.

**Resolved**<br>

Resolved in {{stack}} 9.0.1
:::


:::{dropdown} Elastic Defend's Network driver may lead to bug checks

**Applies to: {{agent}} 8.17.8, 8.18.3, and 9.0.3**

On July 8, 2025, a known issue was discovered in Elastic Defend's network driver that may lead to kernel pool corruption, resulting in bug checks (BSODs) on Windows systems with a large number of long-lived network connections that remain inactive for 30+ minutes.

The system may bug check with any of a variety of codes such as `SYSTEM_SERVICE_EXCEPTION` or `PAGE_FAULT_IN_NONPAGED_AREA`.

For more information, check [elastic/endpoint#90](https://github.com/elastic/endpoint/issues/90).

**Workaround**

If you're on 9.0.3, upgrade to the fixed version: [9.0.3+build202507110136](https://www.elastic.co/downloads/past-releases/elastic-agent-9-0-3+build202507110136).

If you're on 8.18.3, upgrade to the fixed version: [8.18.3+build202507101319](https://www.elastic.co/downloads/past-releases/elastic-agent-8-18-3+build202507101319).

If you're on 8.17.8, downgrade to 8.17.7 or install 8.17.9 once it becomes available.

If you're unable to upgrade or downgrade, set `advanced.kernel.network: false` in your Defend advanced policy.

**Resolved**<br>

Resolved in {{stack}} 9.0.4
:::

:::{dropdown} Security AI Assistant Knowledge Base settings UI not displaying

Applies to: 9.0.3

On June 24, 2025, an error was discovered that prevents the AI Assistant Knowledge Base settings UI from displaying, including the **Setup Knowledge Base** button and alert configuration options. As a result, the Knowledge Base cannot be set up or configured through the Knowledge Base settings UI.

**Workaround**

While the UI for configuring the Knowledge Base is blocked, you can still enable it
[from an AI Assistant conversation](/solutions/security/ai/ai-assistant-knowledge-base.md#_option_1_enable_knowledge_base_from_an_ai_assistant_conversation).

After enabling the Knowledge Base, you can manage entries using the AI Assistant API:

* List Knowledge Base entries using the [find knowledge base entry API]({{kib-apis}}/operation/operation-findknowledgebaseentries):

  ```console
  GET /api/security_ai_assistant/knowledge_base/entries/_find?page=1&per_page=100
  ```

* Create a Knowledge Base index entry using the [create knowledge base entry API]({{kib-apis}}/operation/operation-createknowledgebaseentry):

  ```console
  POST /api/security_ai_assistant/knowledge_base/entries
  {
    "type": "index",
    "name": "test",
    "index": "test-index",
    "field": "mock",
    "outputFields": ["example"],
    "description": "test description",
    "queryDescription": "test query description"
  }
  ```

* Create a Knowledge Base document entry using the [create knowledge base entry API]({{kib-apis}}/operation/operation-createknowledgebaseentry):

  ```console
  POST /api/security_ai_assistant/knowledge_base/entries
  {
    "type": "document",
    "kbResource": "user",
    "source": "user",
    "name": "doc"
  }
  ```

**Resolved**<br>

Resolved in {{stack}} 9.0.4
:::

:::{dropdown} The entity risk score feature may stop persisting risk score documents

Applies to: {{stack}} 9.0.0, 9.0.1, 9.0.2

On May 30, 2025, it was discovered that the entity risk score feature may stop persisting risk score documents if risk scoring was turned on before you upgraded to {{stack}} 8.18.0+ or 9.0.0+. This is due to a bug that prevents the `entity_analytics_create_eventIngest_from_timestamp-pipeline-<space_name>` ingest pipeline (which is set as a default pipeline for the risk scoring index in {{stack}} 8.18.0) from being created when {{kib}} starts up.

While document persistence may initially succeed, it will eventually fail after 0 to 30 days. This is how long it takes for the risk score data stream to roll over and apply its underlying index settings to the new default pipeline.

**NOTE:** This bug does not affect {{es}} clusters created in {{stack}} 8.18.0 or 9.0.0 and higher. It also won't affect you if you only turned on entity risk scoring in {{stack}} 8.18.0 or 9.0.0 and higher.

**Workaround**

To resolve this issue, apply the following workaround before or after upgrading to {{stack}} 9.0.0 or higher.

First, manually create the ingest pipeline in each space that has entity risk scoring turned on. You can do this using a PUT request, which is described in the example below. When reviewing the example, note that `default` in the example ingest pipeline name below is the {{kib}} space ID.

```
PUT /_ingest/pipeline/entity_analytics_create_eventIngest_from_timestamp-pipeline-default
{
  "_meta": {
    "managed_by": "entity_analytics",
    "managed": true
  },
  "description": "Pipeline for adding timestamp value to event.ingested",
  "processors": [
    {
      "set": {
        "field": "event.ingested",
        "value": "{{_ingest.timestamp}}"
      }
    }
  ]
}
```

After you complete this step, risk scores should automatically begin to successfully persist during the entity risk engine's next run. Details for the next run time are described on the **Entity risk score** page, where you can also manually run the risk score by clicking **Run Engine**.

**Resolved**<br>

Resolved in {{stack}} 9.0.3

:::

:::{dropdown} Installing an {{elastic-defend}} integration or a new agent policy upgrades installed prebuilt rules, reverting user customizations and overwriting user-added actions and exceptions

Applies to: {{stack}} 9.0.0

On April 10, 2025, it was discovered that when you install a new {{elastic-defend}} integration or agent policy, the installed prebuilt detection rules upgrade to their latest versions (if any new versions are available). The upgraded rules lose any user-added rule actions, exceptions, and customizations.

**Workaround**

To resolve this issue, before you add an {{elastic-defend}} integration to a policy in {{fleet}}, apply any pending prebuilt rule updates. This will prevent rule actions, exceptions, and customizations from being overwritten.

**Resolved**<br>

Resolved in {{stack}} 9.0.1

:::

:::{dropdown} The technical preview badge incorrectly displays on the alert suppression fields for event correlation rules

Applies to: {{stack}} 9.0.0 and 9.0.1

On April 8, 2025, it was discovered that alert suppression for event correlation rules is incorrectly shown as being in technical preview when you create a new rule. For more information, check [#1021](https://github.com/elastic/docs-content/issues/1021).

**Resolved**<br>

Resolved in {{stack}} 9.0.2

:::


:::{dropdown} Interaction between Elastic Defend and Trellix Access Protection causes IRQL_NOT_LESS_EQUAL bugcheck

Applies to: {{elastic-defend}} 9.0.0

An `IRQL_NOT_LESS_EQUAL` [bugcheck](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/bug-checks--blue-screens-) in the {{elastic-defend}} driver happens due to an interaction with Trellix Access Protection (`mfehidk.sys`). This issue can occur when `elastic-endpoint-driver.sys` calls [`FwpmTransactionBegin0`](https://learn.microsoft.com/en-us/windows/win32/api/fwpmu/nf-fwpmu-fwpmtransactionbegin0) to initialize its network driver. `FwpmTransactionBegin0` performs a synchronous RPC call to the user-mode Base Filtering Engine service. Trellix's driver intercepts this service's operations, causing `FwpmTransactionBegin0` to hang or slow significantly. This delay prevents {{elastic-defend}} driver from properly initializing in a timely manner. Subsequent system activity can invoke {{elastic-defend}}'s driver before it has fully initialized, leading to a `IRQL_NOT_LESS_EQUAL` bugcheck. This issue affects {{elastic-defend}} versions 8.16.0-8.16.6, 8.17.0-8.17.5, 8.18.0, and 9.0.0.

**Workaround**<br>

If you can't upgrade, either disable Trellix Access Protection or add a [Trellix Access Protection exclusion](https://docs.trellix.com/bundle/endpoint-security-10.6.0-threat-prevention-client-interface-reference-guide-windows/page/GUID-6AC245A1-5E5D-4BAF-93B0-FE7FD33571E6.html) for the Base Filtering Engine service (`C:\Windows\System32\svchost.exe`).

**Resolved**<br>

Resolved in {{elastic-defend}} 9.0.1

:::


:::{dropdown} Unbounded kernel non-paged memory growth issue in Elastic Defend's kernel driver causes slow down on Windows systems

Applies to: {{elastic-defend}} 9.0.0

An unbounded kernel non-paged memory growth issue in {{elastic-defend}}'s kernel driver occurs during extremely high event load situations on Windows. Systems affected by this issue will slow down or become unresponsive until the triggering event load (for example, network activity) subsides. We are only aware of this issue occurring on busy Windows Server systems running {{elastic-defend}} versions 8.16.0-8.16.6, 8.17.0-8.17.5, 8.18.0, and 9.0.0

**Workaround**<br>

If you can't upgrade, turn off the relevant event source at the kernel level using your {{elastic-defend}} [advanced policy settings (optional)](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#adv-policy-settings):

* Network Events - Set the `windows.advanced.kernel.network` advanced setting to `false`.
* Registry Events - Set the `windows.advanced.kernel.registry` advanced setting to `false`.

Clearing the corresponding checkbox under [event collection](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#event-collection) is insufficient, as {{elastic-defend}} may still process these event sources internally to support other features.

**Resolved**<br>

Resolved in {{elastic-defend}} 9.0.1

:::
