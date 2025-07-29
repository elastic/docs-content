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

Cloud Connect is included with your [self-managed Enterprise license](https://www.elastic.co/subscriptions) and works with self-managed free trials for the duration of the trial period.

AutoOps is the first service available for use with Cloud Connect. More services are coming soon.

### AutoOps

[AutoOps](/deploy-manage/monitor/autoops.md) is a monitoring tool that helps you manage your cluster with real-time issue detection, performance recommendations, and resolution paths. By analyzing hundreds of {{es}} metrics, your configuration, and usage patterns, AutoOps recommends operational and monitoring insights that deliver real savings in administration time and hardware cost. 

Learn how to set up and use [](/deploy-manage/monitor/autoops/cc-autoops-as-cloud-connected.md). 

## FAQs

Find answers to your questions about Cloud Connect.

:::{dropdown} Does using Cloud Connect require additional payment?

$$$cc-payment$$$

No. Cloud Connect is included with your [self-managed Enterprise license](https://www.elastic.co/subscriptions) and works with self-managed free trials for the duration of the trial period.

However, you may incur additional costs for specific functions within a cloud connected service. For example, when sending metrics data from your cluster in a CSP region to AutoOps in {{ecloud}}, shipping costs will be determined by your agreement with that CSP. 
:::

:::{dropdown} Does using Cloud Connect consume ECU?

$$$cc-ecu$$$

No. The currently available functionality does not consume ECU, but this may change when more features are introduced.
:::

:::{dropdown} Will my data be safe when using Cloud Connect?

$$$cc-data$$$

Yes. For AutoOps, {{agent}} only sends cluster metrics to {{ecloud}}, not the underlying data within your cluster. Learn more in [](/deploy-manage/monitor/autoops/cc-cloud-connect-autoops-faq.md). 
:::

:::{dropdown} Are more services going to be available with Cloud Connect?

$$$cc-more-services$$$

Yes. AutoOps is the first of many cloud connected services to come. The next planned service is the Elastic Inference Service (EIS), which will provide GPU-powered inference for use cases like semantic search and text embeddings.
:::

