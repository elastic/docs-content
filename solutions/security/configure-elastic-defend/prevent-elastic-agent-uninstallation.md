---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/agent-tamper-protection.html
  - https://www.elastic.co/guide/en/serverless/current/security-agent-tamper-protection.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Prevent {{agent}} uninstallation


For hosts enrolled in {{elastic-defend}}, you can prevent unauthorized attempts to uninstall {{agent}} and {{elastic-endpoint}} by enabling **Agent tamper protection** on the Agent policy. This offers an additional layer of security by preventing users from bypassing or disabling {{elastic-defend}}'s endpoint protections.

When enabled, {{agent}} and {{elastic-endpoint}} can only be uninstalled on the host by including an uninstall token in the uninstall CLI command. One unique uninstall token is generated per Agent policy, and you can retrieve uninstall tokens in an Agent policy’s settings or in the {{fleet}} UI.

::::{admonition} Requirements
* In {{stack}}, agent tamper protection requires a [Platinum or higher subscription](https://www.elastic.co/pricing).
* In {{serverless-short}}, agent tamper protection requires the Endpoint Protection Complete [project feature](/deploy-manage/deploy/elastic-cloud/project-settings.md).
* Hosts must be enrolled in the {{elastic-defend}} integration.
* {{agent}}s must be version 8.11.0 or later.
* This feature is supported for all operating systems.
::::


:::{image} /solutions/images/security-agent-tamper-protection.png
:alt: Agent tamper protection setting highlighted on Agent policy settings page
:screenshot:
:::


## Enable Agent tamper protection [enable-agent-tamper-protection]

You can enable Agent tamper protection by configuring the {{agent}} policy.

1. Find **{{fleet}}** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Agent policies**, then select the Agent policy you want to configure.
3. Select the **Settings** tab on the policy details page.
4. In the **Agent tamper protection** section, turn on the **Prevent agent tampering** setting.

    This makes the **Get uninstall command** link available, which you can follow to get the uninstall token and CLI command if you need to [uninstall an Agent](/solutions/security/configure-elastic-defend/uninstall-elastic-agent.md) on this policy.

    ::::{tip}
    You can also access an Agent policy’s uninstall tokens on the **Uninstall tokens** tab on the **{{fleet}}** page. Refer to [Access uninstall tokens](/solutions/security/configure-elastic-defend/prevent-elastic-agent-uninstallation.md#fleet-uninstall-tokens) for more information.
    ::::

5. Select **Save changes**.


## Access uninstall tokens [fleet-uninstall-tokens]

If you need the uninstall token to remove {{agent}} from an endpoint, you can find it in several ways:

* **On the Agent policy**: Go to the Agent policy’s **Settings** tab, then click the **Get uninstall command** link. The **Uninstall agent** flyout opens, containing the full uninstall command with the token.
* **On the {{fleet}} page**: Select **Uninstall tokens** for a list of the uninstall tokens generated for your Agent policies. You can:

    * Click the **Show token** icon in the **Token** column to reveal a specific token.
    * Click the **View uninstall command** icon in the **Actions** column to open the **Uninstall agent** flyout, containing the full uninstall command with the token.


::::{tip}
If you have many tamper-protected {{agent}} policies, you may want to [provide multiple uninstall tokens](/solutions/security/configure-elastic-defend/uninstall-elastic-agent.md#multiple-uninstall-tokens) in a single command.
::::


