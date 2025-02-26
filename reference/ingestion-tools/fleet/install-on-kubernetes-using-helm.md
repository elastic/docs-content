---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/install-on-kubernetes-using-helm.html
---

# Install Elastic Agent on Kubernetes using Helm [install-on-kubernetes-using-helm]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


Starting with {{stack}} version 8.16, a Helm chart is available for installing {{agent}} in a Kubernetes environment. A Helm-based install offers several advantages, including simplified deployment, availability in marketplaces, streamlined ugrades, as well as quick rollbacks whenever they’re needed.

Features of the Helm-based {{agent}} install include:

* Support for both standalone and {{fleet}}-managed {{agent}}.
* For standalone agents, a built-in Kubernetes policy similar to that available in {{fleet}} for {{fleet}}-managed agents.
* Support for custom integrations.
* Support for {{es}} outputs with authentication through username and password, an API key, or a stored secret.
* Easy switching between privileged (`root`) and unprivileged {{agent}} deployments.
* Support for {{stack}} deployments on {{eck}}.

For detailed install steps, try one of our walk-through examples:

* [Example: Install standalone {{agent}} on Kubernetes using Helm](/reference/ingestion-tools/fleet/example-kubernetes-standalone-agent-helm.md)
* [Example: Install {{fleet}}-managed {{agent}} on {{k8s}} using Helm](/reference/ingestion-tools/fleet/example-kubernetes-fleet-managed-agent-helm.md)

::::{note}
The {{agent}} Helm chart is currently available from inside the [elastic/elastic-agent](https://github.com/elastic/elastic-agent) GitHub repo. It’s planned to soon make the chart available from the Elastic Helm repository.
::::


You can also find details about the Helm chart, including all available YAML settings and descriptions, in the [{{agent}} Helm Chart Readme](https://github.com/elastic/elastic-agent/tree/main/deploy/helm/elastic-agent). Several [examples](https://github.com/elastic/elastic-agent/tree/main/deploy/helm/elastic-agent/examples) are available if you’d like to explore other use cases.

