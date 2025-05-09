---
navigation_title: "Reporting production considerations"
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/reporting-production-considerations.html
applies_to:
  deployment:
    self: all
---

# {{kib}} reporting in production environments [reporting-production-considerations]

In production environments, it's important to ensure that {{kib}} reporting is both reliable and secure. To generate [reports](/explore-analyze/report-and-share.md), {{kib}} uses the Chromium web browser, which runs on the server in headless mode (without a graphical user interface).

Because this process requires launching a browser within your server environment, you should pay special attention to operating system compatibility, sandboxing, and dependencies.

Chromium is an open-source project not related to Elastic, and is embedded into {{kib}} (except on Darwin). Running Chromium reliably may require [additional OS dependencies](/deploy-manage/kibana-reporting-configuration.md#install-reporting-packages) and proper sandbox configuration to protect your system from potential browser-level vulnerabilities.

::::{note} 
Chromium is not embedded into {{kib}} for the Darwin (Mac OS) architecture. When running on Darwin, Reporting will download Chromium into the proper area of the {{kib}} installation path the first time the server starts. To separately download and install the browser, see [Manually install the Chromium browser for Darwin](../../explore-analyze/report-and-share/reporting-troubleshooting-pdf.md#reporting-manual-chromium-install).
::::

## Chromium sandbox [reporting-chromium-sandbox] 

For an additional layer of security, use the sandbox. The Chromium sandbox uses operating system-provided mechanisms to ensure that code execution cannot make persistent changes to the computer or access confidential information. The specific sandboxing techniques differ for each operating system.

### Linux sandbox [reporting-linux-sandbox] 

On Linux, the Chromium sandbox relies on user namespaces, which are supported in kernels version 3.8 and newer. However, many distributions may:
* Not support user namespaces for non-privileged processes
* Require the `CAP_SYS_ADMIN` capability

As a result, {{kib}} may **automatically disable** the sandbox if it detects that the system does not support it. In that case, you’ll see the following message in your {{kib}} startup logs:

```sh
Chromium sandbox provides an additional layer of protection, but is not supported for your OS. Automatically setting 'xpack.screenshotting.browser.chromium.disableSandbox: true'.
```

By default, if your system does support sandboxing, {{kib}} will **enable it automatically**.

#### Recommendation

Even if sandboxing is likely supported (e.g., kernel 3.8+), we recommend explicitly enabling it to ensure protection is active and avoid relying on auto-detection. To do that, add the following setting to your [`kibana.yml`](/deploy-manage/stack-settings.md) configuration file:

```yaml
xpack.screenshotting.browser.chromium.disableSandbox: false
```

If you know your system doesn't support sandboxing, or if you want to explicitly disable it, you can configure:

```yaml
xpack.screenshotting.browser.chromium.disableSandbox: true
```

### Docker [reporting-docker-sandbox] 

When running {{kib}} inside a Docker container, all container processes are run within a user namespace with `seccomp-bpf` and `AppArmor` profiles that prevent the Chromium sandbox from being used. In this case,  we recommend disabling the sandbox, since the container already provides equivalent isolation.
