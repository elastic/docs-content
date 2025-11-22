---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/profiling-tag-data-query.html
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: observability
---

# Tag data for querying [profiling-tag-data-query]

The instructions to deploy the Universal Profiling Agent displayed in **Add Data** show a default configuration that allows ingesting data into an {{ecloud}} deployment. The only config setting you may want to change is `project-id` (default value is `1`).

The `-project-id` flag, or the `project-id` key in the Universal Profiling Agent configuration file, splits profiling data into logical groups that you control.

You can assign any non-zero, unsigned integer ⇐ 4095 to a Universal Profiling Agent deployment you control. In Kibana, the KQL field `profiling.project.id` is mapped to `project-id` and you can use it to split or filter data.

You may want to set a per-environment project ID (for example, dev=3, staging=2, production=1), a per-datacenter project ID (for example, DC1=1, DC2=2), or even a per-k8s-cluster project ID (for example, us-west2-production=100, eu-west1-production=101).

You can also use the `-tags` flag to associate an arbitrary string with a specific Universal Profiling Agent instance. Each tag must match `^[a-zA-Z0-9-:._]+$` regex and use `;` as a separator. Invalid tags are dropped and warnings issued on startup.

In Kibana, you can use the KQL field `tags` for filtering. For example, when running the Universal Profiling Agent with the following:

```bash
sudo pf-host-agent/pf-host-agent -project-id=1 -tags='cloud_region:us-central1;env:staging'
```

You can then filter profiling data from the Universal Profiling Agent in Kibana with the following tag:

```bash
tags : "cloud_region:us-central1"
```

It is also possible to use the environment variable `PRODFILER_TAGS="cloud_region:us-central1;env:staging"` to set this configuration.

