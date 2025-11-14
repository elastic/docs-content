---
description: Troubleshoot PDF and PNG export issues including browser dependencies, sandbox requirements, font rendering, connection errors, and system requirements.
navigation_title: PDF/PNG
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/reporting-troubleshooting-pdf.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---



# PDF/PNG [reporting-troubleshooting-pdf]

PDF and PNG reporting in {{product.kibana}} uses a headless Chromium browser to capture screenshots of dashboards and visualizations. Issues can occur due to missing system dependencies, sandbox restrictions, font problems, or resource constraints. This page helps you diagnose and resolve common PDF and PNG export problems.

Common issues include:

* Missing Network Security Service (NSS) libraries
* Chromium sandbox requirements and user namespace restrictions
* Text rendering incorrectly due to missing fonts
* Connection refused errors with server host settings
* Memory limitations causing page crashes

**Technical summary**: Use the built-in reporting diagnostics tool at **{{reports-app}} > Run reporting diagnostics** to identify common configuration issues. For Docker or {{ecloud}} deployments, most dependencies are preconfigured.

For general troubleshooting guidance, refer to [Troubleshooting](reporting-troubleshooting.md).

::::{note}
PDF and PNG reports work best with moderate amounts of visual data. The feature provides high-level export capability but is not intended for bulk export. If you need to export several pages of image data, use multiple report jobs to export a small number of pages at a time. If exported dashboard screenshots contain a large number of pixels, split large dashboards into smaller artifacts to reduce memory and CPU usage.

