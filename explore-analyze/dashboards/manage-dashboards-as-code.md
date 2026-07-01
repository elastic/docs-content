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

This workflow suits teams that want repeatable, auditable dashboard changes instead of manual edits in the UI, and assumes you are comfortable with Git and your CI/CD system.

## Workflow [dashboards-as-code-workflow]

The same four stages apply whether you manage dashboards with the Dashboards API directly or with the Terraform provider:

| Stage | What happens | With the Dashboards API | With Terraform |
| --- | --- | --- | --- |
| **Export** | Produce a clean, diffable definition of the dashboard, without the internal state that makes raw saved objects hard to read. | [Export the dashboard as API-compatible JSON](sharing.md#export-dashboard-json). | Author the dashboard directly in HCL; there is no export step. |
| **Store** | Commit the definition to Git as the source of truth, so every change is tracked and you can roll back by reverting the commit. | Commit the exported JSON file. | Commit the `.tf` configuration. |
| **Review** | Review changes in a pull request before they ship. | Diff the structured JSON to see exactly which panel, query, or filter changed. | Diff the HCL, and run `terraform plan` to preview the change. |
| **Deploy** | Apply the definition to each target environment, reusing the same source to keep development, staging, and production in sync. | Send the definition to the Dashboards API in each environment. | Run `terraform apply` per environment or workspace. |

Once a dashboard is managed as code, treat Git as the single source of truth: changes made directly in the UI are overwritten the next time you deploy.

For the request schema and authentication details, refer to the [Dashboards API reference](https://elastic.github.io/dashboards-api-spec/dashboards#tag/Dashboards).

## Design for portability across environments [dashboards-as-code-portability]

The same definition should deploy cleanly into every target environment. Keep these considerations in mind so a dashboard behaves the same wherever you apply it.

### Use stable IDs [dashboards-as-code-ids]

A dashboard's ID determines whether a deployment updates an existing dashboard or creates a new one. To promote the same dashboard repeatedly across environments, deploy it with a stable, chosen ID rather than letting the API generate one. When you create a dashboard with a fixed ID, later deployments with that ID update the existing dashboard in place instead of creating duplicates.

To deploy a dashboard to a different space within the same cluster, include the destination space's ID in the request URL. The [JSON export flow](sharing.md#export-dashboard-json) can open a pre-populated request in {{kib}} Dev Tools Console, where you set the destination space before sending it.

### Handle references to data views and saved objects [dashboards-as-code-references]

Panels can reference other saved objects, such as data views or Discover sessions. A reference only resolves if the object it points to exists in the target environment with a matching ID. When you plan how to handle references, choose one of these approaches:

- **Provision the referenced objects first**, with stable IDs, in every environment. The dashboard then resolves its references consistently wherever you deploy it.
- **Avoid external references** by backing panels with [{{esql}}](/explore-analyze/query-filter/languages/esql-kibana.md) queries or ad-hoc index patterns defined directly in the panel. These definitions are self-contained and don't depend on a saved data view in the target environment.

### Choose inline or library panels [dashboards-as-code-panels]

How you define a visualization panel affects portability. **Inline panels** (by value) embed the visualization in the dashboard definition, so it's self-contained and the most portable across environments. **Library panels** (by reference) point to a standalone [saved visualization](create-dashboards-programmatically.md#lens-visualizations-api) that must already exist in the target environment, but let you reuse one chart across dashboards and update it in a single place. Prefer inline panels when portability matters most, and library panels when reuse matters most.

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

- **Use the Dashboards API directly**: see the [Dashboards API reference](https://elastic.github.io/dashboards-api-spec/dashboards#tag/Dashboards) for the request schema and authentication, or [Create dashboards programmatically](create-dashboards-programmatically.md) for an overview of the supported panel types and limits.
- **Manage dashboards with Terraform**: follow [Getting started with Kibana dashboards](https://registry.terraform.io/providers/elastic/elasticstack/latest/docs/guides/kibana-dashboard-getting-started) to build your first dashboard as code.

For the background on this workflow and a worked Terraform example, see the [Kibana dashboards as code: GitOps with Terraform](https://www.elastic.co/search-labs/blog/kibana-dashboards-as-code-terraform-api) blog (May 2026).
