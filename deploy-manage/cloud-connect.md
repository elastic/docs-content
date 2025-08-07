---
applies_to:
  deployment:
    self:
    ece:
    eck:
navigation_title: Cloud Connect
---

# Cloud Connect

Cloud Connect enables you to use {{ecloud}} services in your self-managed cluster without having to install and maintain their infrastructure yourself. In this way, you can get faster access to new features while significantly reducing your operational overhead.

AutoOps is the first service available for use with Cloud Connect. More services are coming soon.

### AutoOps

[AutoOps](/deploy-manage/monitor/autoops.md) is a monitoring tool that helps you manage your cluster with real-time issue detection, performance recommendations, and resolution paths. By analyzing hundreds of {{es}} metrics, your configuration, and usage patterns, AutoOps recommends operational and monitoring insights that deliver real savings in administration time and hardware cost. 

Learn how to set up and use [](/deploy-manage/monitor/autoops/cc-autoops-as-cloud-connected.md). 

## FAQs

Find answers to your questions about Cloud Connect.

:::{dropdown} Does using Cloud Connect require additional payment?

$$$cc-payment$$$

Each cloud connected service has its own licensing and payment requirements. 

:::{include} /deploy-manage/_snippets/autoops-cc-payment-faq.md
:::

:::

:::{dropdown} Will my data be safe when using Cloud Connect?

$$$cc-data$$$

Yes. For AutoOps, {{agent}} only sends cluster metrics to {{ecloud}}, not the underlying data within your cluster. Learn more in [](/deploy-manage/monitor/autoops/cc-cloud-connect-autoops-faq.md). 
:::

:::{dropdown} Are more services going to be available with Cloud Connect?

$$$cc-more-services$$$

Yes. AutoOps is the first of many cloud connected services to come. The next planned service is the Elastic Inference Service (EIS), which will provide GPU-powered inference for use cases like semantic search and text embeddings.
:::

