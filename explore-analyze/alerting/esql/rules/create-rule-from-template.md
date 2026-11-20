---
navigation_title: Create from a template
applies_to:
  stack: ga 9.6+
  serverless:
    observability: ga
products:
  - id: kibana
description: "Create a Kibana Universal Alerting rule from a template in the Rule library. Templates from installed integrations prefill the rule settings for review and editing before saving."
---

# Create a {{alerting-v2-system}} rule from a template [create-rule-from-template]

Rule templates are ready-made {{alerting-v2-system-short}} rules that {{fleet}} integrations provide. Instead of writing the {{esql}} detection logic yourself, you start from a rule that already has its query and settings in place, and then adjust it to your data. The **Rule library** lists the templates available in your deployment.

Templates in the **Rule library** create {{alerting-v2-system-short}} rules only. For templates that create {{alerting-v1-system}} rules, refer to [Create rules from integration alerting templates](/reference/fleet/alerting-rule-templates.md).

## Requirements [create-rule-from-template-requirements]

- The **Rules: All** privilege (under **Universal Alerting**). If **Create** is unavailable in the **Rule library**, your role doesn't include it. Refer to [Configure access](../manage/configure-access.md#alerting-quick-reference).
- An installed {{fleet}} integration that provides {{alerting-v2-system-short}} rule templates. Refer to [Where templates come from](#rule-library-sources).

## Open the Rule library [open-rule-library]

In the {{observability}} navigation menu, go to **Alerting** → **Rule Library**, or find **Rule Library** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

A **Universal** badge in the page header and a **Universal rules only** note, which you can dismiss, remind you that templates create {{alerting-v2-system-short}} rules.

## Where templates come from [rule-library-sources]

{{fleet}} integrations provide the templates. Installing or updating an integration that includes templates adds them to the **Rule library**.

If the **Rule library** shows **No rule templates**, none of your installed integrations provides templates that {{alerting-v2-system-short}} can use. To add some, install or update integrations. Refer to [Manage {{agent}} integrations](/reference/fleet/manage-integrations.md).

## Find a template [find-rule-template]

Each row shows a template's name, description, and tags. To narrow the list, search for text in a template's name or description, or filter by **Tags**. To change the order, sort by **Name** or **Tags**.

The **Rules** column shows how many rules were created from each template. Select a number greater than zero to open the **Rules** page in a new tab, filtered to those rules.

## Create a rule from a template [create-from-template]

1. In the **Rule library**, find the template you want and select **Create** in its row. The rule creation flyout opens with the template's settings filled in.
2. Review the settings and edit anything that doesn't fit your data. For what each setting does, refer to [Configure a rule](configure-a-rule.md).
3. Select **Create rule**.

{{kib}} creates the rule and shows a confirmation with a **View rule** action. The template's **Rules** count in the **Rule library** goes up by one. To edit, disable, or delete the rule later, refer to [View and manage rules](view-manage-rules.md).

## Related pages

- [Create a rule](create-a-rule.md) compares every way to create a rule.
- [Configure a rule](configure-a-rule.md) describes the settings that a template fills in.
- [View and manage rules](view-manage-rules.md) explains how to manage the rule after you create it.
- [Configure access](../manage/configure-access.md) lists the privileges for rules, alerts, and action policies.
