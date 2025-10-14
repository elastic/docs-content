---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/saved-object-migrations.html
applies_to:
  stack: ga
products:
  - id: kibana
---

# Saved object migrations [saved-object-migrations]

Each time you upgrade {{kib}}, an upgrade migration is performed to ensure that all [saved objects](/explore-analyze/find-and-organize/saved-objects.md) are compatible with the new version.

::::{note}
{{kib}} includes an [**Upgrade Assistant**](../prepare-to-upgrade/upgrade-assistant.md) to help you prepare to upgrade. To access the assistant, go to the **Upgrade Assistant** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
::::


% ::::{warning}
% {{kib}} 7.12.0 and later uses a new migration process and index naming scheme. % Before you upgrade, read the documentation for your version of {{kib}}.
% ::::

## How saved object migrations work [upgrade-migrations-process]

When you start a new {{kib}} installation, an upgrade migration is performed before starting plugins or serving HTTP traffic. Before you upgrade, shut down old nodes to prevent losing acknowledged writes.
If the upgrade includes breaking changes, the old saved objects will be reindexed into new indices. Otherwise, the existing indices will be reused, and saved object documents will be updated.

Saved objects are stored in multiple indices. While they all start with the `.kibana*` prefix, other `.kibana*` indices exist but are not used to store saved objects.
The indices used to store saved objects and the conventions on their names and aliases have evolved as follows:

::::{warning} 
The `kibana.index` and `xpack.tasks.index` configuration settings are obsolete and no longer taken into account in 8.x. If you are using custom index names, perform the necessary adaptations before attempting to upgrade to 8.x.
::::

### Kibana 6.5.0

The `.kibana_N` saved object index is created. Saved objects are reindexed into a new index, and the `N` suffix is incremented each time an upgrade is performed. A `.kibana` alias is maintained, which points to the latest version of the index.

### Kibana 7.4.0

A new `.kibana_task_manager_N` is introduced, which hosts the `task` saved objects. It also has the corresponding `.kibana_task_manager` alias, pointing to the latest version of the index.

### Kibana 7.11.0

Starting with 7.11.0 the naming convention evolves, and the indices names contain the version number, along with a `_001` suffix.
Each of the saved objects indices now has a couple of aliases. For example, the `.kibana_7.11.0_001` index has a *default* `.kibana` alias and a `.kibana_7.11.0` *version* alias. The *default* aliases (such as `.kibana` and `.kibana_task_manager`) always point to the most up-to-date saved object indices. Then, *version* aliases are aligned with the deployed {{kib}} version:

| Alias | Version alias | Index name |
| --- | --- | --- |
| .kibana | .kibana_7.11.0 | .kibana_7.11.0_001 |
| .kibana_task_manager | .kibana_task_manager_7.11.0 | .kibana_task_manager_7.11.0_001 |

### Kibana 8.6.0

In versions 8.6.0 and newer, compatible migrations are introduced, allowing to reuse existing saved object indices as long as changes in the mappings are compatible. After this change, index names aren’t necessarily aligned with the deployed {{kib}} version. When updates on a certain index are compatible, {{kib}} will keep the existing index instead of creating a new one. This allows for a more efficient upgrade process. The following example illustrates a completely valid state for an 8.7.0 deployment:

| Alias | Versioned alias | Index name |
| --- | --- | --- |
| .kibana | .kibana_8.7.0 | .kibana_8.7.0_001 |
| .kibana_task_manager | .kibana_task_manager_8.7.0 | .kibana_task_manager_7.17.0_001 |

### Kibana 8.8.0

Starting with 8.8.0, {{kib}} splits the main saved object index into multiple ones, as depicted in the table below. When upgrading from a previous version, the {{kib}} migration process will reindex some saved objects from the `.kibana` index into the new indices, depending on their types. Note that the `.kibana` index still exists and continues storing multiple saved object types.

| Alias | Version alias | Index name |
| --- | --- | --- |
| .kibana | .kibana_8.8.0 | .kibana_8.8.0_001 |
| .kibana_task_manager | .kibana_task_manager_8.8.0 | .kibana_task_manager_7.17.0_001 |
| .kibana_alerting_cases | .kibana_alerting_cases_8.8.0 | .kibana_alerting_cases_8.8.0_001 |
| .kibana_analytics | .kibana_analytics_8.8.0 | .kibana_analytics_8.8.0_001 |
| .kibana_ingest | .kibana_ingest_8.8.0 | .kibana_ingest_8.8.0_001 |
| .kibana_security_solution | .kibana_security_solution_8.8.0 | .kibana_security_solution_8.8.0_001 |

### Kibana 8.16.0 and newer

A new index is introduced, with the goal of storing the `usage-counter` saved object type, which is expected to have a large number of documents.

| Alias | Version alias | Index name |
| --- | --- | --- |
| .kibana | .kibana_8.8.0 | .kibana_8.8.0_001 |
| .kibana_task_manager | .kibana_task_manager_8.8.0 | .kibana_task_manager_7.17.0_001 |
| .kibana_alerting_cases | .kibana_alerting_cases_8.8.0 | .kibana_alerting_cases_8.8.0_001 |
| .kibana_analytics | .kibana_analytics_8.8.0 | .kibana_analytics_8.8.0_001 |
| .kibana_ingest | .kibana_ingest_8.8.0 | .kibana_ingest_8.8.0_001 |
| .kibana_security_solution | .kibana_security_solution_8.8.0 | .kibana_security_solution_8.8.0_001 |
| .kibana_usage_counters | .kibana_usage_counters_8.8.0 | .kibana_usage_counters_8.8.0_001 |


## Old {{kib}} indices [upgrade-migrations-old-indices]

When you upgrade a deployment, Elastic creates multiple {{kib}} indices in {{es}}: (`.kibana_1`, `.kibana_2`, `.kibana_7.12.0_001`, `.kibana_7.13.0_001`, `.kibana_8.0.0_001`, etc.). {{kib}} only uses those indices that the *default* and *version* aliases point to. You can safely delete the older {{kib}} saved object indices, but they're retained for historical records and to facilitate rolling {{kib}} back to a previous version.
