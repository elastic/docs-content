---
navigation_title: Install prebuilt rules
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/prebuilt-rules-management.html
  - https://www.elastic.co/guide/en/serverless/current/security-prebuilt-rules-management.html
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Install and enable Elastic Security prebuilt detection rules to quickly gain threat detection coverage across your environment.
---

# Install Elastic prebuilt rules [install-prebuilt-rules]

Elastic provides hundreds of prebuilt detection rules that cover common attack techniques across multiple platforms. This page explains how to install and enable prebuilt rules so they start generating alerts.

## What you can do by subscription [prebuilt-subscription-capabilities]

Your subscription determines which prebuilt rule features are available:

| Capability | Basic–Platinum | Enterprise |
|---|:---:|:---:|
| Install and enable rules | ✓ | ✓ |
| View prerequisites and tags | ✓ | ✓ |
| Add exceptions | ✓ | ✓ |
| Configure rule actions | ✓ | ✓ |
| Update rules (accept Elastic version) | ✓ | ✓ |
| Duplicate and customize | ✓ | ✓ |
| Edit prebuilt rules directly | — | ✓ |
| Review field-level update changes | — | ✓ |
| Resolve update conflicts | — | ✓ |
| Revert to Elastic version | — | ✓ (9.1+) |

:::{note}
For {{serverless-short}}, Security Analytics Essentials corresponds to Basic–Platinum, and Security Analytics Complete corresponds to Enterprise.
:::

## Install and enable rules [load-prebuilt-rules]

Most prebuilt rules don't start running by default. Use **Install and enable** to start rules immediately, or install first and enable later.

1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to the Rules table.

    The badge next to **Add Elastic rules** shows the number of prebuilt rules available for installation.

    :::{image} /solutions/images/security-prebuilt-rules-add-badge.png
    :alt: The Add Elastic Rules page
    :screenshot:
    :::

2. Select **Add Elastic rules**.

    ::::{tip}
    To examine the details of a rule before you install it, select the rule name. This opens the rule details flyout.
    ::::

3. Do one of the following:

    * Install all available rules: Select **Install all** at the top of the page. (This doesn't enable the rules; you still need to do that manually.)
    * Install a single rule: In the rules table, either select **Install** to install a rule without enabling it, or select ![Vertical boxes button](/solutions/images/security-boxesVertical.svg "") → **Install and enable** to start running the rule once it's installed.
    * Install multiple rules: Select the rules, and then at the top of the page either select **Install *x* selected rule(s)** to install without enabling the rules, or select ![Vertical boxes button](/solutions/images/serverless-boxesVertical.svg "") → **Install and enable** to install and start running the rules.

    ::::{tip}
    Use the search bar and **Tags** filter to find the rules you want to install. For example, filter by `OS: Windows` if your environment only includes Windows endpoints. For more on tag categories, refer to [Prebuilt rule tags](/solutions/security/detect-and-alert/prebuilt-rules.md#prebuilt-rule-tags).
    ::::

    :::{image} /solutions/images/security-prebuilt-rules-add.png
    :alt: The Add Elastic Rules page
    :screenshot:
    :::

4. For any rules you haven't already enabled, go back to the {{rules-ui}} page, search or filter for the rules you want to run, and do either of the following:

    * Enable a single rule: Turn on the rule's **Enabled** switch.
    * Enable multiple rules: Select the rules, then select **Bulk actions** → **Enable**.

Once you enable a rule, it starts running on its configured schedule. To confirm that it's running successfully, check its **Last response** status in the rules table, or open the rule's details page and check the [**Execution results**](/solutions/security/detect-and-alert/monitor-rule-executions.md#rule-execution-logs) tab.

:::{admonition} Endpoint protection rules
Some prebuilt rules serve special purposes: [Endpoint protection rules](/solutions/security/manage-elastic-defend/endpoint-protection-rules.md) generate alerts from {{elastic-defend}}'s threat monitoring and prevention, while the [External Alerts](detection-rules://rules/promotions/external_alerts.md) rule creates alerts for incoming third-party system alerts (for example, Suricata alerts).
:::

## Next steps

After installing prebuilt rules:

* **Keep rules current**: Elastic regularly updates prebuilt rules to detect new threats. Refer to [Update Elastic prebuilt rules](/solutions/security/detect-and-alert/update-prebuilt-rules.md) to learn how to apply updates.
* **Air-gapped environments**: If your deployment doesn't have internet access, refer to [Prebuilt rules in air-gapped environments](/solutions/security/detect-and-alert/prebuilt-rules-airgapped.md).
* **Customize rules**: Adapt prebuilt rules to your environment by editing them directly (Enterprise) or duplicating and modifying copies. Refer to [Customize Elastic prebuilt rules](/solutions/security/detect-and-alert/customize-prebuilt-rules.md).
* **Build custom rules**: Create detection logic tailored to your infrastructure. Refer to [Author rules](/solutions/security/detect-and-alert/author-rules.md).
