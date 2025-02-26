---
mapped_pages:
  - https://www.elastic.co/guide/en/security/master/release-notes-header-9.0.0.html#known-issue-9.0.0

navigation_title: "Elastic Security"
---

# Elastic Security known issues [elastic-security-known-issues]

% Use the following template to add entries to this page.

% :::{dropdown} Title of known issue
% **Details** 
% On [Month/Day/Year], a known issue was discovered that [description of known issue].

% **Workaround** 
% Workaround description.

% **Resolved**
% On [Month/Day/Year], this issue was resolved.

:::

% What needs to be done: Write from scratch

## 9.0.0 [known-issues]

:::{dropdown} Duplicate alerts can be produced from manually running threshold rules
**Details** 
On November 12, 2024, it was discovered that manually running threshold rules could produce duplicate alerts if the date range was already covered by a scheduled rule execution.
:::

