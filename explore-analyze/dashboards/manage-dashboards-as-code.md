---
navigation_title: Manage as code
description: Version-control Kibana dashboards and deploy them across spaces, clusters, and stages using the dashboards API and Git-based review workflows.
applies_to:
  stack: preview 9.4+
  serverless: preview
products:
  - id: kibana
type: how-to
---

# Manage dashboards as code [manage-dashboards-as-code]

Treat dashboards as version-controlled artifacts that live in Git alongside the rest of your infrastructure code. The [dashboards API](create-dashboards-programmatically.md) produces a clean, diffable JSON definition, so you can review dashboard changes in pull requests and promote them across environments through automated pipelines, the same way you manage data views, alerting rules, or any other resource.

This workflow suits teams that want repeatable, auditable dashboard changes instead of manual edits in the UI. If you only need to move a dashboard between environments once, [exporting it as NDJSON](sharing.md#export-ndjson) and [importing it](import-dashboards.md) is simpler.

## Workflow [dashboards-as-code-workflow]

1. **Export** the dashboard definition. From a dashboard, [export it as dashboards API-compatible JSON](sharing.md#export-dashboard-json). The result is a clean JSON document that contains the panels, controls, and display options, without the internal state that makes raw saved objects hard to read.
2. **Store** the definition in Git. Commit the JSON file to a repository so every change is tracked, diffable, and reversible. To roll back, revert the commit and redeploy.
3. **Review** changes in pull requests. Because the definition is structured and minimal, a reviewer can see exactly which panel, query, or filter changed, rather than parsing a single stringified blob.
4. **Deploy** to your target environments. Send the definition to the dashboards API in each environment as part of your pipeline. Use the same definition to keep development, staging, and production in sync.

For the request schema and authentication details, refer to the [dashboards API reference](https://elastic.github.io/dashboards-api-spec/dashboards#tag/Dashboards).

## Manage IDs across environments [dashboards-as-code-ids]

A dashboard's ID determines whether a deployment updates an existing dashboard or creates a new one. To promote the same dashboard repeatedly across environments, deploy it with a stable, chosen ID rather than letting the API generate one. When you create a dashboard with a fixed ID, later deployments with that ID update the existing dashboard in place instead of creating duplicates.

To deploy a dashboard to a different space within the same cluster, target that space in the API request. When you export a dashboard and select **Open in Console**, you can add the destination space to the request before sending it.

## Manage references to data views and saved objects [dashboards-as-code-references]

Panels can reference other saved objects, such as data views or Discover sessions. A reference only resolves if the object it points to exists in the target environment with a matching ID. When you plan how to handle references, choose one of these approaches:

- **Provision the referenced objects first**, with stable IDs, in every environment. The dashboard then resolves its references consistently wherever you deploy it.
- **Avoid external references** by backing panels with [{{esql}}](/explore-analyze/query-filter/languages/esql-kibana.md) queries or ad-hoc index patterns defined directly in the panel. These definitions are self-contained and don't depend on a saved data view in the target environment.

## Choose inline or library panels [dashboards-as-code-panels]

The dashboards API supports two ways to define a visualization panel, and the choice affects how portable your definition is:

- **Inline panels** define the visualization entirely within the dashboard definition. The dashboard is self-contained and carries no external references to resolve, which makes it the most portable option for deploying across environments.
- **Library panels** are stored as standalone [visualizations](create-dashboards-programmatically.md#lens-visualizations-api) and embedded by reference. Use them when you want to reuse a chart across multiple dashboards and have a single update propagate everywhere. The referenced visualization must exist in the target environment.

Prefer inline panels when portability matters most, and library panels when reuse across dashboards matters most.

## Automate with Terraform [dashboards-as-code-terraform]

If you already manage your infrastructure with Terraform, the [Elastic Stack Terraform provider](https://registry.terraform.io/providers/elastic/elasticstack/latest/docs/resources/kibana_dashboard) includes an `elasticstack_kibana_dashboard` resource that manages dashboards through the dashboards API. You define the dashboard in the provider's own configuration schema, then apply it like any other resource, so dashboard changes flow through `terraform plan` and `terraform apply` alongside the rest of your stack.

The provider documentation includes step-by-step guides with complete, runnable examples:

- [Getting started with Kibana dashboards](https://registry.terraform.io/providers/elastic/elasticstack/latest/docs/guides/kibana-dashboard-getting-started) builds a web server logs dashboard one panel at a time, covering the layout grid and Lens metric, line, bar, and donut panels.
- [Kibana dashboard operations guide](https://registry.terraform.io/providers/elastic/elasticstack/latest/docs/guides/kibana-dashboard-operations) adds pinned controls that filter every panel at once, a KPI row, a data table, and an embedded Discover session.
- [Advanced Kibana dashboard patterns](https://registry.terraform.io/providers/elastic/elasticstack/latest/docs/guides/kibana-dashboard-advanced) covers collapsible sections, image panels, {{esql}} controls, access control, and tags.

This resource is in technical preview and still evolving. Keep two things in mind when you plan an adoption:

- **There's no automatic conversion from an exported dashboard to Terraform.** The JSON you export from a dashboard doesn't map to the resource's schema, so Terraform suits dashboards you author as code from the start rather than existing dashboards you want to bring in. You can place an existing dashboard under Terraform management with `terraform import`, but you still write the matching configuration by hand.
- **Confirm the schema covers the panels you need.** The resource doesn't yet expose every panel type and dashboard-level option that the dashboards API supports.

For every attribute and panel type, refer to the [`elasticstack_kibana_dashboard` resource reference](https://registry.terraform.io/providers/elastic/elasticstack/latest/docs/resources/kibana_dashboard).
