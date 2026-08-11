---
layout: hub
description: Logstash documentation. Collect events from any source, transform and enrich them, and ship to Elasticsearch or other destinations.
---

:::{hero}
:icon: logstash
:title: Logstash documentation hub
:description: Real-time server-side data processing pipeline. Collect from many sources, transform and enrich events, and ship to Elasticsearch or other outputs.
:primary-action: [Get started](#get-started)
:secondary-action: [What's new](#whats-new)
:tertiary-action: [Explore Logstash docs](#explore)
:::

:::{get-started}
title: Get started in 3 steps
intro: Install Logstash locally or send events to a free Elastic Cloud trial, then build your first pipeline.
steps:
  - title: Run Logstash
    options:
      - label: Run locally
        description: Install Logstash on your machine (packages or Docker). Prefer this for development, testing pipelines, and full control of the runtime.
        url: logstash://reference/installing-logstash.md
        url-label: Install Logstash
      - label: Try on Cloud
        # OPEN: Logstash-specific Cloud trial deep-link (Florent/Ziv). Default ES3 project registration is a placeholder.
        description: Start a free Elastic Cloud trial as your Elasticsearch destination. Prefer this when you want managed Elasticsearch; you still run Logstash as the shipper.
        url: https://cloud.elastic.co/registration
        url-label: Start a free trial
  - title: Create your first pipeline
    description: Define inputs, filters, and outputs, then run a simple pipeline end to end.
    link: logstash://reference/creating-logstash-pipeline.md
    link-label: Create a pipeline
  - title: Ship to Elasticsearch
    description: Configure the Elasticsearch output and secure the connection (TLS, API keys).
    link: logstash://reference/secure-connection.md
    link-label: Secure your connection
:::

:::{whats-new}
:product: logstash
:::

::::{card-group}
:title: Popular topics
:id: popular
:intro: High-demand Logstash topics from documentation search.

:::{link-card}
title: Grok parsing
link: logstash://reference/plugins-filters-grok.md
links:
  - label: Grok filter plugin
    url: logstash://reference/plugins-filters-grok.md
  - label: Grok Debugger
    url: /explore-analyze/query-filter/tools/grok-debugger.md
  - label: Grok pattern reference
    url: /explore-analyze/scripting/grok.md
:::

:::{link-card}
title: Install and run
link: logstash://reference/installing-logstash.md
links:
  - label: Installing Logstash
    url: logstash://reference/installing-logstash.md
  - label: Docker
    url: logstash://reference/docker.md
  - label: Windows
    url: logstash://reference/running-logstash-windows.md
:::

:::{link-card}
title: Plugins
link: logstash://reference/input-plugins.md
links:
  - label: Input plugins
    url: logstash://reference/input-plugins.md
  - label: Filter plugins
    url: logstash://reference/filter-plugins.md
  - label: Output plugins
    url: logstash://reference/output-plugins.md
:::
::::

:::::{explore}
:id: explore
:title: Explore Logstash
:intro: Find Logstash documentation by task, from deploying and building pipelines to securing, troubleshooting, and reference.

::::{card-group}
:title: Quick links
:id: quick-links

:::{link-card}
title: Releases and APIs
links:
  - label: Release notes
    url: logstash://release-notes/index.md
  - label: Logstash API docs
    url: https://www.elastic.co/docs/api/doc/logstash
  - label: Breaking changes
    url: logstash://release-notes/breaking-changes.md
:::

:::{link-card}
title: Configuration
links:
  - label: Configuration files
    url: logstash://reference/config-setting-files.md
  - label: logstash.yml
    url: logstash://reference/logstash-settings-file.md
  - label: Config examples
    url: logstash://reference/config-examples.md
:::

:::{link-card}
title: Plugins
links:
  - label: Working with plugins
    url: logstash://reference/working-with-plugins.md
  - label: Input plugins
    url: logstash://reference/input-plugins.md
  - label: Output plugins
    url: logstash://reference/output-plugins.md
:::
::::

::::{card-group}
:title: Deploy and manage
:id: deploy

:::{link-card}
title: Install
link: logstash://reference/installing-logstash.md
description: Install and run Logstash on your own infrastructure.
links:
  - label: Installing Logstash
    url: logstash://reference/installing-logstash.md
  - label: Docker
    url: logstash://reference/docker.md
  - label: Docker configuration
    url: logstash://reference/docker-config.md
  - label: Windows
    url: logstash://reference/running-logstash-windows.md
  - label: Setting up and running
    url: logstash://reference/setting-up-running-logstash.md
:::

:::{link-card}
title: Orchestrate
link: /deploy-manage/deploy/cloud-on-k8s/logstash.md
description: Run Logstash on Kubernetes with ECK or plain manifests.
links:
  - label: Elastic Cloud on Kubernetes (ECK)
    url: /deploy-manage/deploy/cloud-on-k8s/logstash.md
  - label: ECK configuration examples
    url: /deploy-manage/deploy/cloud-on-k8s/configuration-examples-logstash.md
  - label: Running on Kubernetes
    url: logstash://reference/running-logstash-kubernetes.md
:::

:::{link-card}
title: Operate
link: logstash://reference/upgrading-logstash.md
description: Upgrade, scale, tune, and monitor Logstash.
links:
  - label: Upgrade Logstash
    url: logstash://reference/upgrading-logstash.md
  - label: Deploy and scale
    url: logstash://reference/deploying-scaling-logstash.md
  - label: Tuning
    url: logstash://reference/tuning-logstash.md
  - label: Monitoring
    url: logstash://reference/monitoring-logstash.md
  - label: Monitoring UI
    url: logstash://reference/logstash-monitoring-ui.md
:::

:::{link-card}
title: Configure
link: logstash://reference/config-setting-files.md
description: Settings files, YAML config, and config reload.
links:
  - label: Configuration files
    url: logstash://reference/config-setting-files.md
  - label: logstash.yml
    url: logstash://reference/logstash-settings-file.md
  - label: Reload configuration
    url: logstash://reference/reloading-config.md
:::
::::

::::{card-group}
:title: Ingest
:id: ingest

:::{link-card}
title: Build pipelines
link: logstash://reference/creating-logstash-pipeline.md
description: Create and structure Logstash pipelines.
links:
  - label: Creating a pipeline
    url: logstash://reference/creating-logstash-pipeline.md
  - label: How Logstash works
    url: logstash://reference/how-logstash-works.md
  - label: Multiple pipelines
    url: logstash://reference/multiple-pipelines.md
  - label: Parsing logs tutorial
    url: logstash://reference/advanced-pipeline.md
:::

:::{link-card}
title: Inputs
link: logstash://reference/input-plugins.md
description: Collect events from files, beats, agents, JDBC, and more.
links:
  - label: Input plugins
    url: logstash://reference/input-plugins.md
  - label: JDBC input
    url: logstash://reference/plugins-inputs-jdbc.md
  - label: Beats input
    url: logstash://reference/plugins-inputs-beats.md
  - label: Filebeat → Logstash
    url: beats://reference/filebeat/logstash-output.md
  - label: Elastic Agent → Logstash
    url: /reference/fleet/logstash-output.md
:::

:::{link-card}
title: Outputs
link: logstash://reference/output-plugins.md
description: Send processed events to Elasticsearch and other destinations.
links:
  - label: Output plugins
    url: logstash://reference/output-plugins.md
  - label: Elasticsearch output
    url: logstash://reference/plugins-outputs-elasticsearch.md
  - label: Logstash-to-Logstash
    url: logstash://reference/logstash-to-logstash-communications.md
  - label: Logstash → Elasticsearch architecture
    url: /manage-data/ingest/ingest-reference-architectures/ls-for-input.md
:::

:::{link-card}
title: Central management and integrations
link: logstash://reference/logstash-centralized-pipeline-management.md
description: Manage pipelines from Kibana and extend Elastic Integrations.
links:
  - label: Centralized pipeline management
    url: logstash://reference/logstash-centralized-pipeline-management.md
  - label: Logstash pipelines in Kibana
    url: /manage-data/ingest/transform-enrich/logstash-pipelines.md
  - label: Elastic Integrations
    url: logstash://reference/using-logstash-with-elastic-integrations.md
:::
::::

::::{card-group}
:title: Search and analyze
:id: search

:::{link-card}
title: Parse unstructured logs
link: logstash://reference/plugins-filters-grok.md
description: Extract fields from log lines with grok, dissect, and pipeline tutorials.
links:
  - label: Grok filter
    url: logstash://reference/plugins-filters-grok.md
  - label: Dissect filter
    url: logstash://reference/plugins-filters-dissect.md
  - label: Parsing logs with Logstash
    url: logstash://reference/advanced-pipeline.md
  - label: Field extraction
    url: logstash://reference/field-extraction.md
:::

:::{link-card}
title: Debug patterns
link: /explore-analyze/query-filter/tools/grok-debugger.md
description: Build and test grok patterns before you deploy them.
links:
  - label: Grok Debugger
    url: /explore-analyze/query-filter/tools/grok-debugger.md
  - label: Grok pattern reference
    url: /explore-analyze/scripting/grok.md
:::

:::{link-card}
title: Filter and enrich
link: logstash://reference/filter-plugins.md
description: Transform events with filters and Elastic Integrations processing.
links:
  - label: Filter plugins
    url: logstash://reference/filter-plugins.md
  - label: Mutate filter
    url: logstash://reference/plugins-filters-mutate.md
  - label: Elastic Integration filter
    url: logstash://reference/plugins-filters-elastic_integration.md
  - label: Transforming data
    url: logstash://reference/transforming-data.md
:::

:::{link-card}
title: Inspect pipelines
link: logstash://reference/logstash-pipeline-viewer.md
description: View pipeline topology and processing in Kibana.
links:
  - label: Pipeline viewer
    url: logstash://reference/logstash-pipeline-viewer.md
:::
::::

::::{card-group}
:title: Secure
:id: security

:::{link-card}
title: Secrets
link: logstash://reference/keystore.md
description: Store credentials and sensitive settings in the Logstash keystore.
links:
  - label: Logstash keystore
    url: logstash://reference/keystore.md
:::

:::{link-card}
title: Connect to Elasticsearch
link: logstash://reference/secure-connection.md
description: TLS, authentication, and API keys for Elasticsearch and Serverless.
links:
  - label: Secure your connection
    url: logstash://reference/secure-connection.md
  - label: Connecting to Elastic Cloud
    url: logstash://reference/connecting-to-cloud.md
:::

:::{link-card}
title: TLS on the wire
link: /reference/fleet/secure-logstash-connections.md
description: Secure connections between agents, Beats, and Logstash.
links:
  - label: Secure Logstash connections (Fleet)
    url: /reference/fleet/secure-logstash-connections.md
  - label: Filebeat SSL to Logstash
    url: beats://reference/filebeat/configuring-ssl-logstash.md
:::
::::

::::{card-group}
:title: Troubleshoot
:id: troubleshoot

:::{link-card}
title: Diagnose common issues
link: /troubleshoot/ingest/logstash.md
description: Startup, pipeline, and ingestion troubleshooting.
links:
  - label: Troubleshoot Logstash
    url: /troubleshoot/ingest/logstash.md
  - label: Performance troubleshooting
    url: logstash://reference/performance-troubleshooting.md
  - label: Monitoring troubleshooting
    url: logstash://reference/monitoring-troubleshooting.md
:::

:::{link-card}
title: Capture diagnostics
link: /troubleshoot/ingest/logstash/diagnostic.md
description: Collect diagnostics for support and debugging.
links:
  - label: Capture Logstash diagnostics
    url: /troubleshoot/ingest/logstash/diagnostic.md
:::

:::{link-card}
title: Logging
link: logstash://reference/logging.md
description: Configure and read Logstash logs.
links:
  - label: Logging
    url: logstash://reference/logging.md
:::
::::

::::{card-group}
:title: Reference
:id: reference

:::{link-card}
title: Plugins
link: logstash://reference/working-with-plugins.md
description: Install, list, and configure Logstash plugins.
links:
  - label: Working with plugins
    url: logstash://reference/working-with-plugins.md
  - label: Input plugins
    url: logstash://reference/input-plugins.md
  - label: Filter plugins
    url: logstash://reference/filter-plugins.md
  - label: Codec plugins
    url: logstash://reference/codec-plugins.md
  - label: Output plugins
    url: logstash://reference/output-plugins.md
:::

:::{link-card}
title: Settings and config
link: logstash://reference/logstash-settings-file.md
description: Settings reference and configuration examples.
links:
  - label: logstash.yml
    url: logstash://reference/logstash-settings-file.md
  - label: Configuration file structure
    url: logstash://reference/configuration-file-structure.md
  - label: Config examples
    url: logstash://reference/config-examples.md
:::

:::{link-card}
title: APIs
link: https://www.elastic.co/docs/api/doc/logstash
description: Logstash APIs for monitoring and management.
links:
  - label: Logstash API docs
    url: https://www.elastic.co/docs/api/doc/logstash
  - label: Monitoring
    url: logstash://reference/monitoring-logstash.md
:::

:::{link-card}
title: Releases
link: logstash://release-notes/index.md
description: What's new, breaking changes, and upgrades.
links:
  - label: Release notes
    url: logstash://release-notes/index.md
  - label: Breaking changes
    url: logstash://release-notes/breaking-changes.md
  - label: Upgrade Logstash
    url: logstash://reference/upgrading-logstash.md
:::
::::

:::::
