---
navigation_title: FedRAMP authorized Cloud offerings
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Elastic FedRAMP authorized Cloud offerings

U.S. government agencies and partners can take advantage of the Elastic FedRAMP authorized Cloud offerings to host sensitive data in a secure environment that meets their regulatory and compliance requirements. These deployments are hosted on AWS GovCloud (US).

Learn about the Elastic FedRAMP offerings:

 - [Comparison of available features](#ec-fedramp-comparison)
 - [Get started with FedRAMP](#ec-fedramp-get-started)
 - [FedRAMP FAQ](#ec-fedramp-faq)

## Comparison of available features [ec-fedramp-comparison]

This table provides a comparison of features and capabilities included in {{ech}} and all FedRAMP authorized Cloud offerings.

| Feature | {{ech}} | {{fedramp-mod}} | {{fedramp-high}} | {{fedramp-il5}} |
|--------------|-----------|--------|-----------|
| Trial period | 14 days | 30 days | none | none |
| Marketplace offering | AWS/GCP/Azure | AWS | AWS  | AWS |
| Cloud service provider | AWS/GCP/Azure | 30 days | AWS | AWS |
| [Required subscription level](https://www.elastic.co/pricing) | Standard, Gold, Platinum, Enterprise | Platinum, Enterprise | Enterprise | Enterprise |
| [Available regions](cloud://reference/cloud-hosted/regions.md) | 50+ regions | `us-gov-east-1` | `us-gov-east-1`  | `us-gov-east-1` |
| [Billing model](/deploy-manage/cloud-organization/billing.md) | Consumption-based | Currently offered as annual and prepaid consumption models | Consumption-based | Consumption-based |
| Allowed users | All | All | U.S. federal, state, and local agencies; tribal groups | U.S. Department of Defence |
| [Account creation](/deploy-manage/deploy/elastic-cloud/create-an-organization.md) | Self serve | Self serve | By request | By request |
| IPv6 support at the edge | No | Yes | Yes | Yes |
| [Bring Your Own Key (BYOK)](/deploy-manage/security/encrypt-deployment-with-customer-managed-encryption-key.md) | Yes | No | No | No |
| Status page | Dedicated; publicly available | Dedicated; publicly available | Dedicated; private | Dedicated; not publicly available |
| Uptime SLA | 99.95% | 99.95% | Minimum 99.95% | Minimum 99.95% |
| [Support policy](https://www.elastic.co/support/welcome) | Global coverage | Global coverage | U.S. persons on U.S. soil | U.S. persons on U.S. soil |
| [{{kib}} connectors](kibana://reference/connectors-kibana.md) | All connector types | TBD | TBD | TBD |
| [Cross-cluster search](/explore-analyze/cross-cluster-search.md) and [cross-cluster replication](/deploy-manage/tools/cross-cluster-replication.md) | Yes | Yes | Yes | TBD |
| [Private connectivity](/deploy-manage/security/private-connectivity.md) | Yes | Yes | No | No |
| [AutoOps](/deploy-manage/monitor/autoops.md) | Yes | No | No | No |
| [Synthetic monitoring](/solutions/observability/synthetics/index.md) | Yes | No | No | No |
| [Elastic Inference Service](/explore-analyze/elastic-inference/eis.md) | Yes | No | No | No |
| [Managed OTLP Endpoint (mOTLP)](opentelemetry://reference/motlp.md) | Yes | No | No | No |
| [Custom bundles and plugins](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md) | Yes | Yes | No | No |
| Salesforce support instance | Salesforce commercial | Salesforce commercial | Salesforce high | Salesforce high |
| [Watcher](/explore-analyze/alerts-cases/watcher.md) | Yes | Yes | Internal only | Internal only |
| [Elastic AI Assistant for Observability and Search](/solutions/observability/observability-ai-assistant.md), [Elastic AI Assistant for Security](/solutions/security/ai/ai-assistant.md) | Yes | Elastic Managed LLM not available | Elastic Managed LLM not available | Elastic Managed LLM not available |
| [Attack Discovery](/solutions/security/ai/attack-discovery.md) | Yes | Yes | TBD | TBD |
| [Universal profiling](/solutions/observability/infra-and-hosts/universal-profiling.md) | Yes | No | No | TBD |

## Get started with FedRAMP [ec-fedramp-get-started]

{{fedramp-mod}} deployments are available for self-serve setup. Refer to the [Elastic FedRAMP authorized cloud offerings](https://www.elastic.co/industries/public-sector/fedramp) page to get started with a free trial. 

To get started on {{fedramp-high}} and {{fedramp-il5}}, [contact our support team](/troubleshoot/index.md#contact-us).

## FedRAMP FAQ [ec-fedramp-faq]

Find answers here to some common questions about using the FedRAMP authorized Cloud offerings.

* [Who can use FedRAMP?](#who-can-use-fedramp)
* [Where is FedRAMP hosted?](#where-is-fedramp-hosted)

$$$who-can-use-fedramp$$$**Who can use FedRAMP?**
:   The FedRAMP authorized Cloud offerings are intended for users who require their {{ecloud}} services to meet special security and compliance requirements:

    - {{fedramp-mod}} is available to all users having a Platinum or Enterprise license.
    - {{fedramp-high}} is available to United States federal, state, and local agencies as well as tribal groups.
    - {{fedramp-il5}} is available to the United States Department of Defense (DoD).

$$$where-is-fedramp-hosted$$$**Where is FedRAMP hosted?**

    {{fedramp-mod}}, {{fedramp-high}}, and {{fedramp-il5}} {{ecloud}} deployments are hosted on [AWS GovCloud (US)](https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/whatis.html) in the `us-gov-east-1` region.

