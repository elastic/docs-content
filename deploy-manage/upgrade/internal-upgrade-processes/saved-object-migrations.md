---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/saved-object-migrations.html
---

# Saved object migrations [saved-object-migrations]

Each time you upgrade {{kib}}, an upgrade migration is performed to ensure that all [saved objects](/explore-analyze/find-and-organize/saved-objects.md) are compatible with the new version.

::::{note} 
{{kib}} includes an [**Upgrade Assistant**](../prepare-to-upgrade/upgrade-assistant.md) to help you prepare for an upgrade. To access the assistant, go to **Stack Management > Upgrade Assistant**.
::::


::::{warning} 
{{kib}} 7.12.0 and later uses a new migration process and index naming scheme. Before you upgrade, read the documentation for your version of {{kib}}.
::::


::::{warning} 
The `kibana.index` and `xpack.tasks.index` configuration settings are obsolete and no longer taken into account in 8.x. If you are using custom index names, please perform the necessary adaptations before attempting to upgrade to 8.x.
::::



## How saved objects migrations work [upgrade-migrations-process] 

When you start a new {{kib}} installation, an upgrade migration is performed before starting plugins or serving HTTP traffic. Before you upgrade, shut down old nodes to prevent losing acknowledged writes. To reduce the likelihood of old nodes losing acknowledged writes, {{kib}} 7.12.0 and later adds a write block to the outdated index.

Saved objects are stored in multiple indices. Whilst all of them start with the `.kibana*` prefix, other `.kibana*` indices exist, which are not used to store saved objects.  The following tables lists the saved objects indices used by each {{kib}} version.

| Upgrading from version | Index | Aliases |
| --- | --- | --- |
| 6.5.0 through 7.3.x | `.kibana_N` | `.kibana` |
| 7.4.0 through 7.11.x | `.kibana_N`<br>`.kibana_task_manager_N` | `.kibana`<br>`.kibana_task_manager` |
| 7.11.x through 8.7.x | `.kibana_{{kibana_version}}_001`<br>`.kibana_task_manager_{{kibana_version}}_001` | `.kibana`, `.kibana_{{kibana_version}}`<br>`.kibana_task_manager`, `.kibana_task_manager_{{kibana_version}}` |
| 8.8.0+ | `.kibana_{{kibana_version}}_001`<br>`.kibana_alerting_cases_{{kibana_version}}_001``.kibana_analytics_{{kibana_version}}_001``.kibana_ingest_{{kibana_version}}_001``.kibana_task_manager_{{kibana_version}}_001``.kibana_security_solution_{{kibana_version}}_001` | `.kibana`, `.kibana_{{kibana_version}}`<br>`.kibana_alerting_cases`, `.kibana_alerting_cases_{{kibana_version}}``.kibana_analytics`, `.kibana_analytics_{{kibana_version}}``.kibana_ingest`, `.kibana_ingest_{{kibana_version}}``.kibana_task_manager`, `.kibana_task_manager_{{kibana_version}}``.kibana_security_solution`, `.kibana_security_solution_{{kibana_version}}` |

Starting on 7.11.0, each of the saved objects indices has a couple of aliases, e.g. the `.kibana_8.8.0_001` index has a *default* alias `.kibana` and a *version* alias `.kibana_8.8.0`. The *default* aliases (e.g. `.kibana` and `.kibana_task_manager`) always point to the most up-to-date saved object indices. Then, *version* aliases are aligned with the deployed {{kib}} version.

Starting on 8.6.0, index names aren’t necessarily aligned with the deployed {{kib}} version. When updates on a certain index are compatible, {{kib}} will keep the existing index instead of creating a new one. This allows for a more efficient upgrade process. The following example illustrates a completely valid state for a 8.8.0 deployment:

* `.kibana_8.8.0_001` index, with `.kibana` and `.kibana_8.8.0` aliases.
* `.kibana_task_manager_8.7.0_001` index, with `.kibana_task_manager` and `.kibana_task_manager_8.8.0` aliases.

Starting on 8.8.0, {{kib}} splits the main saved object index into multiple ones, as depicted on the table above. When upgrading from a previous version, the {{kib}} migration process will reindex some saved objects from the `.kibana` index into the new indices, depending on their types. Note that the `.kibana` index still exists, and it continues to store multiple saved object types.


## Old {{kib}} indices [upgrade-migrations-old-indices] 

As a deployment is gradually upgraded, multiple {{kib}} indices are created in {{es}}: (`.kibana_1`, `.kibana_2`, `.kibana_7.12.0_001`, `.kibana_7.13.0_001`, `.kibana_8.0.0_001` etc). {{kib}} only uses those indices that the *default* and *version* aliases point to. The other, older {{kib}} saved object indices can be safely deleted, but are left around as a matter of historical record, and to facilitate rolling {{kib}} back to a previous version.

