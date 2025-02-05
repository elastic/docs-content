---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/enable-audit-logging.html
  - https://www.elastic.co/guide/en/kibana/current/xpack-security-audit-logging.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-enable-auditing.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s_audit_logging.html
  - https://www.elastic.co/guide/en/cloud/current/ec-enable-logging-and-monitoring.html#ec-enable-audit-logs
applies:
  hosted: all
  ece: all
  eck: all
  stack: all
  serverless: unavailable
---

% What needs to be done: Refine

% GitHub issue: https://github.com/elastic/docs-projects/issues/350

% Scope notes: Merge the content and even consider putting everything under a global section that also covers Elasticsearch self-managed (done)

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/cloud/cloud-enterprise/ece-enable-auditing.md
% - [ ] ./raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s_audit_logging.md
% - [ ] ./raw-migrated-files/cloud/cloud/ec-enable-logging-and-monitoring.md

% https://www.elastic.co/guide/en/cloud/current/ec-add-user-settings.html#ec_audit_settings
% https://www.elastic.co/guide/en/cloud/current/ec-manage-kibana-settings.html#ec_logging_and_audit_settings


# Enable audit logging [enable-audit-logging]

You can log security-related events such as authentication failures and refused connections to monitor your cluster for suspicious activity (including data access authorization and user security configuration changes).

This section describes how to enable and configure audit logging in both {{es}} and {{kib}} for all deployment types.

In all deployment types, the auditing settings to enable and configure audit logs are the same.

As with self-managed systems, audit logging must be enabled separately for both {{es}} and {{kib}} to capture events from both components.

::::{important}
In orchestrated deployments, audit logs must be shipped to a monitoring deployment; otherwise, they remain at container level and won't be accessible to users. For details on configuring log forwarding in orchestrated environments, refer to [logging configuration](../logging-configuration.md).
::::

::::{important}
Audit logs are **disabled** by default. You must explicitly enable audit logging.
::::

<a id="enable-audit-logging-elasticsearch"></a>
<a id="enable-audit-logging-kibana"></a>

## Enable audit logging in self-managed clusters [enable-audit-logging-self-managed] 
:::{applies}
:stack: all
:::

To enable audit logging in {{es}}:

1. Set `xpack.security.audit.enabled` to `true` in `elasticsearch.yml`.
2. Restart {{es}}.

When audit logging is enabled, audit events are persisted to a dedicated `<clustername>_audit.json` file on the host’s file system, on every cluster node. For more information, refer to [{{es}} logfile audit output](logfile-audit-output.md).

::::{note}
You can configure additional options to control what events are logged and what information is included in the audit log. For more information, refer to [{{es}} auditing settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/auditing-settings.html).
::::

To enable audit logging in {{kib}}:

1. Set `xpack.security.audit.enabled` to `true` in `kibana.yml`
2. Restart {{kib}}

