---
mapped_pages:
  - https://www.elastic.co/guide/en/security/master/release-notes-header-9.0.0.html#known-issue-9.0.0

navigation_title: "Elastic Security"
---

# {{elastic-sec}} known issues [elastic-security-known-issues]
Known issues are significant defects or limitations that may impact your implementation. These issues are actively being worked on and will be addressed in a future release. Reviewing known issues can help you make informed decisions, such as upgrading to a new version.

% Use the following template to add entries to this page.

% :::{dropdown} Title of known issue
% **Applicable versions for the known issue and the version for when the known issue was fixed**
% On [Month Day, Year], a known issue was discovered that [description of known issue].
% For more information, check [Issue #](Issue link).

% **Workaround** 
% Workaround description.

:::

:::{dropdown} Duplicate alerts can be produced from manually running threshold rules
**Elastic Stack versions: 9.0.0**

On November 12, 2024, it was discovered that manually running threshold rules could produce duplicate alerts if the date range was already covered by a scheduled rule execution.

:::

