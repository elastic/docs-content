---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/identify-third-party-av-products.html
applies_to:
  stack: preview 9.0
  serverless:
    security: preview
products:
  - id: cloud-serverless
---

# Identify antivirus software on your hosts [identify-third-party-av-products]

::::{admonition} Technical preview
:class: important

This feature is in technical preview. It may change in the future, and you should exercise caution when using it in production environments. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of GA features.
::::


Third-party antivirus (AV) software installed on your hosts can interfere with {{elastic-defend}}. To mitigate issues with running third-party AV alongside {{elastic-defend}}, you first have to identify which AV is present.

After you’ve installed {{elastic-defend}} on one or more hosts, you can use *Automatic Troubleshooting* to check whether your endpoints have third-party AV software installed. Using the same kinds of large language model (LLM) connectors as Elastic AI Assistant, Automatic Troubleshooting can analyze file event logs from your hosts to determine whether antivirus software is present. From there, you can address any incompatibilities to make sure your endpoints are protected.

::::{admonition} Requirements
To use this feature, you need:

* In serverless, a project with the Security Analytics Complete [feature tier](https://www.elastic.co/pricing/serverless-security).
* The **Automatic Troubleshooting: Read** or **Automatic Troubleshooting: All** security [sub-feature privilege](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md).
   :::{note}
   In {{stack}} 9.0.0, this privilege is called **Endpoint Insights**.
   :::
* A working [LLM connector](../ai/set-up-connectors-for-large-language-models-llm.md) for AI Assistant.
::::


## Scan your hosts for AV software [_scan_your_hosts_for_av_software]

1. Find **Endpoints** in the navigation menu or use the global search field.
2. Click on an endpoint to open its details flyout.
3. Under **Automatic Troubleshooting**, select an LLM connector, or [add](../ai/set-up-connectors-for-large-language-models-llm.md) a new one.
4. Click **Scan**. After a brief processing period, any detected AV products will appear under **Insights**.


## Resolve incompatibilities [_resolve_incompatibilities]

After a scan has completed, you can click the **Create trusted app** button to the right of a result to quickly add the associated AV program to {{elastic-defend}}'s trusted applications list. If the button is not clickable, you don’t have the [required privilege](trusted-applications.md).

::::{important}
If you plan to use {{elastic-defend}} alongside third-party AV software, we recommend you that you both [allowlist {{elastic-endpoint}} in your AV](allowlist-elastic-endpoint-in-third-party-antivirus-apps.md) and [make the AV a trusted application](trusted-applications.md).
::::
