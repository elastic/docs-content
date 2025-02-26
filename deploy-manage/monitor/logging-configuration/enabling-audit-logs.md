---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/enable-audit-logging.html
  - https://www.elastic.co/guide/en/kibana/current/xpack-security-audit-logging.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-enable-auditing.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s_audit_logging.html
  - https://www.elastic.co/guide/en/cloud/current/ec-enable-logging-and-monitoring.html#ec-enable-audit-logs
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
  serverless: unavailable
---

# Enable audit logging [enable-audit-logging]

::::{important}
Audit logs are only available on certain [subscription levels](https://www.elastic.co/subscriptions).
::::

You can log security-related events such as authentication failures and refused connections to monitor your cluster for suspicious activity (including data access authorization and user security configuration changes). Audit logging can be enabled independently for {{es}} and {{kib}}.

This section describes how to enable and configure audit logging in both {{es}} and {{kib}} for all supported deployment types, including self-managed clusters, {{ech}}, {{ece}} (ECE), and {{eck}} (ECK).

::::{important}
In orchestrated deployments, audit logs must be shipped to a monitoring deployment; otherwise, they remain at container level and won't be accessible to users. For details on configuring log forwarding in orchestrated environments, refer to [logging configuration](../logging-configuration.md).
::::

When audit logging is enabled, security events are persisted to a dedicated `<clustername>_audit.json` file on the host’s file system, on every cluster node. For more information, refer to [{{es}} logfile audit output](logfile-audit-output.md).

## Enable audit logging [enable-audit-logging-procedure]

To enable {{es}} or {{kib}} audit logs, configure `xpack.security.audit.enabled` to `true` in **all {{es}} or {{kib}} nodes**, then restart the nodes to apply the changes. For detailed instructions, select your deployment type:

::::{note}
Audit logs are disabled by default and must be explicitly enabled.
::::


::::::{tab-set}

:::::{tab-item} Self-managed

**To enable audit logging in {{es}}**:

1. In all nodes, set `xpack.security.audit.enabled` to `true` in `elasticsearch.yml`.
2. Restart the cluster by following the [rolling restart](/deploy-manage/maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md) procedure.

**To enable audit logging in {{kib}}**:

1. Set `xpack.security.audit.enabled` to `true` in `kibana.yml`.
2. Restart {{kib}}.

:::::

:::::{tab-item} Elastic Cloud Hosted


To enable audit logging in an {{ech}} deployment:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).

2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.

3. From your deployment menu, go to the **Edit** page.

4. To enable auditing for Elasticsearch:
    * In the **Elasticsearch** section, select **Manage user settings and extensions**. For deployments with existing user settings, you may have to expand the **Edit elasticsearch.yml** caret for each node instead.
    * Add the setting `xpack.security.audit.enabled: true`.

5. To enable auditing for Kibana:
    * In the **Kibana** section, select **Edit user settings**. For deployments with existing user settings, you may have to expand the **Edit kibana.yml** caret instead.
    * Add the setting `xpack.security.audit.enabled: true`.

6. Select **Save changes**.

A plan change will run on your deployment. When it finishes, audit logs will be delivered to your monitoring deployment.
:::::

:::::{tab-item} ECE


To enable audit logging in an ECE deployment:

1. [Log in to the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).

2. On the **Deployments** page, select your deployment.

3. From your deployment menu, go to the **Edit** page.

4. To enable auditing for {{es}}:
    * In the **Elasticsearch** section, select **Edit user settings and plugins**. For deployments with existing user settings, you may have to expand the **Edit elasticsearch.yml** caret for the first node instead.
    * Add the setting `xpack.security.audit.enabled: true`.

5. To enable auditing for {{kib}}:
    * In the **Kibana** section, select **Edit user settings**. For deployments with existing user settings, you may have to expand the **Edit kibana.yml** caret instead.
    * Add the setting `xpack.security.audit.enabled: true`.
    * If your Elastic Stack version is below 7.6.0, add the setting `logging.quiet: false`.

6. Select **Save**.

A plan change will run on your deployment. When it finishes, audit logs will be delivered to your monitoring deployment.
:::::

:::::{tab-item} ECK


To enable audit logging in an ECK-managed cluster, add `xpack.security.audit.enabled: true` to the `config` section of each {{es}} `nodeSet` and to the `config` section of the {{kib}} object's specification. 

The following example shows this configuration, along with  together with logs and metrics delivery towards a remote cluster:

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
    xpack.security.audit.enabled: true
```

When enabled, audit logs are collected and shipped to the monitoring cluster referenced in the `monitoring.logs` section. If monitoring is not enabled, audit logs will only be visible at container level.
:::::

::::::

## Next steps

You can configure additional options to control what events are logged and what information is included in the audit log. For more information, refer to [](./configuring-audit-logs.md).
