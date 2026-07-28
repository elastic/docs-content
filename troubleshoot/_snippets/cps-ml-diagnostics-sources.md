**Where to look**

* **{{ml}} job messages in {{kib}}**: Open **Machine Learning → Anomaly Detection**, select the job, and review the **Job messages** tab for audit entries and warnings about linked projects, credentials, or scope changes. On the **Datafeed** tab, **View datafeed counts** opens the datafeed chart flyout for extraction timing.

  The same entries are stored in `.ml-notifications-*`.
* **`GET _ml/datafeeds/{datafeed_id}`**: Shows the effective `project_routing` value and, when an internal cloud credential exists, `authorization.cloud_api_key.id`.
* **`GET _ml/datafeeds/{datafeed_id}/_stats`**: While the {{dfeed}} runs, shows `remote_cluster_stats` with `total_clusters`, `available_clusters`, `skipped_clusters`, `availability_ratio`, `stabilized_cluster_aliases`, and `per_cluster_consecutive_skips`. The object is absent until the first search cycle establishes a baseline.
* **`.ml-annotations-*`**: Scope-change annotations for the job. The annotation `event` field carries `search_scope_changed` (not the separate `type` field).
* **`GET /_project/tags`**: Lists linked projects and their tags so you can compare them with a routing expression.
* **Elastic Cloud console**: Review linked projects in [Link and manage projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md).

```console
GET _ml/datafeeds/{datafeed_id}
GET _ml/datafeeds/{datafeed_id}/_stats
```
