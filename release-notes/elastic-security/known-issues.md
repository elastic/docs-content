---
navigation_title: "Known issues"
---

# {{elastic-sec}} known issues [elastic-security-known-issues]
Known issues are significant defects or limitations that may impact your implementation. These issues are actively being worked on and will be addressed in a future release. Review the {{elastic-sec}} known issues to help you make informed decisions, such as upgrading to a new version.

% Use the following template to add entries to this page.

% :::{dropdown} Title of known issue
% **Applicable versions for the known issue and the version for when the known issue was fixed**
% On [Month Day, Year], a known issue was discovered that [description of known issue].
% For more information, check [Issue #](Issue link).

% **Workaround**
% Workaround description.

:::

:::{dropdown} Installing an {{elastic-defend}} integration or a new agent policy upgrades installed prebuilt rules, reverting user customizations and overwriting user-added actions and exceptions

**{{stack}} versions: 9.0.0**

On April 10, 2025, it was discovered that when you install a new {{elastic-defend}} integration or agent policy, the installed prebuilt detection rules upgrade to their latest versions (if any new versions are available). The upgraded rules lose any user-added rule actions, exceptions, and customizations.  

**Workaround**

To resolve this issue, before you add an {{elastic-defend}} integration to a policy in {{fleet}}, apply any pending prebuilt rule updates. This will prevent rule actions, exceptions, and customizations from being overwritten.

:::

:::{dropdown} The technical preview badge incorrectly displays on the alert suppression fields for event correlation rules

**{{stack}} versions: 9.0.0**

On April 8, 2025, it was discovered that alert suppression for event correlation rules is incorrectly shown as being in technical preview when you create a new rule. For more information, check [#1021](https://github.com/elastic/docs-content/issues/1021).

:::
