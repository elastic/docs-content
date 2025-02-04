---
navigation_title: "Reporting"
---

# Reporting production considerations [reporting-production-considerations]


To generate reports, {{kib}} uses the Chromium web browser, which runs on the server in headless mode. Chromium is an open-source project not related to Elastic, and is embedded into {{kib}}. Chromium may require additional OS dependencies to run properly.

::::{note} 
Chromium is not embedded into {{kib}} for the Darwin (Mac OS) architecture. When running on Darwin, Reporting will download Chromium into the proper area of the {{kib}} installation path the first time the server starts. To separately download and install the browser, see [Manually install the Chromium browser for Darwin](../../../explore-analyze/report-and-share/reporting-troubleshooting-pdf.md#reporting-manual-chromium-install).

::::



## Chromium sandbox [reporting-chromium-sandbox] 

For an additional layer of security, use the sandbox. The Chromium sandbox uses operating system-provided mechanisms to ensure that code execution cannot make persistent changes to the computer or access confidential information. The specific sandboxing techniques differ for each operating system.


### Linux sandbox [reporting-linux-sandbox] 

The Linux sandbox depends on user namespaces, which were introduced with the 3.8 Linux kernel. However, many distributions don’t support or allow non-privileged processes to create user namespaces, or they require the CAP_SYS_ADMIN capability. The {{report-features}} automatically disable the sandbox when it detects it is running on systems where it is not enabled. Without explicitly setting `xpack.screenshotting.browser.chromium.disableSandbox: false` in `kibana.yml`, the {{report-features}} may detect that it can’t be enabled. In the event it is automatically disabled, you’ll see the following message in your {{kib}} startup logs: `Chromium sandbox provides an additional layer of protection, but is not supported for your OS. Automatically setting 'xpack.screenshotting.browser.chromium.disableSandbox: true'.`

Reporting automatically enables the Chromium sandbox at startup when a supported OS is detected. However, if your kernel is 3.8 or newer, it’s recommended to set `xpack.screenshotting.browser.chromium.disableSandbox: false` in your `kibana.yml` to explicitly enable the sandbox.


### Docker [reporting-docker-sandbox] 

When running {{kib}} in a Docker container, all container processes are run within a usernamespace with seccomp-bpf and AppArmor profiles that prevent the Chromium sandbox from being used. In these situations, disabling the sandbox is recommended, as the container implements similar security mechanisms.

