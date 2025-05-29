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

% :::

:::{dropdown} [macOS] Osquery integration fails to start on fresh agent installs

**Applies to: {{agent}} 9.0.0 and 9.0.1 (macOS only)**

On May 26th, 2025, a known issue was discovered that causes the `osquery` integration to fail on new {{agent}} installations on macOS. During the installation process, the required `osquery.app/` directory is removed, which prevents the integration from starting.

For more information, check [Issue #8245](https://github.com/elastic/elastic-agent/issues/8245).

**Workaround** 

As a workaround, you can manually restore the `osquery.app/` directory as follows:

1. Extract the {{agent}} package, but do not install it yet.

2. Open the following file in the extracted directory:

   ```
   data/elastic-agent-68f3ed/components/agentbeat.spec.yml
   ```

3. Locate the `component_files` section at the top of the file. It should look similar to this:

   ```yaml
   version: 2
   component_files:
     - certs/*
     - lenses/*
     - module/*
     - "osquery-extension.ext"
     - "osquery-extension.exe"
     - osqueryd
     - "osqueryd.exe"
   ```

4. Add the following entry to the end of the list:

   ```yaml
     - "osquery.app/*"
   ```

   The updated section should now look like this:

   ```yaml
   version: 2
   component_files:
     - certs/*
     - lenses/*
     - module/*
     - "osquery-extension.ext"
     - "osquery-extension.exe"
     - osqueryd
     - "osqueryd.exe"
     - "osquery.app/*"
   ```

5. Proceed to install {{agent}} from the extracted directory as usual.

:::