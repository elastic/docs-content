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

Store your dashboards as code, so you can review changes in pull requests, deploy them across spaces, clusters, and environments, and roll back by reverting a commit, instead of editing them by hand in each {{kib}} instance.

Elastic gives you two ways to define a dashboard as code:

- The [Dashboards API](create-dashboards-programmatically.md) produces a clean, diffable JSON definition that you can create and apply from any tool or language.
- The [Elastic Stack Terraform provider](#dashboards-as-code-terraform) builds on that API with a dashboard resource, so you can manage dashboards with Terraform alongside the rest of your infrastructure as code (IaC).

This workflow suits teams that want repeatable, auditable dashboard changes, and assumes you are comfortable with Git and your CI/CD system.

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

## Keep references portable across environments [dashboards-as-code-portability]

The main challenge in moving a dashboard between spaces, clusters, or stages is that a dashboard and the objects it references, such as data views and library visualizations, are matched by ID. Because these IDs are auto-generated and differ across environments, a dashboard exported from one environment can point at objects that don't exist in another, and its panels show no data until the references resolve.

To keep a dashboard portable, choose one of the following approaches, listed from most to least automated.

### Manage dashboards with Terraform [dashboards-as-code-portability-terraform]

If you already manage infrastructure as code, the Terraform provider handles ID consistency for you: it tracks each resource and maps IDs per environment, so references stay consistent as you promote a dashboard from development to production. Refer to [Automate with Terraform](#dashboards-as-code-terraform).

### Define panels with {{esql}} [dashboards-as-code-portability-inline]

The most portable way to build a panel is to define its visualization with [{{esql}}](/explore-analyze/query-filter/languages/esql-kibana.md) directly in the dashboard. This lets you:

- **Keep the visualization inline**, so its definition lives in the dashboard rather than pointing to a standalone [library visualization](create-dashboards-programmatically.md#lens-visualizations-api) that must already exist, with a matching ID, in the target environment.
- **Skip the data view**, because {{esql}} queries indices by name rather than through a saved data view.

The result carries no external references, so the dashboard stays fully portable. For a panel that can't use {{esql}}, define it by value and back it with an [ad-hoc data view](../find-and-organize/data-views.md#_create_a_temporary_data_source) to keep it just as self-contained.

### Assign matching IDs to referenced objects [dashboards-as-code-portability-ids]

If you keep references to saved objects, give each object the same ID in every environment so the references always resolve:

- **Dashboards and library visualizations**: create them with the [Dashboards API](https://elastic.github.io/dashboards-api-spec/dashboards#tag/Dashboards) and [Visualizations API](https://elastic.github.io/dashboards-api-spec/visualizations#tag/Visualizations) using `PUT` (upsert) with a chosen ID (`PUT /api/dashboards/{id}` or `PUT /api/visualizations/{id}`), rather than `POST`, which generates a new ID each time. Because the exported definition already contains these IDs, re-importing it with `PUT` recreates the same objects, with the same IDs, in the target environment.
- **Data views**: create them with a chosen ID, either through the [Data Views API]({{kib-apis}}operation/operation-createdataviewdefaultw) by passing an `id` in the POST request, or in the UI by [setting a **Custom data view ID**](../find-and-organize/data-views.md#settings-create-pattern). Use human-readable IDs, such as `logs-prod`, so they are easy to reuse and recognize.

Regardless of the approach, to deploy a dashboard to a different space within the same cluster, include the destination space's ID in the request URL. The [JSON export flow](sharing.md#export-dashboard-json) can open a pre-populated request in {{kib}} Dev Tools Console, where you set the destination space before sending it.

## Automate with Terraform [dashboards-as-code-terraform]

If you already manage your infrastructure with Terraform, the [Elastic Stack Terraform provider](https://registry.terraform.io/providers/elastic/elasticstack/latest/docs/resources/kibana_dashboard) includes an `elasticstack_kibana_dashboard` resource that manages dashboards through the Dashboards API. You define the dashboard in the provider's own configuration schema, then apply it like any other resource, so dashboard changes flow through `terraform plan` and `terraform apply` alongside the rest of your stack.

Terraform is the IaC option that Elastic maintains and documents. Because `elasticstack_kibana_dashboard` is a standard Terraform provider resource, other IaC tools that support Terraform providers can manage it too, including from languages other than HCL.

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
