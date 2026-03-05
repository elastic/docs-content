---
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
description: Deployment-level data source settings that affect detection rule behavior across your environment.
---

# Advanced data source configuration

These pages cover deployment-level data settings that affect detection rule behavior. Unlike [per-rule data source settings](/solutions/security/detect-and-alert/set-rule-data-sources.md), which apply to individual rules, the configurations below affect how your entire environment interacts with the detection engine.

Most users don't need these pages during initial setup. Review them if any of the following apply to your environment:

**[{{ccs-cap}} and detection rules](/solutions/security/detect-and-alert/cross-cluster-search-detection-rules.md)**
:   Relevant if your data is spread across multiple {{es}} clusters and you need detection rules on one cluster to query indices on another. Covers trust setup, remote cluster connections, and how to reference remote indices in rule index patterns. {{stack}} only.

**[Using logsdb index mode with {{elastic-sec}}](/solutions/security/detect-and-alert/using-logsdb-index-mode-with-elastic-security.md)**
:   Relevant if your indices use logsdb index mode (enabled by default in {{serverless-short}}). Explains how synthetic `_source` reconstruction can affect field formatting in alerts and rule queries, and what to watch for when writing rules against logsdb-backed indices.
