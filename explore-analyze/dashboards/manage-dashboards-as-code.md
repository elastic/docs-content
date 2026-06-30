---
navigation_title: Manage as code
description: Version-control Kibana dashboards and deploy them across spaces, clusters, and stages using the Dashboards API and Git-based review workflows.
applies_to:
  stack: preview 9.4+
  serverless: preview
products:
  - id: kibana
type: overview
---

# Manage dashboards as code [manage-dashboards-as-code]

Treat dashboards as version-controlled artifacts that live in Git alongside the rest of your infrastructure code. The [Dashboards API](create-dashboards-programmatically.md) produces a clean, diffable JSON definition, so you can review dashboard changes in pull requests and promote them across environments through automated pipelines, the same way you manage data views, alerting rules, or any other resource.

This workflow suits teams that want repeatable, auditable dashboard changes instead of manual edits in the UI, and assumes you are comfortable with Git and your CI/CD system. If you only need to move a dashboard between environments once, [exporting it as NDJSON](sharing.md#export-ndjson) and [importing it](import-dashboards.md) is simpler.

## Workflow [dashboards-as-code-workflow]

The same four stages apply whether you manage dashboards with the Dashboards API directly or with the Terraform provider:

| Stage | What happens | With the Dashboards API | With Terraform |
| --- | --- | --- | --- |
| **Export** | Produce a clean, diffable definition of the dashboard, without the internal state that makes raw saved objects hard to read. | [Export the dashboard as API-compatible JSON](sharing.md#export-dashboard-json). | Author the dashboard directly in HCL; there is no export step. |
| **Store** | Commit the definition to Git as the source of truth, so every change is tracked and reversible. | Commit the exported JSON file. | Commit the `.tf` configuration. |
| **Review** | Review changes in a pull request before they ship. | Diff the structured JSON to see exactly which panel, query, or filter changed. | Diff the HCL, and run `terraform plan` to preview the change. |
| **Deploy** | Apply the definition to each target environment, reusing the same source to keep development, staging, and production in sync. | Send the definition to the Dashboards API in each environment. | Run `terraform apply` per environment or workspace. |

To roll back a change, revert the commit and redeploy. For the request schema and authentication details, refer to the [Dashboards API reference](https://elastic.github.io/dashboards-api-spec/dashboards#tag/Dashboards).

## Manage IDs across environments [dashboards-as-code-ids]

A dashboard's ID determines whether a deployment updates an existing dashboard or creates a new one. To promote the same dashboard repeatedly across environments, deploy it with a stable, chosen ID rather than letting the API generate one. When you create a dashboard with a fixed ID, later deployments with that ID update the existing dashboard in place instead of creating duplicates.

To deploy a dashboard to a different space within the same cluster, include the destination space's ID in the request URL. The [JSON export flow](sharing.md#export-dashboard-json) can open a pre-populated request in {{kib}} Dev Tools Console, where you set the destination space before sending it.

## Manage references to data views and saved objects [dashboards-as-code-references]

Panels can reference other saved objects, such as data views or Discover sessions. A reference only resolves if the object it points to exists in the target environment with a matching ID. When you plan how to handle references, choose one of these approaches:

- **Provision the referenced objects first**, with stable IDs, in every environment. The dashboard then resolves its references consistently wherever you deploy it.
- **Avoid external references** by backing panels with [{{esql}}](/explore-analyze/query-filter/languages/esql-kibana.md) queries or ad-hoc index patterns defined directly in the panel. These definitions are self-contained and don't depend on a saved data view in the target environment.

## Choose inline or library panels [dashboards-as-code-panels]

The Dashboards API supports two ways to define a visualization panel, and the choice affects how portable your definition is. The API refers to these as **by value** (inline) and **by reference** (library):

- **Inline panels** define the visualization entirely within the dashboard definition. The dashboard is self-contained and carries no external references to resolve, which makes it the most portable option for deploying across environments.
- **Library panels** are stored as standalone [visualizations](create-dashboards-programmatically.md#lens-visualizations-api) and embedded by reference. Use them when you want to reuse a chart across multiple dashboards and have a single update propagate everywhere. The referenced visualization must exist in the target environment.

Prefer inline panels when portability matters most, and library panels when reuse across dashboards matters most.

## Automate with Terraform [dashboards-as-code-terraform]

If you already manage your infrastructure with Terraform, the [Elastic Stack Terraform provider](https://registry.terraform.io/providers/elastic/elasticstack/latest/docs/resources/kibana_dashboard) includes an `elasticstack_kibana_dashboard` resource that manages dashboards through the Dashboards API. You define the dashboard in the provider's own configuration schema, then apply it like any other resource, so dashboard changes flow through `terraform plan` and `terraform apply` alongside the rest of your stack.

The provider documentation includes step-by-step guides with complete, runnable examples:

- [Getting started with Kibana dashboards](https://registry.terraform.io/providers/elastic/elasticstack/latest/docs/guides/kibana-dashboard-getting-started) builds a web server logs dashboard one panel at a time, covering the layout grid and Lens metric, line, bar, and donut panels.
- [Kibana dashboard operations guide](https://registry.terraform.io/providers/elastic/elasticstack/latest/docs/guides/kibana-dashboard-operations) adds pinned controls that filter every panel at once, a KPI row, a data table, and an embedded Discover session.
- [Advanced Kibana dashboard patterns](https://registry.terraform.io/providers/elastic/elasticstack/latest/docs/guides/kibana-dashboard-advanced) covers collapsible sections, image panels, {{esql}} controls, access control, and tags.

This resource is in technical preview and still evolving. Keep two things in mind when you plan an adoption:

- **There's no automatic conversion from an exported dashboard to Terraform.** The JSON you export from a dashboard doesn't map to the resource's schema, so Terraform suits dashboards you author as code from the start rather than existing dashboards you want to bring in. You can place an existing dashboard under Terraform management with `terraform import`, but you still write the matching configuration by hand.
- **Confirm the schema covers the panels you need.** The resource doesn't yet expose every panel type and dashboard-level option that the Dashboards API supports.

For every attribute and panel type, refer to the [`elasticstack_kibana_dashboard` resource reference](https://registry.terraform.io/providers/elastic/elasticstack/latest/docs/resources/kibana_dashboard).

## Next steps [manage-dashboards-as-code-next-steps]

To put this workflow into practice, choose the path that matches your tooling:

- **Use the Dashboards API directly**: start with [Create dashboards programmatically](create-dashboards-programmatically.md), which introduces the API and links to its full reference.
- **Manage dashboards with Terraform**: follow [Getting started with Kibana dashboards](https://registry.terraform.io/providers/elastic/elasticstack/latest/docs/guides/kibana-dashboard-getting-started) to build your first dashboard as code.

## Related pages [manage-dashboards-as-code-related]

- [Create dashboards programmatically](create-dashboards-programmatically.md): overview of the Dashboards API and Visualizations API.
- [Sharing dashboards](sharing.md): export a dashboard as Dashboards API-compatible JSON or as NDJSON saved objects.
- [Import dashboards](import-dashboards.md): import dashboards and their related saved objects.
- [Organize dashboard panels](arrange-panels.md): grid layout and panel limits when you position panels by hand.
- [Dashboards API reference](https://elastic.github.io/dashboards-api-spec/dashboards#tag/Dashboards): endpoints, request schema, and authentication.
- [Elastic Stack Terraform provider](https://registry.terraform.io/providers/elastic/elasticstack/latest/docs): manage Kibana dashboards and other Elastic resources as Terraform configuration.
- [Kibana dashboards as code: GitOps with Terraform](https://www.elastic.co/search-labs/blog/kibana-dashboards-as-code-terraform-api) (May 2026): Elastic Search Labs blog on the Dashboards API and the Terraform resource.
