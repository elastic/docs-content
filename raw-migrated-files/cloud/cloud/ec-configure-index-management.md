# Configure index management [ec-configure-index-management]

::::{important}
Index curation is deprecated. Any deployments using index curation will be prompted to migrate to ILM.
::::


The index lifecycle management (ILM) feature of the Elastic Stack provides an integrated and streamlined way to manage time-based data, making it easier to follow best practices for managing your indices. Compared to index curation, migrating to ILM gives you more fine-grained control over the lifecycle of each index.

For existing hot-warm deployments that are currently using index curation, there are a couple of options for migrating to index lifecycle management (ILM). You can:

* Use the migration process in the console to change an existing deployment to ILM.
* Take a snapshot and restore your data to a new Elastic Stack 6.7+ deployment that has ILM enabled.
* [Create your index lifecyle policy](https://www.elastic.co/guide/en/elasticsearch/reference/current/set-up-lifecycle-policy.html)
* [Managing the index lifecycle](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html)


