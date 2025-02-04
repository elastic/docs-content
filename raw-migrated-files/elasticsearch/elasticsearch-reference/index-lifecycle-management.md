# {{ilm-init}}: Manage the index lifecycle [index-lifecycle-management]

You can configure {{ilm}} ({{ilm-init}}) policies to automatically manage indices according to your performance, resiliency, and retention requirements. For example, you could use {{ilm-init}} to:

* Spin up a new index when an index reaches a certain size or number of documents
* Create a new index each day, week, or month and archive previous ones
* Delete stale indices to enforce data retention standards

You can create and manage index lifecycle policies through {{kib}} Management or the {{ilm-init}} APIs. Default {{ilm}} policies are created automatically when you use {{agent}}, {{beats}}, or the {{ls}} {es} output plugin to send data to the {{stack}}.

![index lifecycle policies](../../../images/elasticsearch-reference-index-lifecycle-policies.png "")

::::{tip}
To automatically back up your indices and manage snapshots, use [snapshot lifecycle policies](../../../deploy-manage/tools/snapshot-and-restore/create-snapshots.md#automate-snapshots-slm).
::::


* [Tutorial: Customize built-in policies](../../../manage-data/lifecycle/index-lifecycle-management/tutorial-customize-built-in-policies.md)
* [Tutorial: Automate rollover](../../../manage-data/lifecycle/index-lifecycle-management/tutorial-automate-rollover.md)
* [Overview](../../../manage-data/lifecycle/index-lifecycle-management.md)
* [Concepts](../../../manage-data/lifecycle/index-lifecycle-management/concepts.md)
* [*Configure a lifecycle policy*](../../../manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md)
* [*Migrate index allocation filters to node roles*](../../../manage-data/lifecycle/index-lifecycle-management/migrate-index-allocation-filters-to-node-roles.md)
* [*Troubleshooting {{ilm}} errors*](../../../troubleshoot/elasticsearch/elasticsearch-reference/index-lifecycle-management-errors.md)
* [*Start and stop {{ilm}}*](../../../manage-data/lifecycle/index-lifecycle-management/start-stop-index-lifecycle-management.md)
* [*Manage existing indices*](../../../manage-data/lifecycle/index-lifecycle-management/manage-existing-indices.md)
* [*Skip rollover*](../../../manage-data/lifecycle/index-lifecycle-management/skip-rollover.md)
* [*Restore a managed data stream or index*](../../../manage-data/lifecycle/index-lifecycle-management/restore-managed-data-stream-index.md)
* [*{{ilm-cap}} APIs*](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management-api.html)
* [*Index lifecycle actions*](https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-actions.html)

