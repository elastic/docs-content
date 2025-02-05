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
---

% What needs to be done: Refine

% GitHub issue: https://github.com/elastic/docs-projects/issues/350

% Scope notes: Merge the content and even consider putting everything under a global section that also covers Elasticsearch self-managed (done)

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/cloud/cloud-enterprise/ece-enable-auditing.md
% - [ ] ./raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s_audit_logging.md
% - [ ] ./raw-migrated-files/cloud/cloud/ec-enable-logging-and-monitoring.md

# Enable audit logging [enable-audit-logging]

You can log security-related events such as authentication failures and refused connections to monitor your cluster for suspicious activity (including data access authorization and user security configuration changes).

Audit logging also provides forensic evidence in the event of an attack.

::::{important}
Audit logs are **disabled** by default. You must explicitly enable audit logging.
::::

## Enable audit logging in Elasticsearch [enable-audit-logging-elasticsearch]

To enable audit logging:

1. Set `xpack.security.audit.enabled` to `true` in `elasticsearch.yml`.
2. Restart {{es}}.

When audit logging is enabled, [security events](elasticsearch-audit-events.md) are persisted to a dedicated `<clustername>_audit.json` file on the host’s file system, on every cluster node. For more information, see [Logfile audit output](logfile-audit-output.md).

::::{note}
You can configure additional options to control what events are logged and what information is included in the audit log. For more information, refer to [{{es}} auditing settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/auditing-settings.html).
::::

## Enable audit logging in Kibana [enable-audit-logging-kibana]

To enable audit logging in {{kib}}:

1. Set `xpack.security.audit.enabled` to `true` in `kibana.yml`
2. Restart {{kib}}

::::{note}
You can optionally configure audit logs location, file/rolling file appenders and ignore filters using [{{kib}} audit logging settings](https://www.elastic.co/guide/en/kibana/current/security-settings-kb.html#audit-logging-settings).
::::

## Enable audit logging in orchestrated deployments [enable-audit-logging-orchestrated]

In orchestrated systems you just need to set the relevant setting through the orchestrator, as with any other {{es}} or {{kib}} setting.

Below you have some examples:

::::::{tab-set}

:::::{tab-item} Elastic Cloud Hosted

To enable audit logs on your deployment:

1. Log in to the [Elasticsearch Service Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the Elasticsearch Service card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the deployments page to view all of your deployments.

  ::::{tip}
  On the deployments page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.
  ::::

3. From your deployment menu, go to the **Edit** page.
4. To enable audit logs in {{es}}, in the **Elasticsearch** section select **Manage user settings and extensions**. For deployments with existing user settings, you may have to expand the **Edit elasticsearch.yml** caret for each node instead.
5. To enable audit logs in {{kib}}, in the **Kibana** section select **Edit user settings**. For deployments with existing user settings, you may have to expand the **Edit kibana.yml** caret instead.
6. Add `xpack.security.audit.enabled: true` to the user settings.
7. Select **Save changes**.

A plan change will run on your deployment. When it finishes, audit logs will be delivered to your monitoring deployment.

:::::

:::::{tab-item} ECE
In Elastic Cloud Enterprise, to get audit events for both Elasticsearch and Kibana, you need to enable auditing for each component separately.

To enable auditing for Elasticsearch:

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.
  ::::{tip}
  On the deployments page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.
  ::::
3. From your deployment menu, go to the **Edit** page.
4. In the **Elasticsearch** section, select **Edit user settings and plugins**. For deployments with existing user settings, you may have to expand the **Edit elasticsearch.yml** caret for the first node instead.
5. Add the setting `xpack.security.audit.enabled: true`.
6. Select **Save**.

For more information and other available auditing settings in Elasticsearch, check [Auditing security settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/auditing-settings.html). Audit logs can be viewed within Elasticsearch logs.

To enable auditing for Kibana:

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.
  ::::{tip}
  On the deployments page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.
  ::::
3. From your deployment menu, go to the **Edit** page.
4. In the **Kibana** section, select **Edit user settings**. For deployments with existing user settings, you may have to expand the **Edit kibana.yml** caret instead.
5. Add the setting `xpack.security.audit.enabled: true`.
6. If your Elastic Stack version is below 7.6.0, add the setting `logging.quiet: false`.
7. Select **Save**.

For more information about audit logging in Kibana, check [Audit Logging](https://www.elastic.co/guide/en/kibana/current/xpack-security-audit-logging.html).
:::::

:::::{tab-item} ECK

Audit logs are collected and shipped to the monitoring cluster referenced in the `monitoring.logs` section when audit logging is enabled (it is disabled by default).

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

:::::

::::::


Orchestrated deployments allow to change certain settings regarding audit logging, such as:

* asdad
* bsdsda
