---
navigation_title: Customize prebuilt rules
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Customize Elastic Security prebuilt detection rules by editing directly (Enterprise), duplicating, adding exceptions, or reverting to the original Elastic version.
---

# Customize Elastic prebuilt rules [customize-prebuilt-rules]

Prebuilt rules provide a starting point for threat detection, but you might need to adapt them to your environment. This page explains how to customize prebuilt rules based on your subscription level.

## What you can customize by subscription [customize-subscription-capabilities]

Your subscription determines how you can customize prebuilt rules:

| Capability | Basic–Platinum | Enterprise |
|---|:---:|:---:|
| Add exceptions to rules | ✓ | ✓ |
| Configure rule actions | ✓ | ✓ |
| Duplicate and modify copies | ✓ | ✓ |
| Edit prebuilt rules directly | — | ✓ |
| Revert to Elastic version | — | ✓ |

:::{note}
For {{serverless-short}}, Security Analytics Essentials corresponds to Basic–Platinum, and Security Analytics Complete corresponds to Enterprise.
:::


## Edit prebuilt rules directly [edit-prebuilt-rules]

With an Enterprise subscription on {{stack}} or a Security Analytics Complete project on {{serverless-short}}, you can edit most prebuilt rule settings directly (except **Author** and **License**).

1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the Rules table, find the prebuilt rule you want to edit.
3. Do one of the following:
    * Select the **All actions** menu {icon}`boxes_horizontal` on a rule, then select **Edit rule settings**.
    * Select a rule's name to open its details page, then select **Edit rule settings**.
4. Modify the [rule's settings](/solutions/security/detect-and-alert/using-the-rule-ui.md).
5. Select **Save changes**.

::::{admonition} Tracking modifications
:applies_to: { stack: ga 9.1+ }

After saving changes to a prebuilt rule, modified fields are marked with the **Modified** badge. From the rule's details page, select the badge to view a side-by-side comparison of the original Elastic version and your modified version. Deleted characters are highlighted in red; added characters are highlighted in green. You can also access this comparison by clicking the **Modified Elastic rule** badge under the rule's name.
::::

### Considerations for editing prebuilt rules

* **Updates might cause conflicts**: When Elastic releases an update that changes the same fields you modified, you need to resolve the conflict. Refer to [Resolve update conflicts](/solutions/security/detect-and-alert/update-prebuilt-rules.md#resolve-reduce-rule-conflicts).
* **Revert if needed**: You can restore the original Elastic version if it's still available in your system. The revert option is hidden when the original version is missing. Keep your prebuilt rules updated to ensure this option remains available. Refer to [Revert to Elastic version](#revert-prebuilt-rules).


## Duplicate and modify prebuilt rules [duplicate-prebuilt-rules]

If you can't edit prebuilt rules directly, or if you want to preserve the original rule while creating a customized version, duplicate the rule first.

:::{important}
Duplicated rules are entirely separate from the original prebuilt rule. They don't receive Elastic updates when the prebuilt rule is updated.
::::

1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the **Rules** table, select the **Elastic rules** filter.
3. Do one of the following:
    * Duplicate a single rule: Select the **All actions** menu {icon}`boxes_horizontal` on the rule, then select **Duplicate**.
    * Duplicate multiple rules: Select one or more rules (or select **Select all *x* rules**), then select **Bulk actions** > **Duplicate**.
4. If the rule has exceptions, select how to handle them:
    * Duplicate the rule and its exceptions (active and expired)
    * Duplicate the rule and active exceptions only
    * Duplicate only the rule

    :::{admonition} Exceptions of duplicated rules
    If you duplicate a rule and its exceptions, copies of the exceptions are created and added to the duplicated rule's [default rule list](/solutions/security/detect-and-alert/rule-exceptions.md). If the original rule used exceptions from a shared exception list, the duplicated rule references the same shared exception list.
    :::

5. Select **Duplicate**.

After duplicating a rule, modify the new rule's settings as needed. If you don't want both rules running, turn off or delete the original prebuilt rule.


## Add exceptions [add-exceptions-prebuilt]

All subscriptions allow you to add exceptions to prebuilt rules. Exceptions prevent rules from generating alerts for specific conditions. For more guidance, refer to [Add and manage exceptions](/solutions/security/detect-and-alert/add-manage-exceptions.md).


## Configure rule actions [configure-actions-prebuilt]

All subscriptions allow you to configure rule actions (notifications) on prebuilt rules. For more guidance, refer to [Rule actions](/solutions/security/detect-and-alert/common-rule-settings.md#rule-notifications).

## Revert to Elastic version [revert-prebuilt-rules]

With an Enterprise subscription (or Security Analytics Complete), you can [edit prebuilt rules directly](#edit-prebuilt-rules). If you've modified a prebuilt rule and want to restore the original Elastic version:

1. Open the rule's details page.
2. Select the **All actions** menu {icon}`boxes_horizontal`, then select **Revert to Elastic version**.
3. In the flyout, review the modified fields. Deleted characters are highlighted in red; added characters are highlighted in green.
4. Select **Revert** to restore the modified fields to their original versions.

::::{note}
If you haven't updated the rule in a while, its original version might be unavailable for comparison. You can avoid this by regularly [updating prebuilt rules](/solutions/security/detect-and-alert/update-prebuilt-rules.md).
::::
