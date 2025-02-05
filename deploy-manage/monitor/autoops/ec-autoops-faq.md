---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoops-faq.html
applies:
  hosted: all
---

# AutoOps FAQ [ec-autoops-faq]

This frequently-asked-questions list answers some of your more common questions about AutoOps.

$$$faq-what-is-autoops$$$What is AutoOps? What does it do?
:   AutoOps for Elasticsearch significantly simplifies cluster management with performance recommendations, resource utilization and cost insights, real-time issue detection and resolution paths. By analyzing hundreds of Elasticsearch metrics, your configuration, and usage patterns, AutoOps recommends operational and monitoring insights that deliver savings in administration time and hardware costs.

$$$faq-autoops-availability$$$When will AutoOps be available for Self-hosted and Serverless users?
:   AutoOps will be available for Self-hosted and Serverless customers with a different set of capabilities in the future.

$$$faq-autoops-monitoring$$$Does AutoOps monitor the entire Elastic Stack?
:   AutoOps is currently limited to {{es}} (not {{kib}}, Logstash and Beats).

$$$faq-autoops-supported-versions$$$What versions of Elasticsearch are supported for Elastic Cloud Hosted?
:   AutoOps is currently available for {{es}} versions 7.17 and above.

$$$faq-autoops-license$$$How is AutoOps currently licensed?
:   AutoOps current feature set is available to Elastic Cloud Hosted customers at all subscription tiers. For more information please refer to the [subscription page](https://www.elastic.co/subscriptions/cloud).

$$$faq-autoops-installation$$$How does AutoOps get installed and why may I not see AutoOps available on specific deployments?
:   AutoOps is automatically applied to {{es}} clusters on Elastic Cloud, rolling out in phases across CSPs and regions. Read more about AutoOps [roll out](ec-autoops-regions.md) status.

$$$faq-autoops-issue-resolution$$$Can AutoOps currently automatically resolve issues?
:   AutoOps only analyzes metrics, and is a “read-only” solution.

$$$faq-autoops-data-retention$$$How long does Elastic retain AutoOps data?
:   Currently, AutoOps has a four-day retention period for all Hosted customers.

$$$faq-autoops-metrics-storage$$$Where are AutoOps metrics stored, and does AutoOps affect customer ECU usage?
:   AutoOps metrics are stored internally within the Elastic infrastructure, not on customer deployments. Therefore, using AutoOps does not consume customer ECU).

$$$faq-autoops-vs-stack-monitoring$$$Does AutoOps replace Stack Monitoring now?
:   As of now, AutoOps provides insights on {{es}} (not {{kib}}, Logstash and Beats) and analyzes metrics, but not logs. Stack Monitoring covers the entire stack and with it you can analyze logs.

