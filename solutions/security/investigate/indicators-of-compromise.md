---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/indicators-of-compromise.html
  - https://www.elastic.co/guide/en/serverless/current/security-indicators-of-compromise.html
---

# Indicators of compromise

The Indicators page collects data from enabled threat intelligence feeds and provides a centralized view of indicators, also known as indicators of compromise (IoCs). This topic helps you set up the Indicators page and explains how to work with IoCs.

::::{admonition} Requirements
* In {{stack}}, the Indicators page is an [Enterprise subscription](https://www.elastic.co/pricing) feature.
* In serverless, the Indicators page requires the Security Analytics Complete [project feature](/deploy-manage/deploy/elastic-cloud/project-settings.md)
* You must have *one* of the following installed on the hosts you want to monitor:

    * **{{agent}}** - Install a [{{fleet}}-managed {{agent}}](https://www.elastic.co/guide/en/fleet/current/install-fleet-managed-elastic-agent.html) and ensure the agent’s status is `Healthy`. Refer to [{{fleet}} Troubleshooting](/troubleshoot/ingest/fleet/common-problems.md) if it isn’t.
    * **{{filebeat}}** - Install [{{filebeat}}](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-installation-configuration.html) version 8.x or later. Earlier {{filebeat}} versions are incompatible with ECS and will prevent indicator data from displaying in the Indicators table.


::::


:::{image} ../../../images/security-indicators-table.png
:alt: Shows the Indicators page
:class: screenshot
:::


## Threat intelligence and indicators [ti-indicators]

Threat intelligence is a research function that analyzes current and emerging threats and recommends appropriate actions to strengthen a company’s security posture. Threat intelligence requires proactivity to be useful, such as gathering, analyzing, and investigating various threat and vulnerability data sources.

An indicator, also referred to as an IoC, is a piece of information associated with a known threat or reported vulnerability. There are many types of indicators, including URLs, files, domains, email addresses, and more. Within SOC teams, threat intelligence analysts use indicators to detect, assess, and respond to threats.


## Set up the Indicators page [setup-indicators-page]

Install a threat intelligence integration to add indicators to the Indicators page.

1. From the {{security-app}}, click **Add Integrations**.
2. In the search bar, search for `Threat Intelligence` to get a list of threat intelligence integrations.
3. Select a threat intelligence integration, then complete the integration’s guided installation.

    ::::{note}
    For more information about available fields, go to the [Elastic integration documentation](https://docs.elastic.co/integrations) and search for a specific threat intelligence integration.
    ::::

4. Return to the Indicators page in {{elastic-sec}}. Refresh the page if indicator data isn’t displaying.


## Indicators page UI [intelligence-page-ui]

After you add indicators to the Indicators page, you can [examine](#examine-indicator-details), search, filter, and take action on indicator data. Indicators also appear in the Trend view, which shows the total values in the legend.

:::{image} ../../../images/security-interact-with-indicators-table.gif
:alt: interact with indicators table
:class: screenshot
:::


### Examine indicator details [examine-indicator-details]

Learn more about an indicator by clicking **View details**, then opening the Indicator details flyout. The flyout contains these informational tabs:

* **Overview**: A summary of the indicator, including the indicator’s name, the threat intelligence feed it came from, the indicator type, and additional relevant data.

    ::::{note}
    Some threat intelligence feeds provide  [Traffic Light Protocol (TLP) markings](https://www.cisa.gov/tlp#:~:text=Introduction,shared%20with%20the%20appropriate%20audience). The `TLP Marking` and `Confidence` fields will be empty if the feed doesn’t provide that data.
    ::::

* **Table**: The indicator data in table format.
* **JSON**: The indicator data in JSON format.

    :::{image} ../../../images/security-indicator-details-flyout.png
    :alt: Shows the Indicator details flyout
    :class: screenshot
    :::



## Find related security events [find-related-sec-events]

Investigate an indicator in [Timeline](/solutions/security/investigate/timeline.md) to identify and predict related events in your environment. You can add an indicator to Timeline from the Indicators table or the Indicator details flyout.

:::{image} ../../../images/security-indicator-query-timeline.png
:alt: Shows the results of an indicator being investigated in Timeline
:class: screenshot
:::

When you add an indicator to Timeline, a new Timeline opens with an auto-generated KQL query. The query contains the indicator field-value pair that you selected plus the field-value pair of the automatically mapped source event. By default, the query’s time range is set to seven days before and after the indicator’s `timestamp`.


### Example indicator Timeline investigation [example-indicator-timeline]

The following image shows a file hash indictor being investigated in Timeline. The indicator field-value pair is:

`threat.indicator.file.hash.sha256 : 116dd9071887611c19c24aedde270285a4cf97157b846e6343407cf3bcec115a`

:::{image} ../../../images/security-indicator-in-timeline.png
:alt: Shows the results of an indicator being investigated in Timeline
:class: screenshot
:::

The auto-generated query contains the indicator field-value pair (mentioned previously) and the auto-mapped source event field-value pair, which is:

`file.hash.sha256 : 116dd9071887611c19c24aedde270285a4cf97157b846e6343407cf3bcec115a`

The query results show an alert with a matching `file.hash.sha256` field value, which may indicate suspicious or malicious activity in the environment.


## Attach indicators to cases [attach-indicator-to-case]

Attaching indicators to cases provides more context and available actions for your investigations. This feature allows you to easily share or escalate threat intelligence to other teams.

To add indicators to cases:

1. From the Indicators table, click the **More actions** (**…​​**) menu. Alternatively, open an indicator’s details, then select **Take action**.
2. Select one of the following:

    * **Add to existing case**: From the **Select case** dialog box, select the case to which you want to attach the indicator.
    * **Add to new case**: Configure the case details. Refer to [Open a new case](/solutions/security/investigate/open-manage-cases.md#cases-ui-open) to learn more about opening a new case.

    The indicator is added to the case as a new comment.


:::{image} ../../../images/security-indicator-added-to-case.png
:alt: An indicator attached to a case
:class: screenshot
:::


### Review indicator details in cases [review-indicator-in-case]

When you attach an indicator to a case, the indicator is added as a new comment with the following details:

* **Indicator name**: Click the linked name to open the Indicator details flyout, which contains the following tabs:

    * **Overview**: A summary of the threat indicator, including its name and type, which threat intelligence feed it came from, and additional relevant data.

        ::::{note}
        Some threat intelligence feeds provide  [Traffic Light Protocol (TLP) markings](https://www.cisa.gov/tlp#:~:text=Introduction,shared%20with%20the%20appropriate%20audience). The `TLP Marking` and `Confidence` fields will be empty if the feed doesn’t provide that data.
        ::::

    * **Table**: The indicator data in table format.
    * **JSON**: The indicator data in JSON format.

* **Feed name**: The threat feed from which the indicator was ingested.
* **Indicator type**: The indicator type, for example, `file` or `.exe`.


### Remove indicators from cases [delete-indicator-from-case]

To remove an indicator attached to a case, click the **More actions** (**…​​**) menu → **Delete attachment** in the case comment.

:::{image} ../../../images/security-remove-indicator.png
:alt: Removing an indicator from a case
:class: screenshot
:::


## Use data from indicators to expand the blocklist [add-indicator-to-blocklist]

Add indicator values to the [blocklist](/solutions/security/manage-elastic-defend/blocklist.md) to prevent selected applications from running on your hosts. You can use MD5, SHA-1, or SHA-256 hash values from `file` type indicators.

You can add indicator values to the blocklist from the Indicators table or the Indicator details flyout. From the Indicators table, select the **More actions** (**…​​**) menu → **Add blocklist entry**.  Alternatively, open an indicator’s details, then select the **Take action** menu → **Add blocklist entry**.

::::{note}
Refer to [Blocklist](/solutions/security/manage-elastic-defend/blocklist.md) for more information about blocklist entries.
::::


