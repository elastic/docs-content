---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/add-fleet-server-cloud.html
---

# Deploy on Elastic Cloud [add-fleet-server-cloud]

To use {{fleet}} for central management, a [{{fleet-server}}](/reference/ingestion-tools/fleet/fleet-server.md) must be running and accessible to your hosts.

{{fleet-server}} can be provisioned and hosted on {{ecloud}}. When the Cloud deployment is created, a highly available set of {{fleet-server}}s is provisioned automatically.

This approach might be right for you if you want to reduce on-prem compute resources and you’d like Elastic to take care of provisioning and life cycle management of your deployment.

With this approach, multiple {{fleet-server}}s are automatically provisioned to satisfy the chosen instance size (instance sizes are modified to satisfy the scale requirement). You can also choose the resources allocated to each {{fleet-server}} and whether you want each {{fleet-server}} to be deployed in multiple availability zones. If you choose multiple availability zones to address your fault-tolerance requirements, those instances are also utilized to balance the load.

This approach might *not* be right for you if you have restrictions on connectivity to the internet.

:::{image} images/fleet-server-cloud-deployment.png
:alt: {{fleet-server}} Cloud deployment model
:::


## Compatibility and prerequisites [fleet-server-compatibility]

{{fleet-server}} is compatible with the following Elastic products:

* {{stack}} 7.13 or later.

    * For version compatibility, {{es}} must be at the same or a later version than {{fleet-server}}, and {{fleet-server}} needs to be at the same or a later version than {{agent}} (not including patch releases).
    * {{kib}} should be on the same minor version as {{es}}.

* {{ece}} 2.10 or later

    * Requires additional wildcard domains and certificates (which normally only cover `*.cname`, not `*.*.cname`). This enables us to provide the URL for {{fleet-server}} of `https://.fleet.`.
    * The deployment template must contain an {{integrations-server}} node.

    For more information about hosting {{fleet-server}} on {{ece}}, refer to [Manage your {{integrations-server}}](/deploy-manage/deploy/cloud-enterprise/manage-integrations-server.md).


::::{note}
The TLS certificates used to secure connections between {{agent}} and {{fleet-server}} are managed by {{ecloud}}. You do not need to create a private key or generate certificates.
::::


When {{es}} or {{fleet-server}} are deployed, components communicate over well-defined, pre-allocated ports. You may need to allow access to these ports. See the following table for default port assignments:

| Component communication | Default port |
| --- | --- |
| Elastic Agent → {{fleet-server}} | 443 |
| Elastic Agent → {{es}} | 443 |
| Elastic Agent → Logstash | 5044 |
| Elastic Agent → {{kib}} ({{fleet}}) | 443 |
| {{fleet-server}} → {{kib}} ({{fleet}}) | 443 |
| {{fleet-server}} → {{es}} | 443 |

::::{note}
If you do not specify the port for {{es}} as 443, the {{agent}} defaults to 9200.
::::



## Setup [add-fleet-server-cloud-set-up]

To confirm that an {{integrations-server}} is available in your deployment:

1. Open {{fleet}}.
2. On the **Agent policies** tab, look for the **{{ecloud}} agent policy**. This policy is managed by {{ecloud}}, and contains a {{fleet-server}} integration and an Elastic APM integration. You cannot modify the policy. Confirm that the agent status is **Healthy**.

:::::{tip}
Don’t see the agent? Make sure your deployment includes an {{integrations-server}} instance. This instance is required to use {{fleet}}.

:::{image} images/integrations-server-hosted-container.png
:alt: Hosted {integrations-server}
:class: screenshot
:::

:::::



## Next steps [add-fleet-server-cloud-next]

Now you’re ready to add {{agent}}s to your host systems. To learn how, see [Install {{fleet}}-managed {{agent}}s](/reference/ingestion-tools/fleet/install-fleet-managed-elastic-agent.md).
