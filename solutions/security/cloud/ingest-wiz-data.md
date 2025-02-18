---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/ingest-wiz-data.html
  - https://www.elastic.co/guide/en/serverless/current/ingest-wiz-data.html
---

# Ingest Wiz data

% What needs to be done: Lift-and-shift

% Use migrated content from existing pages that map to this page:

% - [x] ./raw-migrated-files/security-docs/security/ingest-wiz-data.md
% - [ ] ./raw-migrated-files/docs-content/serverless/ingest-wiz-data.md

In order to enrich your {{elastic-sec}} workflows with third-party cloud security posture and vulnerability data collected by Wiz:

* Follow the steps to [set up the Wiz integration](https://docs.elastic.co/en/integrations/wiz).
* Make sure the integration version is at least 2.0.1.
* Ensure you have `read` privileges for the following indices: `security_solution-*.misconfiguration_latest`, `security_solution-*.vulnerability_latest`.
* While configuring the Wiz integration, turn on **Cloud Configuration Finding logs** and **Vulnerability logs**. We recommend you also set the **Initial Interval** values for both settings to `2160h` (equivalent to 90 days) to ingest existing logs.

:::{image} ../../../images/security-wiz-config-finding-logs.png
:alt: Wiz integration settings showing the findings toggle
:::

:::{image} ../../../images/security-wiz-config-vuln-logs.png
:alt: Wiz integration settings showing the vulnerabilities toggle
:::

After you’ve completed these steps, Wiz data will appear on the [Misconfiguations](/solutions/security/cloud/findings-page.md) and [Vulnerabilities](https://www.elastic.co/guide/en/security/current/vuln-management-findings.html) tabs of the Findings page.

:::{image} ../../../images/security-wiz-findings.png
:alt: Wiz data on the Findings page
:::

Any available findings data will also appear in the entity details flyouts for related [alerts](/solutions/security/detect-and-alert/view-detection-alert-details.md#insights-section). If alerts are present for a user or host that has findings data from Wiz, the findings will appear on the [users](/solutions/security/explore/users-page.md#user-details-flyout), and [hosts](/solutions/security/explore/hosts-page.md#host-details-flyout) flyouts.
