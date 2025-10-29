---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoops-faq.html
applies_to:
  serverless:
  deployment:
    ess: all
    self:
    ece:
    eck:
products:
  - id: cloud-hosted
  - id: cloud-kubernetes
  - id: cloud-enterprise
navigation_title: FAQ
---

# AutoOps FAQ [ec-autoops-faq]

Here are answers to some common questions about AutoOps.

$$$faq-what-is-autoops$$$What does AutoOps do?
:   AutoOps for {{es}} significantly simplifies cluster management with performance recommendations, resource utilization and cost insights, real-time issue detection and resolution paths. By analyzing hundreds of {{es}} metrics, your configuration, and usage patterns, AutoOps recommends operational and monitoring insights that deliver savings in administration time and hardware costs.

$$$faq-autoops-deployment-types$$$Is AutoOps available in all types of deployments?
:   In the [regions](ec-autoops-regions.md) where it has been rolled out, AutoOps is automatically available in [{{ech}} deployments](/deploy-manage/monitor/autoops/ec-autoops-how-to-access.md) and [{{serverless-full}} projects](/deploy-manage/monitor/autoops/autoops-for-serverless.md), and can be set up for [ECE, ECK, and self-managed clusters](/deploy-manage/monitor/autoops/cc-autoops-as-cloud-connected.md).

$$$faq-autoops-regions$$$Why can't I see AutoOps in some deployments?
:   AutoOps is rolling out in phases across CSPs and [regions](ec-autoops-regions.md), so you may not see it if your deployment is in a region where AutoOps is not available yet. 

$$$faq-autoops-monitoring$$$Does AutoOps monitor the entire {{stack}}?
:   AutoOps is currently limited to {{es}} (not {{kib}}, Logstash, and Beats).

$$$faq-autoops-supported-versions$$$What versions of {{es}} are supported for {{ech}}?
:   AutoOps supports {{es}} versions according to the [supported {{stack}} versions](https://www.elastic.co/support/eol).

$$$faq-autoops-license$$$How is AutoOps currently licensed?
:   Using AutoOps for {{ech}} deployments is available at all [subscription tiers](https://www.elastic.co/subscriptions/cloud).
    :::{include} /deploy-manage/_snippets/autoops-cc-payment-faq.md
    ::: 

$$$faq-autoops-issue-resolution$$$Can AutoOps currently automatically resolve issues?
:   AutoOps only analyzes metrics, and is a read-only solution.

$$$faq-autoops-data-retention$$$How long does Elastic retain AutoOps data?
:   Currently, AutoOps has a 10 day retention period for all {{ech}} customers.

$$$faq-autoops-metrics-storage$$$Where are AutoOps metrics stored, and does AutoOps affect customer ECU usage?
:   AutoOps metrics are stored internally within the Elastic infrastructure, not on customer deployments. So using AutoOps does not consume customer ECU.

$$$faq-autoops-vs-stack-monitoring$$$Has AutoOps replaced Stack Monitoring?
:   Currently, AutoOps has many of the same features as Stack Monitoring as well as several new ones. However, it only provides insights on {{es}} and analyzes metrics, but not logs. Read more in [](/deploy-manage/monitor/autoops-vs-stack-monitoring.md).

