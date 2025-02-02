---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-custom-repository.html
---

# Snapshot and restore with custom repositories [ech-custom-repository]

Specify your own repositories to snapshot to and restore from. This can be useful, for example, to do long-term archiving of old indexes, restore snapshots across Elastic Cloud accounts, or to be certain you have an exit strategy, should you need to move away from our service.

Elasticsearch Add-On for Heroku supports these repositories:

* [Amazon Web Services (AWS)](ech-aws-custom-repository.md)
* [Google Cloud Storage (GCS)](ech-gcs-snapshotting.md)
* [Azure Blob Storage](ech-azure-snapshotting.md)

::::{note} 
Automated snapshots are only available in the *found snapshots* repository. You are responsible for the execution and maintenance of the snapshots that you store in custom repositories. Note that the automated snapshot frequency might conflict with manual snapshots. You can enable SLM to automate snapshot management in a custom repository.
::::


::::{tip} 
By using a custom repository, you can restore snapshots across regions.
::::





