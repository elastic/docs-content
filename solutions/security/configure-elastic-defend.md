---
description: Install and configure Elastic Defend to protect endpoints against malware, ransomware, and behavioral threats. 
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/endpoint-protection-intro.html
  - https://www.elastic.co/guide/en/serverless/current/security-endpoint-protection-intro.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Configure endpoint protection with {{elastic-defend}} [endpoint-protection-intro]

{{elastic-defend}} is Elastic's endpoint protection integration. It prevents and detects malware, ransomware, memory threats, and malicious behavior on Windows, macOS, and Linux hosts. When a threat is detected, {{elastic-defend}} can generate an alert or block the activity outright, depending on your protection settings.

{{elastic-defend}} runs as part of [{{agent}}](/reference/fleet/index.md), which you deploy to each host you want to protect. Once installed, {{agent}} communicates with {{fleet}} for centralized policy management and sends security data to {{elastic-sec}}, where you can investigate alerts, manage exceptions, and respond to threats.

## How {{elastic-defend}}, {{agent}}, and {{elastic-endpoint}} work together

{{elastic-defend}} relies on three components that each play a distinct role in endpoint protection:

- **{{elastic-defend}}** is the integration that defines your protection policy — which threat protections are active, which events to collect, and which exceptions to apply. You add it to an {{agent}} policy and configure it through the {{elastic-sec}} UI or API.
- **{{agent}}** is the unified agent you install on each host. It manages integrations (including {{elastic-defend}}), handles enrollment and communication with {{fleet}}, and ships collected data to {{es}}.
- **{{elastic-endpoint}}** is the component that {{agent}} installs on the host when the {{elastic-defend}} integration is added. It performs the actual threat monitoring, prevention, and response actions at the operating system level.


In practice, you add the {{elastic-defend}} integration from the **Integrations** page, assign it to an {{agent}} policy, and deploy {{agent}} to your hosts. {{agent}} installs {{elastic-endpoint}}, which immediately begins monitoring the host according to your policy settings.

## Data that {{elastic-defend}} collects [elastic-defend-data]

{{elastic-defend}} collects events from each host it protects, such as process, network, and file activity. The preset you select when you install it sets which event categories it collects, and you can change them later in the integration policy. For the categories available on each operating system, refer to [Event collection](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#event-collection).

To bring in data from other sources, refer to [Ingest data to {{elastic-sec}}](/solutions/security/get-started/ingest-data-to-elastic-security.md).

## Where to start

| Your goal | Start here |
|---|---|
| Deploy {{elastic-defend}} for the first time | [Requirements](/solutions/security/configure-elastic-defend/elastic-defend-requirements.md) → [Install {{elastic-defend}}](/solutions/security/configure-elastic-defend/install-elastic-defend.md) |
| Deploy to macOS hosts without user prompts | [Deploy on macOS with MDM](/solutions/security/configure-elastic-defend/deploy-on-macos-with-mdm.md) |
| Set up endpoints in restricted networks | [Configure offline endpoints and air-gapped environments](/solutions/security/configure-elastic-defend/configure-offline-endpoints-air-gapped-environments.md) |
| {applies_to}`stack: ga 9.5+` {applies_to}`serverless: unavailable` Store endpoint data in a different cluster from the one that manages your {{agents}} | [Use {{elastic-defend}} with a remote {{es}} output](/solutions/security/configure-elastic-defend/use-elastic-defend-with-remote-output-and-ccs.md) |
| Tune protection, manage privileges, or remove agents after deployment | [Manage {{elastic-defend}}](/solutions/security/manage-elastic-defend.md) |

## Next steps

After installing and configuring {{elastic-defend}}, you can:

- [Manage endpoints, policies, and exceptions](/solutions/security/manage-elastic-defend.md) to tune protection for your environment.
- Read [Optimize {{elastic-defend}}](/solutions/security/manage-elastic-defend/optimize-elastic-defend.md) to understand different {{elastic-endpoint}} configuration settings.
- [Set up endpoint response actions](/solutions/security/endpoint-response-actions.md) to isolate hosts, run commands, or take other actions on protected endpoints.
- [Troubleshoot {{elastic-defend}}](/troubleshoot/security/elastic-defend.md) if you run into installation, connectivity, or policy issues.
