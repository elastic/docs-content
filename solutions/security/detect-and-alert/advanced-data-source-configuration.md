---
navigation_title: Query clusters, projects, and indices
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
description: Write Elastic Security detection rules that search data in other clusters or linked projects, logsdb indices, or the alerts that other rules create.
---

# Query data from other clusters, projects, and indices

Some rules search data that needs extra setup or care: data in another {{es}} cluster or a linked {{serverless-short}} project, indices that use logsdb index mode, or the alerts that other rules create. To learn how to set the index patterns, data views, and data tiers that any rule searches, refer to [](/solutions/security/detect-and-alert/set-rule-data-sources.md).

Each of these pages explains how to write rules for one kind of data:

**[{{ccs-cap}} and detection rules](/solutions/security/detect-and-alert/cross-cluster-search-detection-rules.md)** {applies_to}`stack: ga`
:   For data in other {{es}} clusters. Explains how to establish trust between clusters, connect to remote clusters, and reference remote indices in a rule's index patterns.

**[{{cps-cap}} and detection rules](/solutions/security/detect-and-alert/cross-project-search-detection-rules.md)** {applies_to}`serverless: ga`
:   For data in linked {{serverless-short}} projects. Explains which projects a rule searches, where {{elastic-sec}} stores the rule's alerts, and how the alert limit applies across projects.

**[Query alert indices](/solutions/security/detect-and-alert/query-alert-indices.md)**
:   For the alerts that other rules create. Explains which index to query, gives example queries, and explains how to write rules that correlate alerts, such as building block alerts from several rules on the same host.

**[Using logsdb index mode with {{elastic-sec}}](/solutions/security/detect-and-alert/using-logsdb-index-mode-with-elastic-security.md)**
:   For indices that use logsdb index mode, which is on by default in {{serverless-short}}. Explains how synthetic `_source` reconstruction can affect field formatting in alerts and rule queries, and what to watch for when you write rules for logsdb indices.
