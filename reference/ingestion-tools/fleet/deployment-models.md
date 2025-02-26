---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-deployment-models.html
---

# Deployment models [fleet-deployment-models]

There are various models for setting up {{agents}} to work with {{es}}. The recommended approach is to use {{fleet}}, a web-based UI in Kibana, to centrally manage all of your {{agents}} and their policies. Using {{fleet}} requires having an instance of {{fleet-server}} that acts as the interface between the {{fleet}} UI and your {{agents}}.

For an overview of {{fleet-server}}, including details about how it communicates with {{es}}, how to ensure high availability, and more, refer to [What is {{fleet-server}}?](/reference/ingestion-tools/fleet/fleet-server.md).

The requirements for setting up {{fleet-server}} differ, depending on your particular deployment model:

{{serverless-full}}
:   In a [{{serverless-short}}](/deploy-manage/deploy/elastic-cloud/serverless.md) environment, {{fleet-server}} is offered as a service, it is configured and scaled automatically without the need for any user intervention.

{{ech}}
:   If you’re running {{es}} and {{kib}} with [{{ech}}](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md), no extra setup is required unless you want to scale your deployment. {{ech}} runs a hosted version of {{integrations-server}} that includes {{fleet-server}}. For details about this deployment model, refer to [Deploy on {{ecloud}}](/reference/ingestion-tools/fleet/add-fleet-server-cloud.md).

{{ech}} with {{fleet-server}} on-premise
:   When you use an {{ech}} deployment you may still choose to run {{fleet-server}} on-premise. For details about this deployment model and set up instructions, refer to [Deploy {{fleet-server}} on-premises and {{es}} on Cloud](/reference/ingestion-tools/fleet/add-fleet-server-mixed.md).

Docker and Kubernetes
:   You can deploy {{fleet}}-managed {{agent}} in Docker or on Kubernetes. Refer to [Run {{agent}} in a container](/reference/ingestion-tools/fleet/elastic-agent-container.md) or  [Run {{agent}} on Kubernetes managed by {{fleet}}](/reference/ingestion-tools/fleet/running-on-kubernetes-managed-by-fleet.md) for all of the configuration instructions. For a Kubernetes install we also have a [Helm chart](/reference/ingestion-tools/fleet/install-on-kubernetes-using-helm.md) available to simplify the installation. Details for configuring {{fleet-server}} are included with the {{agent}} install steps.

{{eck}}
:   You can deploy {{fleet}}-managed {{agent}} in an {{ecloud}} Kubernetes environment that provides configuration and management capabilities for the full {{stack}}. For details, refer to [Run {{fleet}}-managed {{agent}} on ECK](/deploy-manage/deploy/cloud-on-k8s/fleet-managed-elastic-agent.md).

Self-managed
:   For self-managed deployments, you must install and host {{fleet-server}} yourself. For details about this deployment model and set up instructions, refer to [Deploy on-premises and self-managed](/reference/ingestion-tools/fleet/add-fleet-server-on-prem.md).









