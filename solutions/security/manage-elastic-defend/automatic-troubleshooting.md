---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/identify-third-party-av-products.html
applies_to:
  stack: ga 9.2, preview 9.0
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Automatic troubleshooting

Automatic troubleshooting helps you identify and resolve issues that could prevent {{elastic-defend}} from working as intended. It provides actionable insights into the following common problem areas:

* {applies_to}`stack: ga 9.2` {applies_to}`serverless: ga` **Policy responses**: Detect warnings or failures in {{elastic-defend}}’s integration policies.
* **Third-party antivirus (AV) software**: Identify installed third-party antivirus (AV) products that may conflict with {{elastic-defend}}.

This helps you resolve configuration errors, address incompatibilities, and ensure that your hosts remain protected.

::::{admonition} Requirements
To use this feature, you need:

* In serverless, a project with the Security Analytics Complete [feature tier](https://www.elastic.co/pricing/serverless-security).
* The **Automatic Troubleshooting: Read** or **Automatic Troubleshooting: All** security [sub-feature privilege](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md).
   :::{note}
   In {{stack}} 9.0.0, this privilege is called **Endpoint Insights**.
   :::
* A working [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md) for AI Assistant.
::::

## Troubleshoot policy issues
```yaml {applies_to}
stack: ga 9.2
serverless: ga
```

{{elastic-defend}}'s integration policy statuses indicate whether protections are applied successfully to your hosts. Warnings or failures in these policies can weaken your security posture. Automatic troubleshooting helps you detect any issues and suggests remediation steps.

::::{admonition} Requirements
To use this functionality, you need to enable [AI Assistant Knowledge Base](/solutions/security/ai/ai-assistant-knowledge-base.md).
::::

### Scan your hosts for policy issues 

1. Find **Endpoints** in the navigation menu or use the global search field.  
2. Click on an endpoint to open its details flyout.  
3. Under **Automatic Troubleshooting**, select an LLM connector, or [add](/explore-analyze/ai-features/llm-guides/llm-connectors.md) a new one.
4. If you don't already have AI Assistant Knowledge Base enabled, click **Setup Knowledge Base**. 
5. Once Knowledge Base is enabled, click **Scan**. After a brief processing period, any detected warnings or failures in policy responses will appear under **Insights**.  

### Resolve policy issues 

After a scan has completed, automatic troubleshooting suggests recommended next steps for each policy issue. These may include adjusting specific {{elastic-defend}} policy settings or reviewing conflicting host configurations. Where available, click **Learn more** to the right of a result to open Elastic documentation, which provides more context and guidance for resolving the issue.

## Identify antivirus software on your hosts [identify-third-party-av-products]

Third-party antivirus software installed on your hosts can interfere with {{elastic-defend}}. To mitigate issues with running third-party AV alongside {{elastic-defend}}, you first have to identify which AV is present.

After you’ve installed {{elastic-defend}} on one or more hosts, you can use automatic troubleshooting to check whether your endpoints have third-party AV software installed. Using the same kinds of large language model (LLM) connectors as Elastic AI Assistant, automatic troubleshooting can analyze file event logs from your hosts to determine whether antivirus software is present. From there, you can address any incompatibilities to make sure your endpoints are protected.

### Scan your hosts for AV software [_scan_your_hosts_for_av_software]

1. Find **Endpoints** in the navigation menu or use the global search field.
2. Click on an endpoint to open its details flyout.
3. Under **Automatic Troubleshooting**, select an LLM connector, or [add](/explore-analyze/ai-features/llm-guides/llm-connectors.md) a new one.
4. Click **Scan**. After a brief processing period, any detected AV products will appear under **Insights**.

### Resolve incompatibilities [_resolve_incompatibilities]

After a scan has completed, you can click the **Create trusted app** button to the right of a result to quickly add the associated AV program to {{elastic-defend}}'s trusted applications list. If the button is not clickable, you don’t have the [required privilege](trusted-applications.md).

::::{important}
If you plan to use {{elastic-defend}} alongside third-party AV software, we recommend you that you both [allowlist {{elastic-endpoint}} in your AV](allowlist-elastic-endpoint-in-third-party-antivirus-apps.md) and [make the AV a trusted application](trusted-applications.md).
::::
