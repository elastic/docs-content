---
navigation_title: Upgrade from EASE to Elastic Security
applies_to:
  serverless:
    security: preview
---

# Upgrade from Elastic AI SOC Engine to {{elastic-sec}} to access additional features

This page describes how to upgrade an {{sec-serverless}} project from the Elastic AI SOC Engine (EASE) feature tier to the Security Analytics Essentials or Security Analytics Complete feature tiers.

## Why upgrade?
EASE provides a small subset of the features available on other {{sec-serverless}} feature tiers. It's designed to add a layer of AI features onto your existing SOC software stack. In contrast, {{elastic-sec}} provides a full set of SOC capabilities including many additional ways to ingest data, prebuilt and customizable detection rules, response actions, integrated threat intelligence, runtime protection, data visualization, and more. 

For a full breakdown of the features available in the Security Analytics Essentials and Security Analytics Complete feature tiers, refer to [Elastic Security Serverless pricing](https://www.elastic.co/pricing/serverless-security).

:::{important}
The AI features present in EASE are not available on the Essentials tier. 
:::


## How to upgrade from EASE to other feature tiers

1. Log in to the [{{ecloud}} console](https://console.qa.cld.elstc.co/).
2. Find the project you wish to upgrade on the list of serverless projects, and click **Manage**. 

   :::{image} /solutions/images/security-ease-cloud-console-manage-project.png
   :alt: The cloud console showing an EASE project with the MANAGE button highlighted
   :width: 550px
   :::

3. On the project management page, next to **Project features**, click **Edit**.

   :::{image} /solutions/images/security-ease-cloud-console-edit-project-features.png
   :alt: The manage project page for an EASE project with the EDIT button highlighted
   :width: 550px
   :::

4. Select either the **Security Analytics Essentials** or **Security Analytics Complete** options, and select any desired add-on options. Click **Save**. 

You can return to this page at any point to switch between Essentials and Complete and change your add-on selections.
However, once you upgrade from EASE to another product tier, you cannot revert or downgrade the project back to EASE. You can always create another new project of any tier.

## What to do after upgrading an EASE project

When you upgrade an EASE project, you gain access to all the {{elastic-sec}} capabilities included in your selected [feature tier](https://www.elastic.co/pricing/serverless-security). To learn more about what {{elastic-sec}} can do and how to use it, refer to [Get started with {{elastic-sec}}](/solutions/security/get-started.md).