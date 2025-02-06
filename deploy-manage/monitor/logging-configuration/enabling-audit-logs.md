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

::::{important}
Audit logs are **disabled** by default and must be explicitly enabled; they are available only on certain [subscription levels](https://www.elastic.co/subscriptions).
::::

You can log security-related events such as authentication failures and refused connections to monitor your cluster for suspicious activity (including data access authorization and user security configuration changes).

This section describes how to enable and configure audit logging in both {{es}} and {{kib}} for all supported deployment types, including self-managed clusters, Elastic Cloud Hosted, Elastic Cloud Enterprise (ECE), and Elastic Cloud on Kubernetes (ECK).

Audit logging is enabled separately for both {{es}} and {{kib}}, and enabling both is optional, depending on your use case and requirements. 

The process of enabling and configuring audit logging is consistent across all supported deployment types, whether self-managed, Elastic Cloud, Elastic Cloud Enterprise (ECE), or Elastic Cloud on Kubernetes (ECK). The same settings apply regardless of the deployment type, ensuring a unified approach to audit logging configuration.

The only difference lies in how the configuration is applied:
  * In self-managed clusters, settings are added directly to the `elasticsearch.yml` and `kibana.yml` configuration files.
  * In orchestrated deployments (Elastic Cloud Hosted, ECE or ECK), the configuration is applied using the appropriate mechanisms provided by the orchestrator. Refer to [](/deploy-manage/deploy.md) for more information about the different orchestrators and deployment configuration mechanisms.

In short, to enable {{es}} or {{kib}} audit logs, set `xpack.security.audit.enabled` to `true` in the configuration of **all {{es}} or {{kib}} nodes**. In self-managed clusters you will have to perform a [rolling restart of the cluster](/deploy-manage/maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md) to apply the changes, while in orchestrated environments the orchestrator will apply the change and restart the nodes automatically.

The following tabs show the detailed process for all deployment types:

## Enabling procedure [enable-audit-logging-procedure]

::::::{tab-set}

:::::{tab-item} Self-managed

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

:::::

:::::{tab-item} Elastic Cloud Hosted

::::{important}
In orchestrated deployments, audit logs must be shipped to a monitoring deployment; otherwise, they remain at container level and won't be accessible to users. For details on configuring log forwarding in orchestrated environments, refer to [logging configuration](../logging-configuration.md).
::::

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

::::{important}
In orchestrated deployments, audit logs must be shipped to a monitoring deployment; otherwise, they remain at container level and won't be accessible to users. For details on configuring log forwarding in orchestrated environments, refer to [logging configuration](../logging-configuration.md).
::::

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

::::{important}
In orchestrated deployments, audit logs must be shipped to a monitoring deployment; otherwise, they remain at container level and won't be accessible to users. For details on configuring log forwarding in orchestrated environments, refer to [logging configuration](../logging-configuration.md).
::::

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

{{es}} audit logging and {{kib}} audit logging offer several configuration mechanisms to control what events are logged and what information is included in the audit log. For more information, refer to:

* [{{es}} audited event settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/auditing-settings.html#event-audit-settings)
* [{{es}} node information settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/auditing-settings.html#node-audit-settings)
* [{{es}} ignore policies settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/auditing-settings.html#audit-event-ignore-policies)
* [{{kib}} audit logging settings](https://www.elastic.co/guide/en/kibana/current/security-settings-kb.html#audit-logging-settings)

::::{important} 
Be advised that **sensitive data may be audited in plain text** when including the request body in audit events, even though all the security APIs, such as those that change the user’s password, have the credentials filtered out when audited.
::::

The configuration can be applied using the same [procedure](#enable-audit-logging-procedure) used to enable audit logs, described for all deployment types.

Configuration suggestions:
* Use [`xpack.security.audit.logfile.events.include`](https://www.elastic.co/guide/en/elasticsearch/reference/current/auditing-settings.html#xpack-sa-lf-events-include) or the corresponding `exclude` setting to specify the kind of events you want to include or exclude in the {{es}} auditing output.
* Refer to [logfile ignore policies](./logfile-audit-events-ignore-policies.md) for an example of how to tune the verbosity of the {{es}} audit trail.
* Refer to [auditing search queries](./auditing-search-queries.md) for details on logging request bodies in the {{es}} audit logs.
* Use {{kib}} [ignore filters](https://www.elastic.co/guide/en/kibana/current/security-settings-kb.html#audit-logging-ignore-filters) to determine which events to exclude from the {{kib}} audit log.

Extra considerations:

* Elastic Cloud Hosted deployments provide its own subset of supported settings for auditing configuration:
  * [Elasticsearch audit settings on Elastic Cloud](https://www.elastic.co/guide/en/cloud/current/ec-add-user-settings.html#ec_audit_settings)
  * [Kibana audit settings on Elastic Cloud](https://www.elastic.co/guide/en/cloud/current/ec-manage-kibana-settings.html#ec_logging_and_audit_settings)

* Changing the configuration of `log4j2.properties` is not supported in orchestrated deployments, and it's not recommended for `self-managed` deployments.

* For a complete list of event kinds and attributes, refer to:
  * [{{es}} audit events](/deploy-manage/monitor/logging-configuration/elasticsearch-audit-events.md).
  * [{{kib}} audit events](https://www.elastic.co/guide/en/kibana/current/xpack-security-audit-logging.html#xpack-security-ecs-audit-logging)


## Elasticsearch audit output 



You can also configure how the logfile is written in the `log4j2.properties` file located in `ES_PATH_CONF` (or check out the relevant portion of the [log4j2.properties in the sources](https://github.com/elastic/elasticsearch/blob/master/x-pack/plugin/core/src/main/config/log4j2.properties)). By default, audit information is appended to the `<clustername>_audit.json` file located in the standard Elasticsearch `logs` directory (typically located at `$ES_HOME/logs`). The file is also rotated and archived daily or upon reaching the 1GB file size limit.







