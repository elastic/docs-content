---
navigation_title: FedRAMP authorized Cloud offerings
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Elastic FedRAMP authorized Cloud offerings

Elastic users can take advantage of the FedRAMP authorized Cloud offerings to host sensitive data in a secure environment that meets their regulatory and compliance requirements.

{{fedramp-mod}} deployments are available to all users who have a Platinum or Enterprise subscription level. {{fedramp-high}} deployments are available to United States federal, state, and local agencies as well as tribal groups that have an Enterprise subscription level.

All FedRAMP deployments are hosted on AWS GovCloud (U.S.).

Learn about the Elastic FedRAMP offerings:

 - [Comparison of available features](#ec-fedramp-comparison)
 - [Get started with FedRAMP](#ec-fedramp-get-started)
 - [Limitations](#ec-fedramp-limitations)
 - [FedRAMP FAQ](#ec-fedramp-faq)

## Comparison of available features [ec-fedramp-comparison]

This table provides a comparison of features and capabilities included in {{ech}} and all FedRAMP authorized Cloud offerings.

| Feature | {{ech}} | {{fedramp-mod}} | {{fedramp-high}} |
|--------------|-----------|--------|-----------|
| Trial period | 14 days | 30 days | none |
| Marketplace offering | AWS/GCP/Azure | AWS GovCloud | AWS GovCloud  |
| Cloud service provider | AWS/GCP/Azure | AWS GovCloud | AWS GovCloud |
| [Required subscription level](https://www.elastic.co/pricing) | Standard, Gold, Platinum, Enterprise | Platinum, Enterprise | Enterprise |
| [Available regions](cloud://reference/cloud-hosted/regions.md) | 50+ regions | `us-gov-east-1` | `us-gov-east-1`  |
| Allowed users | All | All | U.S. federal, state, and local agencies; tribal groups |
| IPv6 support at the edge | No | Yes | Yes |
| [Bring Your Own Key (BYOK)](/deploy-manage/security/encrypt-deployment-with-customer-managed-encryption-key.md) | Yes | No | No |
| [Support policy](https://www.elastic.co/support/welcome) | Global coverage | Global coverage or optional U.S. persons on U.S. soil support available | U.S. persons on U.S. soil support |
| [{{kib}} connectors](kibana://reference/connectors-kibana.md) | All connector types | Email, Index, Webhook, Gen-AI, Bedrock, Gemini, Inference, Slack, Slack-API, PagerDuty | Email, Index, Webhook, Gen-AI, Bedrock, Gemini, Inference, Slack, Slack-API, PagerDuty |
| [Cross-cluster search](/explore-analyze/cross-cluster-search.md) and [cross-cluster replication](/deploy-manage/tools/cross-cluster-replication.md) | Yes | Yes | Yes |
| [Private connectivity](/deploy-manage/security/private-connectivity.md) | Yes | Yes | No |
| [AutoOps](/deploy-manage/monitor/autoops.md) | Yes | No | No |
| [Synthetic monitoring](/solutions/observability/synthetics/index.md) | Yes | No | No |
| [Elastic Inference Service](/explore-analyze/elastic-inference/eis.md) | Yes | No | No |
| [Managed OTLP Endpoint (mOTLP)](opentelemetry://reference/motlp.md) | Yes | No | No |
| [Custom bundles and plugins](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md) | Yes | Yes | No |
| [Elastic AI Assistant for Observability and Search](/solutions/observability/observability-ai-assistant.md), [Elastic AI Assistant for Security](/solutions/security/ai/ai-assistant.md) | Yes | Elastic Managed LLM not available | Elastic Managed LLM not available |
| [Attack Discovery](/solutions/security/ai/attack-discovery.md) | Yes | Yes | TBD |
| [Universal profiling](/solutions/observability/infra-and-hosts/universal-profiling.md) | Yes | No | No |

## Get started with FedRAMP [ec-fedramp-get-started]

{{fedramp-mod}} deployments are available for self-serve setup. Refer to the [Elastic FedRAMP authorized cloud offerings](https://www.elastic.co/industries/public-sector/fedramp) page to get started with a free trial. 

To get started on {{fedramp-high}}, [contact our support team](/troubleshoot/index.md#contact-us).

## Limitations [ec-fedramp-limitations]

There are some limitations to note for using the FedRAMP authorized Cloud offerings.

### TLS

**Applies to:** {{fedramp-mod}}, {{fedramp-high}}

% Copied from https://www.elastic.co/docs/deploy-manage/security/fips-ingest#ingest-limitations-tls
% I'll single-source this if the finalized content is identical to what we have in the security section.

Only FIPS 140-2 compliant TLS protocols, ciphers, and curve types are allowed to be used as listed below.
* The supported TLS versions are `TLS v1.2` and `TLS v1.3`.
* The supported cipher suites are:
  * `TLS v1.2`: `ECDHE-RSA-AES-128-GCM-SHA256`, `ECDHE-RSA-AES-256-GCM-SHA384`, `ECDHE-ECDSA-AES-128-GCM-SHA256`, `ECDHE-ECDSA-AES-256-GCM-SHA384`
  * `TLS v1.3`: `TLS-AES-128-GCM-SHA256`, `TLS-AES-256-GCM-SHA384`
* The supported curve types are `P-256`, `P-384` and `P-521`.

Support for encrypted private keys is not available, as the cryptographic modules used for decrypting password protected keys are not FIPS validated. If an output or any other component with an SSL key that is password protected is configured, the components will fail to load the key. When running in FIPS mode, you must provide non-encrypted keys.
Be sure to enforce security in your FIPS environments through other means, such as strict file permissions and access controls on the key file itself, for example.

### {{elastic-defend}}

**Applies to:** {{fedramp-mod}}, {{fedramp-high}}

The {{elastic-defend}} integration that runs on hosts being protected has various features that require data to be sent directly to Elastic-managed cloud services. The data sent is not sourced from within the secure enclave on the host. However, you may still want to adjust the configuration for your {{fedramp-mod}} and {{fedramp-high}} environments. You can use the [advanced setting](/reference/security/defend-advanced-settings.md) `[linux,mac,windows].advanced.allow_cloud_features` to activate or deactivate each {{elastic-defend}} feature individually.

### Custom plugins

**Applies to:** {{fedramp-high}}

Custom plugins are currently not supported in {{fedramp-high}} deployments. 

## FedRAMP FAQ [ec-fedramp-faq]

Find answers here to some common questions about using the FedRAMP authorized Cloud offerings.

* [Who can use FedRAMP?](#who-can-use-fedramp)
* [Where is FedRAMP hosted?](#where-is-fedramp-hosted)

$$$who-can-use-fedramp$$$**Who can use FedRAMP?**
:   The FedRAMP authorized Cloud offerings are intended for users who require their {{ecloud}} services to meet special security and compliance requirements:

    - {{fedramp-mod}} is available to all users having a Platinum or Enterprise subscription level.
    - {{fedramp-high}} is available to United States federal, state, and local agencies as well as tribal groups. An Enterprise subscription level is required.
    
$$$where-is-fedramp-hosted$$$**Where is FedRAMP hosted?**

:    {{fedramp-mod}} and {{fedramp-high}} {{ecloud}} deployments are hosted on [AWS GovCloud (US)](https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/whatis.html) in the `us-gov-east-1` region.
