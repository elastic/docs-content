---
navigation_title: Known issues
---

# {{fleet}} and {{agent}} known issues [fleet-elastic-agent-known-issues]
Known issues are significant defects or limitations that may impact your implementation. These issues are actively being worked on and will be addressed in a future release. Review the {{fleet}} and {{agent}} known issues to help you make informed decisions, such as upgrading to a new version.

% Use the following template to add entries to this page.

% :::{dropdown} Title of known issue
% **Applicable versions for the known issue and the version for when the known issue was fixed**
% On [Month Day, Year], a known issue was discovered that [description of known issue].
% For more information, check [Issue #](Issue link).

% **Workaround** 
% Workaround description.

:::

:::dropdown [macOS] Osquery integration fails to start on fresh agent installs

**Affects version: 9.1.0 (macOS only)**

On May 26th, 2025, a known issue was discovered that causes the `osquery` integration to fail on new Elastic Agent installations on macOS. During the installation process, the required `osquery.app/` directory is removed, which prevents the integration from starting.

For more information, check [Issue #8245](https://github.com/elastic/elastic-agent/issues/8245).

**Workaround** 
As a workaround, you can manually restore the `osquery.app/` directory from a working installation or download it from the [official osquery site](https://osquery.io/downloads/official/), and then restart the Elastic Agent.

