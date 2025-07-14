---
navigation_title: Known issues
---

# {{observability}} known issues [elastic-observability-known-issues]
Known issues are significant defects or limitations that may impact your implementation. These issues are actively being worked on and will be addressed in a future release. Review the {{observability}} known issues to help you make informed decisions, such as upgrading to a new version.

% Use the following template to add entries to this page.

% :::{dropdown} Title of known issue
% Applies to: Applicable versions for the known issue
% Description of the known issue.
% For more information, check [Issue #](Issue link).
% **Impact**<br> Impact of the known issue.
% **Workaround**<br> Steps for a workaround until the known issue is fixed.

% :::

:::{dropdown} Observability AI Assistant - Elastic Managed LLM may be automatically selected as default connector

Applies to: {{stack}} 9.x

The Elastic Managed LLM may be automatically selected as your default connector because of existing connector selection logic.
This can occur if you had not previously specified a connector for any of the following reasons:

* You only had one connector available and it was always automatically picked for your conversations.
* You had multiple connectors available but didn’t make a specific selection and used the automatically picked connector for your conversations.
* You previously selected a connector but cleared your browser's local storage or switched browsers or devices.

*And:*

* All of your existing connector names come after the “Elastic Managed LLM connector" when sorted alphabetically.

For more information, check [#2088](https://github.com/elastic/docs-content/issues/2088)

::::