---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/detection-engine-overview.html
  - https://www.elastic.co/guide/en/serverless/current/security-detection-engine-overview.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Detections and alerts [security-detection-engine-overview]

Use the detection engine to create and manage rules and view the alerts these rules create. Rules periodically search indices (such as `logs-*` and `filebeat-*`) for suspicious source events and create alerts when a rule’s conditions are met. When an alert is created, its status is `Open`. To help track investigations, an alert’s [status](/solutions/security/detect-and-alert/manage-detection-alerts.md#detection-alert-status) can be set as `Open`, `Acknowledged`, or `Closed`.

:::{image} /solutions/images/security-alert-page.png
:alt: Alerts page
:screenshot:
:::

In addition to creating [your own rules](/solutions/security/detect-and-alert/create-detection-rule.md), enable [Elastic prebuilt rules](/solutions/security/detect-and-alert/install-manage-elastic-prebuilt-rules.md#load-prebuilt-rules) to immediately start detecting suspicious activity. For detailed information on all the prebuilt rules, see the [Prebuilt rule reference](detection-rules://index.md) section. Once the prebuilt rules are loaded and running, [Tune detection rules](/solutions/security/detect-and-alert/tune-detection-rules.md) and [Add and manage exceptions](/solutions/security/detect-and-alert/add-manage-exceptions.md) explain how to modify the rules to reduce false positives and get a better set of actionable alerts. You can also use exceptions and value lists when creating or modifying your own rules.

There are several special prebuilt rules you need to know about:

* [**Endpoint protection rules**](/solutions/security/manage-elastic-defend/endpoint-protection-rules.md): Automatically create alerts based on {{elastic-defend}}'s threat monitoring and prevention.
* [**External Alerts**](detection-rules://rules/promotions/external_alerts.md): Automatically creates an alert for all incoming third-party system alerts (for example, Suricata alerts).

If you want to receive notifications via external systems, such as Slack or email, when alerts are created, use the {{kib}} [Alerting and Actions](/explore-analyze/alerts-cases.md) framework.

::::{note}
To use {{kib}} Alerting for detection alert notifications in the {{stack}}, you need the [appropriate license](https://www.elastic.co/subscriptions).
::::


After rules have started running, you can monitor their executions to verify they are functioning correctly, as well as view, manage, and troubleshoot alerts (see [Manage detection alerts](/solutions/security/detect-and-alert/manage-detection-alerts.md) and [Monitor and troubleshoot rule executions](/troubleshoot/security/detection-rules.md)).

You can create and manage rules and alerts via the UI or the [Detections API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-security-detections-api).

::::{important}
To make sure you can access Detections and manage rules, see [Detections requirements](/solutions/security/detect-and-alert/detections-requirements.md).

::::



## Manage data in cold and frozen tiers [cold-tier-detections]

```yaml {applies_to}
stack:
```

Cold [data tiers](/manage-data/lifecycle/data-tiers.md) store time series data that's accessed infrequently and rarely updated, while frozen data tiers hold time series data that's accessed even less frequently and never updated. If you're automating searches across different data tiers using rules, consider the following best practices and limitations.

### Best practices [best-practices-data-tiers]

* **Retention in hot tier**: We recommend keeping data in the hot tier ({{ilm-cap}} hot phase) for at least 24 hours. {{ilm-cap}} policies that move ingested data from the hot phase to another phase (for example, cold or frozen) in less than 24 hours may cause performance issues and/or rule execution errors.
* **Replicas for mission-critical data**: Your data should have replicas if it must be highly available. Since frozen tiers don't have replicas by default, shard unavailability can cause partial rule run failures. Shard unavailability may be also encountered during or after {{stack}} upgrades. If this happens, you can [manually rerun](/solutions/security/detect-and-alert/manage-detection-rules.md#manually-run-rules) rules over the affected time period once the shards are available.

### Limitations [limitations-data-tiers]

Data tiers are a powerful and useful tool. When using them, keep the following in mind:

* To avoid rule failures, do not modify {{ilm}} policies for {{elastic-sec}}-controlled indices, such as alert and list indices.
* Source data must have an {{ilm}} policy that keeps it in the hot or warm tiers for at least 24 hours before moving to cold or frozen tiers.

## Limited support for indicator match rules [support-indicator-rules]

Indicator match rules provide a powerful capability to search your security data; however, their queries can consume significant deployment resources. When creating an [indicator match rule](/solutions/security/detect-and-alert/rule-types/indicator-match.md), we recommend limiting the time range of the indicator index query to the minimum period necessary for the desired rule coverage. For example, the default indicator index query `@timestamp > "now-30d/d"` searches specified indicator indices for indicators ingested during the past 30 days and rounds the query start time down to the nearest day (resolves to UTC `00:00:00`). Without this limitation, the rule will include all of the indicators in your indicator indices, which may extend the time it takes for the indicator index query to complete.

In addition, the following support restrictions are in place:

* Indicator match rules don’t support cold or frozen data. Cold or frozen data in indices queried by indicator match rules must be older than the time range queried by the rule. If your data’s timestamps are unreliable, you can exclude cold and frozen tier data using a [Query DSL filter](/solutions/security/detect-and-alert/exclude-cold-frozen-data-from-individual-rules.md).
* Indicator match rules with an additional look-back time value greater than 24 hours are not supported.


## Detections configuration and index privilege prerequisites [detections-permissions]

[Detections requirements](/solutions/security/detect-and-alert/detections-requirements.md) provides detailed information on all the permissions required to initiate and use the Detections feature.

## Resolve UI error messages [_resolve_ui_error_messages]

Depending on your privileges and whether detection system indices have already been created for the {{kib}} space, you might get one of these error messages when you open the **Alerts** or **Rules** page:

* **`Let’s set up your detection engine`**

    If you get this message, a user with specific privileges must visit the **Alerts** or **Rules** page before you can view detection alerts and rules. Refer to [Enable and access detections](/solutions/security/detect-and-alert/detections-requirements.md#enable-detections-ui) for a list of all the requirements.

    ::::{note}
    For **self-managed** {{stack}} deployments only, this message may be displayed when the [`xpack.encryptedSavedObjects.encryptionKey`](/solutions/security/detect-and-alert.md#detections-permissions) setting has not been added to the [`kibana.yml`](/deploy-manage/stack-settings.md) file. For more information, refer to [Configure self-managed {{stack}} deployments](/solutions/security/detect-and-alert/detections-requirements.md#detections-on-prem-requirements).
    ::::

* **`Detection engine permissions required`**

    If you get this message, you do not have the [required privileges](/solutions/security/detect-and-alert.md#detections-permissions) to view the **Detections** feature, and you should contact your {{kib}} administrator.

    ::::{note}
    For **self-managed** {{stack}} deployments only, this message may be displayed when the [`xpack.security.enabled`](/solutions/security/detect-and-alert.md#detections-permissions) setting is not enabled in the `elasticsearch.yml` file. For more information, refer to [Configure self-managed {{stack}} deployments](/solutions/security/detect-and-alert/detections-requirements.md#detections-on-prem-requirements).
    ::::



## Using logsdb index mode [detections-logsdb-index-mode]

To learn how your rules and alerts are affected by using the [logsdb index mode](/manage-data/data-store/data-streams/logs-data-stream.md), refer to [Using logsdb index mode with {{elastic-sec}}](/solutions/security/detect-and-alert/using-logsdb-index-mode-with-elastic-security.md).

## Manage rules as code [manage-rule-dac]

Utilize the [Detection-as-Code](https://dac-reference.readthedocs.io/en/latest/dac_concept_and_workflows.html) (DaC) principles to externally manage your detection rules.

The {{elastic-sec}} Labs team uses the [detection-rules](https://github.com/elastic/detection-rules) repo to develop, test, and release {{elastic-sec}}'s[ prebuilt rules](https://github.com/elastic/detection-rules/tree/main/rules). The repo provides DaC features and allows you to customize settings to simplify the setup for managing user rules with the DaC pipeline.

To get started, refer to the [DaC documentation](https://github.com/elastic/detection-rules/blob/main/README.md#detections-as-code-dac).
