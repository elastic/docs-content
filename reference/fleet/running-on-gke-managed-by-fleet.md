---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/running-on-gke-managed-by-fleet.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Run Elastic Agent on GKE managed by Fleet [running-on-gke-managed-by-fleet]

Follow the steps to run the {{agent}} on [Run {{agent}} on Kubernetes managed by {{fleet}}](/reference/fleet/running-on-kubernetes-managed-by-fleet.md) page.


### Important notes: [_important_notes_2]

On managed Kubernetes solutions like GKE, {{agent}} has no access to several data sources. Find below the list of the non-available data:

1. Metrics from [Kubernetes control plane](https://kubernetes.io/docs/concepts/overview/components/#control-plane-components) components are not available. Consequently, metrics are not available for `kube-scheduler` and `kube-controller-manager` components. In this regard, the respective **dashboards** will not be populated with data.
2. **Audit logs** are available only on Kubernetes master nodes as well, hence cannot be collected by {{agent}}.

## Autopilot GKE [_autopilot_gke]

Although autopilot removes many administration challenges (such as workload management or deployment automation of kubernetes clusters), it additionally restricts access to specific namespaces (that is, `kube-system`) and host paths which is the reason that default Elastic Agent manifests would not work.

Specific manifests are provided to cover [Autopilot environments](https://github.com/elastic/elastic-agent/blob/main/docs/elastic-agent-gke-autopilot.md).

`kube-state-metrics` also must be installed to another namespace rather than the `default` as access to `kube-system` is not allowed.

## Additonal Resources: [_additonal_resources]

* Blog [Using Elastic to observe GKE Autopilot clusters](https://www.elastic.co/blog/elastic-observe-gke-autopilot-clusters)
* Elastic speakers webinar: ["Get full Kubernetes visibility into GKE Autopilot with Elastic Observability"](https://www.elastic.co/virtual-events/get-full-kubernetes-visibility-into-gke-autopilot-with-elastic-observability)
