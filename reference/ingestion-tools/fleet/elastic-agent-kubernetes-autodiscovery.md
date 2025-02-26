---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-kubernetes-autodiscovery.html
---

# Kubernetes autodiscovery with Elastic Agent [elastic-agent-kubernetes-autodiscovery]

When you run applications on containers, they become moving targets to the monitoring system. Autodiscover allows you to track them and adapt settings as changes happen. By defining configuration templates, the autodiscover subsystem can monitor services as they start running.

To use autodiscover, you will need to modify the manifest file of the {{agent}}. Refer to [Run {{agent}} Standalone on Kubernetes](/reference/ingestion-tools/fleet/running-on-kubernetes-standalone.md) to learn how to retrieve and configure it.

There are two different ways to use autodiscover:

* [Conditions based autodiscover](/reference/ingestion-tools/fleet/conditions-based-autodiscover.md)
* [Hints annotations based autodiscover](/reference/ingestion-tools/fleet/hints-annotations-autodiscovery.md)


## How to configure autodiscover [_how_to_configure_autodiscover]

`Conditions Based Autodiscover` is more suitable for scenarios when users know the different group of containers they want to monitor in advance. It is advisable to choose conditions-based configuration when administrators can configure specific conditions that match their needs. Conditions are supported in both Managed and Standalone {{agent}}.

`Hints Based Autodiscover` is suitable for more generic scenarios, especially when users don’t know the exact configuration of the system to monitor and can not create in advance conditions. Additionally a big advantage of Hints Autodiscover is the ability to offer dynamic configuration of inputs based on annotations from Pods/Containers. If dynamic configuration is needed, then Hints should be enabled. Hints are supported only in Standalone {{agent}} mode.

**Best Practises when you configure autodiscover:**

* Always define alternatives and default values to your variables that are used in conditions or [hint templates](eg. See `auth.basic` set as `auth.basic.user: ${kubernetes.hints.nginx.access.username|kubernetes.hints.nginx.username|''}`` in [nginx.yml](https://github.com/elastic/elastic-agent/blob/main/deploy/kubernetes/elastic-agent-standalone/templates.d/nginx.yml#L8)))

::::{important}
When an input uses a variable substitution that is not present in the current key/value mappings being evaluated, the input is removed in the result. (See more information in [Variables and conditions in input configurations](/reference/ingestion-tools/fleet/dynamic-input-configuration.md))
::::


* To debug configurations that include variable substitution and conditions, use the inspect command of {{agent}}. (See more information in [Variables and conditions in input configurations](/reference/ingestion-tools/fleet/dynamic-input-configuration.md) in **Debugging** Section)
* In Condition Based autodiscover is advisable to define a generic last condition that will act as your default condition and will be validated when all others fail or don’t apply. If applicable, such conditions might help to identify processing and troubleshoot possible problems.



