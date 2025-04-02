---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/saved-object-migrations.html
applies_to:
  stack:
  deployment:
    eck:
    ess:
    ece:
    self:
---

# Saved object migrations [saved-object-migrations]

Each time you upgrade {{kib}}, an upgrade migration is performed to ensure that all [saved objects](/explore-analyze/find-and-organize/saved-objects.md) are compatible with the new version.

::::{note} 
{{kib}} includes an [**Upgrade Assistant**](../prepare-to-upgrade/upgrade-assistant.md) to help you prepare to upgrade. To access the assistant, go to **Stack Management > Upgrade Assistant**.
::::


% ::::{warning} 
% {{kib}} 7.12.0 and later uses a new migration process and index naming scheme. % Before you upgrade, read the documentation for your version of {{kib}}.
% ::::

## How saved object migrations work [upgrade-migrations-process] 

When you start a new {{kib}} installation, an upgrade migration is performed before starting plugins or serving HTTP traffic. Before you upgrade, shut down old nodes to prevent losing acknowledged writes.
If the upgrade includes breaking changes, the old saved objects will be reindexed into new indices. Otherwise, the existing indices will be reused, and saved object documents will be updated in place.

Saved objects are stored in multiple indices. While they all start with the `.kibana*` prefix, other `.kibana*` indices exist but are not used to store saved objects.  The following table lists the saved objects indices used by each {{kib}} version.

| Upgrading from version | Index | Aliases |
| --- | --- | --- |
| 6.5.0 through 7.3.x | `.kibana_N` | `.kibana` |
| 7.4.0 through 7.11.x | `.kibana_N`<br>`.kibana_task_manager_N` | `.kibana`<br>`.kibana_task_manager` |
| 7.11.x through 8.7.x | `.kibana_{{kibana_version}}_001`<br>`.kibana_task_manager_{{kibana_version}}_001` | `.kibana`, `.kibana_{{kibana_version}}`<br>`.kibana_task_manager`, `.kibana_task_manager_{{kibana_version}}` |
| 8.8.0 through 8.15.x | `.kibana_{kibana_version}_001` <br> `.kibana_alerting_cases_{{kibana_version}}_001` <br> `.kibana_analytics_{kibana_version}_001` <br> `.kibana_ingest_{kibana_version}_001`<br> `.kibana_task_manager_{kibana_version}_001` <br> `.kibana_security_solution_{kibana_version}_001` | .`kibana`, `.kibana_{kibana_version}` <br> `.kibana_alerting_cases`, <br> `.kibana_alerting_cases_{kibana_version}` <br> `.kibana_analytics`, <br> `.kibana_analytics_{kibana_version}` <br> `.kibana_ingest`, `.kibana_ingest_{kibana_version}`<br> `.kibana_task_manager`, <br> `.kibana_task_manager_{kibana_version}` <br> `.kibana_security_solution`, <br> `.kibana_security_solution_{kibana_version}`
| 8.16.0+ | `.kibana_usage_counters_{{kibana_version}}_001`| `.kibana_usage_counters_{{kibana_version}}_001`, <br> `.kibana_usage_counters`

Starting on 7.11.0, each of the saved objects indices has a couple of aliases. For example, the `.kibana_8.8.0_001` index has a *default* alias `.kibana` and a *version* alias `.kibana_8.8.0`. The *default* aliases (such as `.kibana` and `.kibana_task_manager`) always point to the most up-to-date saved object indices. Then, *version* aliases are aligned with the deployed {{kib}} version.

Starting on 8.6.0, index names aren’t necessarily aligned with the deployed {{kib}} version. When updates on a certain index are compatible, {{kib}} will keep the existing index instead of creating a new one. This allows for a more efficient upgrade process. The following example illustrates a completely valid state for an 8.8.0 deployment:

* `.kibana_8.8.0_001` index, with `.kibana` and `.kibana_8.8.0` aliases.
* `.kibana_task_manager_8.7.0_001` index, with `.kibana_task_manager` and `.kibana_task_manager_8.8.0` aliases.

Starting on 8.8.0, {{kib}} splits the main saved object index into multiple ones, as depicted in the table above. When upgrading from a previous version, the {{kib}} migration process will reindex some saved objects from the `.kibana` index into the new indices, depending on their types. Note that the `.kibana` index still exists and continues storing multiple saved object types.


## Old {{kib}} indices [upgrade-migrations-old-indices] 

As a deployment is gradually upgraded, multiple {{kib}} indices are created in {{es}}: (`.kibana_1`, `.kibana_2`, `.kibana_7.12.0_001`, `.kibana_7.13.0_001`, `.kibana_8.0.0_001`, etc.). {{kib}} only uses those indices that the *default* and *version* aliases point to. The other, older {{kib}} saved object indices can be safely deleted, but are retained for historical records and to facilitate rolling {{kib}} back to a previous version.

