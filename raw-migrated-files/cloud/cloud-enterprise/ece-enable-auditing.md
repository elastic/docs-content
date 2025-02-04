# Enable auditing [ece-enable-auditing]

With auditing enabled you can keep track of security-related events, such as successful and unsuccessful authorization attempts on the cluster. In Elastic Cloud Enterprise, to get audit events for both Elasticsearch and Kibana, you need to enable auditing for each component separately.

To enable auditing for Elasticsearch:

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From your deployment menu, go to the **Edit** page.
4. In the **Elasticsearch** section, select **Edit user settings and plugins**. For deployments with existing user settings, you may have to expand the **Edit elasticsearch.yml** caret for the first node instead.
5. Add the setting `xpack.security.audit.enabled: true`.
6. Select **Save**.

For more information and other available auditing settings in Elasticsearch, check [Auditing security settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/auditing-settings.html). Audit logs can be viewed within Elasticsearch logs.

To enable auditing for Kibana:

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From your deployment menu, go to the **Edit** page.
4. In the **Kibana** section, select **Edit user settings**. For deployments with existing user settings, you may have to expand the **Edit kibana.yml** caret instead.
5. Add the setting `xpack.security.audit.enabled: true`.
6. If your Elastic Stack version is below 7.6.0, add the setting `logging.quiet: false`.
7. Select **Save**.

For more information about audit logging in Kibana, check [Audit Logging](https://www.elastic.co/guide/en/kibana/current/xpack-security-audit-logging.html).