For the most reliable configuration of PDF/PNG {{report-features}}, install {{product.kibana}} using [Docker](../../deploy-manage/deploy/self-managed/install-kibana-with-docker.md) or use [{{ecloud}}](https://cloud.elastic.co).

::::


## Reporting diagnostics [reporting-diagnostics]

Reporting comes with a built-in utility to try to automatically find common issues. When {{product.kibana}} is running, navigate to the **Report Listing** page, and click **Run reporting diagnostics**. This will open up a diagnostic tool that checks various parts of the {{product.kibana}} deployment and comes up with any relevant recommendations.

If the diagnostic information doesn’t reveal the problem, you can troubleshoot further by starting the Kibana server with an environment variable for revealing additional debugging logs. Refer to [Puppeteer debug logs](#reporting-troubleshooting-puppeteer-debug-logs).


## Network security service libraries [reporting-troubleshooting-nss-dependency]

You must install Network Security Service (NSS) libraries for {{report-features}} to work. Reporting using the Chromium browser relies on these libraries. Install the appropriate nss package for your distribution. Refer to [Install the dependencies for the headless browser](../report-and-share.md#install-reporting-packages).


## Chromium sandbox requirements [reporting-troubleshooting-sandbox-dependency]

Chromium uses sandboxing techniques that are built on top of operating system primitives. The Linux sandbox depends on user namespaces, which were introduced with the 3.8 Linux kernel. However, many distributions don’t have user namespaces enabled by default or they require the CAP_SYS_ADMIN capability. If the sandbox is not explicitly disabled in Kibana, either based on operating system detection or with the `xpack.screenshotting.browser.chromium.disableSandbox` setting, Chrome will try to enable the sandbox. If it fails due to operating system or permissions restrictions, Chrome will crash during initialization.

Elastic recommends that you research the feasibility of enabling unprivileged user namespaces before disabling the sandbox. An exception is if you are running Kibana in Docker because the container runs in a user namespace with the built-in seccomp/bpf filters.


## Text rendered incorrectly in generated reports [reporting-troubleshooting-text-incorrect]

If a report label is rendered as an empty rectangle, no system fonts are available. Install at least one font package on the system.

If the report is missing certain Chinese, Japanese or Korean characters, ensure that a system font with those characters is installed.


## Missing data in PDF report of data table visualization [reporting-troubleshooting-missing-data]

There is currently a known limitation with the data table visualization that only the first page of data rows, which are the only data visible on the screen, are shown in PDF reports.


## Connection refused errors [reporting-troubleshooting-pdf-connection-refused]

If PDF or PNG reports are not working due to a "connection refused" or "unable to connect" type of error, ensure that the [`kibana.yml`](/deploy-manage/stack-settings.md) file uses the setting of `server.host: 0.0.0.0`. Also verify that no firewall rules or other routing rules prevent local services from accessing this address. Find out more at [Set the `server.host` for the headless browser](../report-and-share.md#set-reporting-server-host).


## File permissions [reporting-troubleshooting-file-permissions]

Ensure that the `headless_shell` binary located in your Kibana data directory is owned by the user who is running Kibana, that the user has the execute permission, and if applicable, that the filesystem is mounted with the `exec` option.

::::{note}
The Chromium binary is located in the Kibana installation directory as `data/headless_shell-OS_TYPE/headless_shell`. The full path is logged the first time Kibana starts when verbose logging is enabled.

::::



## Puppeteer debug logs [reporting-troubleshooting-puppeteer-debug-logs]

The Chromium browser that {{product.kibana}} launches on the server is driven by a NodeJS library for Chromium called Puppeteer. The Puppeteer library has its own command-line method to generate its own debug logs, which can sometimes be helpful, particularly to figure out if a problem is caused by Kibana or Chromium. Learn more [debugging tips](https://github.com/GoogleChrome/puppeteer/blob/v1.19.0/README.md#debugging-tips).

Using Puppeteer’s debug method when launching Kibana would look like:

```
env DEBUG="puppeteer:*" ./bin/kibana
```

The internal DevTools protocol traffic will be logged via the `debug` module under the `puppeteer` namespace.

The Puppeteer logs are very verbose and could possibly contain sensitive information. Handle the generated output with care.


## System requirements [reporting-troubleshooting-system-requirements]

In Elastic Cloud, the {{product.kibana}} instances that most configurations provide by default is for 1GB of RAM for the instance. That is enough for {{product.kibana}} {{report-features}} when the visualization or dashboard is relatively simple, such as a single pie chart or a dashboard with a few visualizations. However, certain visualization types incur more load than others. For example, a TSVB panel has a lot of network requests to render.

If the {{product.kibana}} instance doesn’t have enough memory to run the report, the report fails with an error such as `Error: Page crashed!`. In this case, try increasing the memory for the {{product.kibana}} instance to 2GB.


## Unable to connect to Elastic Maps Service [reporting-troubleshooting-maps-ems]

[Elastic Maps Service ({{ems-init}})](https://www.elastic.co/elastic-maps-service) is a service that hosts tile layers and vector shapes of administrative boundaries. If a report contains a map with a missing basemap layer or administrative boundary, the {{product.kibana}} server does not have access to {{ems-init}}. Refer to [*Connect to Elastic Maps Service*](../visualize/maps/maps-connect-to-ems.md) for information about how to connect your {{product.kibana}} server to {{ems-init}}.


## Manually install the Chromium browser for Darwin [reporting-manual-chromium-install]

Chromium is not embedded into {{product.kibana}} for the Darwin (Mac OS) architecture. When running {{product.kibana}} on Darwin, {{report-features}} will download Chromium into the proper area of the {{product.kibana}} installation path the first time the server starts. If the server does not have access to the internet, you must download the Chromium browser and install it into the {{product.kibana}} installation path.

1. Download the Chromium zip file:

    * For [x64](https://commondatastorage.googleapis.com/chromium-browser-snapshots/Mac/901912/chrome-mac.zip) systems
    * For [ARM](https://commondatastorage.googleapis.com/chromium-browser-snapshots/Mac_Arm/901913/chrome-mac.zip) systems

2. Copy the zip file into the holding area. Relative to the root directory of {{product.kibana}}, the path is:

    * `.chromium/x64` for x64 systems
    * `.chromium/arm64` for ARM systems


When {{product.kibana}} starts, it will automatically extract the browser from the zip file and is then ready for PNG and PDF reports.

