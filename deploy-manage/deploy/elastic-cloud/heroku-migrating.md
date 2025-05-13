---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-migrating.html
applies_to:
  deployment:
    ess:
products:
  - id: cloud-hosted
---

# Migrate between plans [ech-migrating]

Plans for the {{heroku}} differ based on:

* How much memory and disk space are available
* How many data centers your cluster is replicated across to achieve high availability

Available memory is an important factor for performance when sizing your {{es}} cluster, and replicating across multiple data centers is important for the resilience of production applications.

To learn more about what plans are available for Heroku users, check the [{{es}} add-on](https://elements.heroku.com/addons/foundelasticsearch) in the Elements Marketplace.

You should time the migration to a new plan to ensure proper application function during the migration process. A cluster that is already overwhelmed with requests will take much longer to migrate to a larger capacity; if your workload warrants a plan change to increase capacity, migrate to a larger plan early.

To migrate to a new plan, use the `heroku addons:upgrade` command and include one of the available plans:

```bash
foundelasticsearch:dachs-standard
foundelasticsearch:beagle-standard
foundelasticsearch:dachs-ha
foundelasticsearch:boxer-standard
foundelasticsearch:beagle-ha
foundelasticsearch:labrador-standard
foundelasticsearch:boxer-ha
foundelasticsearch:husky-standard
foundelasticsearch:labrador-ha
foundelasticsearch:husky-ha
```

For example: Migrate from the smallest, default `dachs-standard` plan to the larger `beagle-ha` plan that includes high availability for MY_APP:

```bash
heroku addons:upgrade foundelasticsearch:beagle-ha --app MY_APP
```

Response:
```bash
Changing foundelasticsearch-defined-nnnnn on MY_APP from foundelasticsearch:dachs-standard to foundelasticsearch:beagle-ha... done, $201/month
```

Upgrading to a new plan may involve extending the existing cluster with new nodes and migrating data from the old nodes to the new ones. When the migration is finished, the old nodes are shut down and removed from the cluster. For high availability clusters, you can continue to search and index documents while this plan change is happening.