::::{note}
You can optionally configure audit logs location, file/rolling file appenders and ignore filters using [{{kib}} audit logging settings](https://www.elastic.co/guide/en/kibana/current/security-settings-kb.html#audit-logging-settings).
::::

## Enable audit logging in orchestrated deployments [enable-audit-logging-orchestrated]
:::{applies}
:ece: all
:eck: all
:hosted: all
:::

To enable {{es}} or {{kib}} audit logs in an orchestrated system, set `xpack.security.audit.enabled` to `true` in the respective {{es}} or {{kib}} configuration through the orchestrator.

If you’re unfamiliar with configuring {{es}} and {{kib}} settings in your orchestrator, use the following tabs for detailed instructions on enabling audit logging for your deployment type.

::::::{tab-set}

:::::{tab-item} Elastic Cloud Hosted
To enable audit logging in an Elastic Cloud Hosted deployment:

1. Log in to the [Elasticsearch Service Console](https://cloud.elastic.co?page=docs&placement=docs-body).

2. Find your deployment on the home page in the Elasticsearch Service card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the deployments page to view all of your deployments.

  ::::{tip}
  On the deployments page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.
  ::::

3. From your deployment menu, go to the **Edit** page.

4. To enable auditing for Elasticsearch:
    * In the **Elasticsearch** section select **Manage user settings and extensions**. For deployments with existing user settings, you may have to expand the **Edit elasticsearch.yml** caret for each node instead.
    * Add the setting `xpack.security.audit.enabled: true`.

5. To enable auditing for Kibana:
    * In the **Kibana** section, select **Edit user settings**. For deployments with existing user settings, you may have to expand the **Edit kibana.yml** caret instead.
    * Add the setting `xpack.security.audit.enabled: true`.

6. Select **Save changes**.
    A plan change will run on your deployment. When it finishes, **audit logs will be delivered to your monitoring deployment**.

For details on available audit settings in Elastic Cloud Hosted deployments, refer to the following documents:
* [Elasticsearch audit settings on Elastic Cloud](https://www.elastic.co/guide/en/cloud/current/ec-add-user-settings.html#ec_audit_settings)
* [Kibana audit settings on Elastic Cloud](https://www.elastic.co/guide/en/cloud/current/ec-manage-kibana-settings.html#ec_logging_and_audit_settings)
:::::

:::::{tab-item} ECE
To enable audit logging in an ECE deployment:

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).

2. On the **Deployments** page, select your deployment.
  ::::{tip}
  On the deployments page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.
  ::::

3. From your deployment menu, go to the **Edit** page.

4. To enable auditing for {{es}}:
    * In the **Elasticsearch** section, select **Edit user settings and plugins**. For deployments with existing user settings, you may have to expand the **Edit elasticsearch.yml** caret for the first node instead.
    * Add the setting `xpack.security.audit.enabled: true`.

5. To enable auditing for {{kib}}:
    * In the **Kibana** section, select **Edit user settings**. For deployments with existing user settings, you may have to expand the **Edit kibana.yml** caret instead.
    * Add the setting `xpack.security.audit.enabled: true`.
    * If your Elastic Stack version is below 7.6.0, add the setting `logging.quiet: false`.

6. Select **Save**.
    A plan change will run on your deployment. When it finishes, **audit logs will be delivered to your monitoring deployment**.

For more information and other available auditing settings, refer to [{{es}} auditing settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/auditing-settings.html) and [{{kib}} auditing settings](https://www.elastic.co/guide/en/kibana/current/security-settings-kb.html#audit-logging-settings). Audit logs can be viewed within Elasticsearch and Kibana logs.
:::::

:::::{tab-item} ECK
To enable audit logging in an ECK-managed cluster, add `xpack.security.audit.enabled: true` to the `config` section of each {{es}} `nodeSet` and to the `config` section of the {{kib}} object's specification, for example:

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
spec:
  monitoring:
    metrics:
      elasticsearchRefs:
      - name: monitoring
        namespace: observability
    logs:
      elasticsearchRefs:
      - name: monitoring
        namespace: observability
  nodeSets:
  - name: default
    config:
      # https://www.elastic.co/guide/en/elasticsearch/reference/current/enable-audit-logging.html
      xpack.security.audit.enabled: true
---
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
spec:
  monitoring:
    metrics:
      elasticsearchRefs:
      - name: monitoring
        namespace: observability
    logs:
      elasticsearchRefs:
      - name: monitoring
        namespace: observability
  config:
    # https://www.elastic.co/guide/en/kibana/current/xpack-security-audit-logging.html
    xpack.security.audit.enabled: true
```

When enabled, audit logs are collected and shipped to the monitoring cluster referenced in the `monitoring.logs` section. If monitoring is not enabled audit logs will only be visible at container level.
:::::

::::::

## Advanced Configuration [audit-logging-configuration]

Kibana:
You can optionally configure audit logs location, file/rolling file appenders and ignore filters using [{{kib}} audit logging settings](https://www.elastic.co/guide/en/kibana/current/security-settings-kb.html#audit-logging-settings).


Elasticsearch:
You can configure additional options to control what events are logged and what information is included in the audit log. For more information, refer to [{{es}} auditing settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/auditing-settings.html).


Consider the following recommendations when working with {{es}} and {{kib}} audit logging:

(you configure in the same way you have enabled the feature...)

(reading security events... in the overview)

(move this)* When you are auditing security events, a single client request might generate multiple audit events across multiple cluster nodes. The common `request.id` attribute can be used to correlate the associated events.
* Use [`xpack.security.audit.logfile.events.include`](https://www.elastic.co/guide/en/elasticsearch/reference/current/auditing-settings.html#xpack-sa-lf-events-include) or the corresponding `exclude` setting to specify the kind of events you want to include or exclude in the {{es}} auditing output.
* Refer to [logfile ignore policies](./logfile-audit-events-ignore-policies.md) for an example of how to tune the verbosity of the {{es}} audit trail.
* Refer to [auditing search queries](./auditing-search-queries.md) for details on logging request bodies in the {{es}} audit logs.
* Use {{kib}} [ignore filters](https://www.elastic.co/guide/en/kibana/current/security-settings-kb.html#audit-logging-ignore-filters) to determine which events to exclude from the {{kib}} audit log.
* For a complete list of event kinds and attributes, refer to:
  * [{{es}} audit events](/deploy-manage/monitor/logging-configuration/elasticsearch-audit-events.md).
  * [{{kib}} audit events](https://www.elastic.co/guide/en/kibana/current/xpack-security-audit-logging.html#xpack-security-ecs-audit-logging)

Audit logs generated in orchestrated deployments are similar to those in self-managed clusters, and you can also control which security events to log using all the mechanisms described in [](#audit-logging-configuration). However, in orchestrated environments, changing log file names or `log4j2.properties` settings is not supported.

For details on available audit settings in Elastic Cloud Hosted deployments, refer to the following documents:
* [Elasticsearch audit settings on Elastic Cloud](https://www.elastic.co/guide/en/cloud/current/ec-add-user-settings.html#ec_audit_settings)
* [Kibana audit settings on Elastic Cloud](https://www.elastic.co/guide/en/cloud/current/ec-manage-kibana-settings.html#ec_logging_and_audit_settings)


