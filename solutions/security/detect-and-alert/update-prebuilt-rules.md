---
navigation_title: Update prebuilt rules
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Update Elastic Security prebuilt detection rules to stay current with the latest threat intelligence, resolve conflicts, and preserve your customizations.
---

# Update Elastic prebuilt rules [update-prebuilt-rules]

Elastic regularly updates prebuilt rules to optimize their performance and ensure they detect the latest threats and techniques. This page explains how to review and apply updates to your installed prebuilt rules.

How updates handle your customizations depends on whether your subscription lets you [edit prebuilt rules directly](/solutions/security/detect-and-alert/customize-prebuilt-rules.md#customize-subscription-capabilities). If it does, {{elastic-sec}} keeps them where possible and gives you more options to review updates and resolve conflicts. If it doesn't, each update replaces the rule with the Elastic version.

:::{admonition} Air-gapped environments
For deployments without internet access, refer to [Prebuilt rules in air-gapped environments](/solutions/security/detect-and-alert/prebuilt-rules-airgapped.md).
:::

## Check for available updates [update-availability]

When updated versions are available for your installed prebuilt rules, the **Rule Updates** tab appears on the **{{siem-rules-ui}}** page.

::::{note}
The **{{siem-rules-ui}}** page was renamed from **Rules** in 9.3.1 and 9.2.6.
::::

:::{admonition} Automatic updates
On {{stack}}, automatic updates are supported for the current {{elastic-sec}} version and the two previous minor releases. For example, if you're on version 9.0, you can use the Rules UI to update prebuilt rules until version 9.3 is released. After that, you can still manually download and install updates, but must upgrade {{elastic-sec}} to receive automatic updates again.
:::

## Review updates [review-updates]

Before applying updates, you can examine what's changing in each rule.

1. Find **{{siem-rules-ui}}** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the Rules table, select the **Rule Updates** tab.

    ::::{note}
    The **Rule Updates** tab doesn't appear if all your installed prebuilt rules are up to date.
    ::::

3. Select a rule name to open the rule update flyout and review the changes.

To preview an update, select the **Elastic update overview** tab for a field-by-field view, or the **JSON view** tab for a full rule comparison. Both tabs display side-by-side comparisons of the **Current rule** and the **Elastic update** version. Deleted characters are highlighted in red; added characters are highlighted in green.

:::{image} /solutions/images/security-prebuilt-rules-update-diff-basic.png
:alt: Prebuilt rule comparison
:screenshot:
:::

::::{dropdown} Additional review options if you can edit prebuilt rules directly
:name: enterprise-review-options

The rule update flyout also includes these options:

* **Compare different versions**: Use the **Diff view** drop-down menu to compare different versions of a rule field. For example, compare changes you made to the current version with changes from the incoming Elastic update.

    ::::{note}
    If you haven't updated the rule in a while, its original version might be unavailable for comparison. You can avoid this by updating prebuilt rules regularly.
    ::::

* **Check update status**: View the status of the entire rule update and for each field being changed. Refer to [Field update statuses](#rule-field-update-statuses) for status definitions.

* **Edit the final update**: Change the update that will be applied to any field. Go to the **Final update** section, make your changes, and save them.

    ::::{important}
    You can't edit an Elastic update that changes the rule's type. To keep your customizations, [duplicate the rule](/solutions/security/detect-and-alert/customize-prebuilt-rules.md#duplicate-prebuilt-rules) before you update it.
    ::::

:::{image} /solutions/images/security-prebuilt-rules-update-diff-advanced.png
:alt: Prebuilt rule comparison with advanced options
:screenshot:
:::

::::


## Preserve customizations during updates [preserve-customizations]

To keep your customizations when you apply updates, follow the guidance that matches whether you can [edit prebuilt rules directly](/solutions/security/detect-and-alert/customize-prebuilt-rules.md#customize-subscription-capabilities).

::::{dropdown} If you can edit prebuilt rules directly
:name: enterprise-modified-rules

{{elastic-sec}} attempts to merge your changes with the Elastic update. If conflicts arise:

* **Auto-resolved conflicts**: {{elastic-sec}} suggests a resolution for your review. The field displays a `Review required` status.
* **Unresolved conflicts**: You must manually select how to resolve the conflict. The field displays an `Action required` status.

:::{note}
If the rule's original version is unavailable, as described in [Additional review options](#enterprise-review-options), {{elastic-sec}} cannot identify which changes are yours. For fields that hold multiple values, such as **Tags**, **Reference URLs**, and **Indicator index patterns**, the suggested resolution is Elastic's values rather than a combination of both sets. These fields display the `Review required` status. To keep your values, open the rule update flyout and edit the **Final update** value before you accept it.
:::

Refer to [Resolve update conflicts](#resolve-reduce-rule-conflicts) for guidance on handling conflicts.

If an Elastic update changes the rule's type, updating the rule overwrites your customizations. To keep a copy of them, refer to [Update rules with a rule type change](#update-rule-type-change).

::::{tip}
Use the **Modified/Unmodified** drop-down menu in the **Rule Updates** tab to filter for modified rules that may need attention.
::::

::::

::::{dropdown} If you can't edit prebuilt rules directly
:name: basic-modified-rules

Each update replaces the rule with the Elastic version, which overwrites any customizations the rule already has, for example from before a subscription change. To keep them:

1. [Duplicate the rule](/solutions/security/detect-and-alert/customize-prebuilt-rules.md#duplicate-prebuilt-rules).
2. Apply the update to the original prebuilt rule.
3. Continue using your duplicated rule with your customizations.

::::


## Apply updates [apply-updates]

From the **Rule Updates** tab, do one of the following:

* **Update all available rules**: Select **Update all**. If you can edit prebuilt rules directly and some rules have conflicts, a dialog opens so you can decide which rules to update.
* **Update a single rule**: Select **Update rule** for that rule.
* **Update multiple rules**: Select the rules and select **Update *x* selected rule(s)**.

Bulk updates might skip some [rules with a rule type change](#update-rule-type-change).

::::{tip}
Use the search bar and **Tags** filter to find specific rules. For example, filter by `OS: Windows` if your environment only includes Windows endpoints. For more on tag categories, refer to [Prebuilt rule tags](/solutions/security/detect-and-alert/prebuilt-rule-components.md#prebuilt-rule-tags).
::::

:::{image} /solutions/images/security-prebuilt-rules-update.png
:alt: The Rule Updates tab on the Detection rules (SIEM) page
:screenshot:
:::

### Update rules and discard your customizations [update-to-elastic-version]
```{applies_to}
serverless: ga
stack: ga 9.4+
```

If you want to update prebuilt rules without keeping your customizations, you can update them to the Elastic version instead of resolving conflicts. This option requires a subscription that lets you [edit prebuilt rules directly](/solutions/security/detect-and-alert/customize-prebuilt-rules.md#customize-subscription-capabilities). The updated rules keep their exceptions and actions. On {{stack}} 9.4 and 9.5, this option is available starting in 9.4.8 and 9.5.5.

1. From the **Rule Updates** tab, do one of the following:

    * To update specific rules, select them, then select the {icon}`chevron_single_down` arrow next to **Update *x* selected rule(s)**.
    * To update every rule on the tab that matches your current search and filters, select the {icon}`chevron_single_down` arrow next to **Update all**.

2. Select **Update to Elastic version**. If a confirmation dialog opens, review how many rules lose customizations or change type, then confirm the update.
3. If any rules changed type, open each rule's details page and check that its exceptions and actions still work as you intend with the new rule type. Exceptions are on the **Rule exceptions** tab. For how each rule type evaluates exceptions, refer to [Rule type considerations](/solutions/security/detect-and-alert/add-manage-exceptions.md#rule-type-considerations).

To return a rule to the Elastic version you installed without applying the update, use [Revert to Elastic version](/solutions/security/detect-and-alert/customize-prebuilt-rules.md#revert-prebuilt-rules) instead.

### Update rules with a rule type change [update-rule-type-change]

Some Elastic updates change a rule's type, for example from custom query to event correlation. For these rules, the rule update flyout shows a **Rule type change** callout. When you apply one of these updates:

* The update overwrites your customizations. To keep them, [duplicate the rule](/solutions/security/detect-and-alert/customize-prebuilt-rules.md#duplicate-prebuilt-rules) before you update. The duplicate keeps the old rule type but doesn't receive Elastic updates.
* The rule keeps its exceptions and actions, but they might behave differently with the new rule type. After you update, check them on the rule's details page. For how rule types evaluate exceptions, refer to [Rule type considerations](/solutions/security/detect-and-alert/add-manage-exceptions.md#rule-type-considerations).

If you can't edit prebuilt rules directly, **Update all** and **Update *x* selected rule(s)** include every rule with a type change. If you can, these options handle rules with a type change as follows:

| Rule | **Update all** and **Update *x* selected rule(s)** |
|---|---|
| Customized | Skipped. Update each rule individually, or use [Update to Elastic version](#update-to-elastic-version). |
| Not customized {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` | Included, but listed as auto-resolved conflicts. To update only these rules, filter by **Unmodified** first. In the **Conflicts found** dialog, select **Update rules**. On {{stack}} 9.4 and 9.5, bulk updates include these rules starting in 9.4.8 and 9.5.5. Earlier versions skip them. |
| Not customized {applies_to}`stack: ga 9.0-9.3` | Skipped. Update each rule individually. |


## Field update statuses [rule-field-update-statuses]

If you can edit prebuilt rules directly, each field of a rule you've customized displays a status when you update the rule. The status shows whether your changes conflict with the incoming Elastic update:

| Status | Description | Action required |
|---|---|---|
| Ready for update | No conflicts. The field can be updated. | None |
| No update | The field isn't being updated by Elastic, but your current value differs from the original. | None. You can still edit the final value if needed. |
| Review required | Elastic auto-resolved a conflict between your changes and the Elastic update. | Review the suggested resolution and accept or edit it. |
| Action required | Elastic couldn't auto-resolve the conflict. | Manually set the field's final value. |


## Resolve update conflicts [resolve-reduce-rule-conflicts]

If you [edit prebuilt rules directly](/solutions/security/detect-and-alert/customize-prebuilt-rules.md#edit-prebuilt-rules), conflicts can arise when Elastic updates the same fields you modified. Keeping prebuilt rules up to date helps minimize the frequency and complexity of these conflicts.

::::{tip}
:applies_to: {serverless: ga, stack: ga 9.4+}
If you don't need to keep your customizations, you can [update the rules to the Elastic version](#update-to-elastic-version) instead of resolving conflicts.
::::

### Review auto-resolved conflicts [auto-resolved-conflicts]

When {{elastic-sec}} can suggest a resolution, the field displays `Review required`. You can still update rules with auto-resolved conflicts, but review each rule individually rather than bulk-updating to avoid unintended changes.

### Fix unresolved conflicts [unresolved-conflicts]

When {{elastic-sec}} can't resolve a conflict, the field displays `Action required`. To fix unresolved conflicts:

1. From the **Rule Updates** tab, select the rule name or select **Review** to open the rule update flyout.

    ::::{tip}
    Fields with unresolved conflicts have the `Action required` status.
    ::::

2. Go to the **Final update** section and do any of the following:

    * Keep your current value instead of accepting the Elastic update.
    * Accept the Elastic update and overwrite your current value.
    * Combine your changes with the Elastic update.

3. Select **Save and accept** to apply your changes. The field's status changes to `Ready for update`.

After resolving all conflicts, select **Update rule** to apply the update.
