---
applies_to:
  deployment:
    self:
    ece:
    eck:
navigation_title: Cloud Connect
---

# Cloud Connect

Cloud Connect enables you to use {{ecloud}} services in your [ECE](/deploy-manage/deploy/cloud-enterprise.md), [ECK](/deploy-manage/deploy/cloud-on-k8s.md), or [self-managed](/deploy-manage/deploy/self-managed.md) cluster without having to install and maintain their infrastructure yourself. In this way, you can get faster access to new features without adding to your operational overhead.

AutoOps is the first service available for use with Cloud Connect. More services are coming soon.

## AutoOps

[AutoOps](/deploy-manage/monitor/autoops.md) is a monitoring tool that helps you manage your cluster with real-time issue detection, performance recommendations, and resolution paths. By analyzing hundreds of {{es}} metrics, your configuration, and your usage patterns, AutoOps recommends operational and monitoring insights that deliver real savings in administration time and hardware cost. 

Learn how to set up and use [](/deploy-manage/monitor/autoops/cc-autoops-as-cloud-connected.md). 

## Elastic {{infer-cap}} Service (EIS)

[Elastic {{infer-cap}} Service](/explore-analyze/elastic-inference/eis.md) enables you to add AI-powered search and assistance to your {{es}} deployment without running models yourself.
You can use EIS to enable features such as:

- [Semantic search](/solutions/search/semantic-search.md)
- [AI Assistants](/explore-analyze/ai-features/ai-chat-experiences/ai-assistant.md)
- [Agent Builder](/explore-analyze/ai-features/elastic-agent-builder.md)
- [Attack Discovery](/solutions/security/ai/attack-discovery.md)

For a full list of EIS-powered features, refer to [AI features powered by EIS](/explore-analyze/elastic-inference/eis.md#ai-features-powered-by-eis).

Learn how to set up and use [](/explore-analyze/elastic-inference/connect-self-managed-cluster-to-eis.md).

## FAQ

Find answers to your questions about Cloud Connect.

* [Does Cloud Connect require additional payment?](#cc-additional-payment)
* [Can I use Cloud Connect to connect my Elastic Cloud Hosted clusters to AutoOps?](#cc-ech)
* [Are more services going to be available with Cloud Connect?](#cc-more-services)

$$$cc-additional-payment$$$ **Does Cloud Connect require additional payment?** 
:   Each cloud connected service has its own licensing and payment requirements. 
    :::{include} /deploy-manage/_snippets/autoops-cc-payment-faq.md
::: 

$$$cc-ech$$$ **Can I use Cloud Connect to connect my Elastic Cloud Hosted clusters to AutoOps?**
:   :::{include} /deploy-manage/_snippets/autoops-cc-ech-faq.md
:::

$$$cc-more-services$$$ **Are more services going to be available with Cloud Connect?**
:   Yes. AutoOps is the first of many cloud connected services to come. The next planned service is the Elastic Inference Service (EIS), which will provide GPU-powered inference for use cases like semantic search and text embeddings.

