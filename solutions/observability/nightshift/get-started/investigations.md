---
navigation_title: Set up investigations
applies_to:
  serverless:
    observability: preview
description: Enable Elastic nightshift, connect your data and code, run your first investigation, and create your first automation.
products:
  - id: observability
  - id: cloud-serverless
---

# Set up investigations [nightshift-get-started-investigations]

Go from a fresh project to your first investigation and your first automation. This guide follows the **Get started** checklist on the {{nightshift}} home page, so you can keep it open next to {{kib}}.

By the end, {{nightshift}} has investigated a real problem in your data and learned the first things about your system. Before you start, check [what you need](../get-started.md#nightshift-get-started-requirements).

:::::{stepper}

::::{step} Enable {{nightshift}}
:anchor: nightshift-get-started-enable

An admin does this once. Until then, every {{nightshift}} page shows **One-time admin setup required for this space**.

:::{image} ../../../images/nightshift-get-started-enable.png
:alt: The Elastic nightshift home page before setup, with the Enable Elastic nightshift button and the Get started checklist
:screenshot:
:::

Select **Enable {{nightshift}}**.

{{nightshift}} runs every investigation as a service account. Refer to [Privileges that {{nightshift}} runs with](./privileges.md#nightshift-privileges-accounts).

The checklist moves on to **Add data**. No **Enable {{nightshift}}** button? Ask an admin to do this step.
::::

::::{step} Add data
:anchor: nightshift-get-started-add-data

Choose the {{es}} data that investigations query.

:::{image} ../../../images/nightshift-get-started-add-data.png
:alt: The Add data step, with the External Elasticsearch card and the Add data in 10+ other ways card
:screenshot:
:::

**If your data is in this project**, it's already connected. {{nightshift}} creates a **Local Elasticsearch** connector that can read your `logs-*`, `metrics-*`, and `traces-*` data, so the **External Elasticsearch** card shows **1 connector**. Select **Proceed**.

**If your data is in another cluster or project**, add an External {{es}} connector for it. You need this only when [{{cps}}](/deploy-manage/cross-project-search-config.md) can't reach that data. For what works with each deployment type, refer to [Reference architecture](../reference-architecture.md).

1. Create an API key on the cluster that holds the data. Grant only read access to the indices that you want {{nightshift}} to search. For example, run this request in that cluster's **Console**:

   ```console
   POST /_security/api_key
   {
     "name": "nightshift-elasticsearch",
     "role_descriptors": {
       "nightshift_local_read": {
         "cluster": [],
         "indices": [
           {
             "names": ["logs-*", "metrics-*", "traces-*"],
             "privileges": ["read", "view_index_metadata"],
             "allow_restricted_indices": false
           }
         ]
       }
     }
   }
   ```

   Copy the `encoded` value from the response.

1. Find the cluster's {{es}} endpoint. In the [{{ecloud}} console](https://cloud.elastic.co/), open the project or deployment and copy its {{es}} endpoint (the `direct_endpoint`). Use the endpoint on port 443, without a port such as `:9243`.
1. In {{nightshift}}, on the **External Elasticsearch** card, select **Connect**, then **Create connector**.

   :::{image} ../../../images/nightshift-get-started-connect-menu.png
   :alt: The Connect menu, listing the Local Elasticsearch connector and the Create connector option
   :screenshot:
   :::

1. In the flyout, enter a **Connector name** and a **Connector ID**, for example `prod-logs`.
1. In **Elasticsearch URL**, paste the endpoint. Keep **Elasticsearch API key** selected, and paste the `encoded` value into **API Key**.
1. Keep the default **Actions**, and select **Save**.

   :::{image} ../../../images/nightshift-connector-elasticsearch.png
   :alt: The External Elasticsearch connector flyout with the connector name, Elasticsearch URL, API key, and actions
   :screenshot:
   :::

The card now shows one more connector. Select **Proceed**. For more options, refer to [External {{es}}](../investigation/set-up.md#nightshift-set-up-external-es).

:::{tip}
No data yet? Select **Add data** on the **Add data in 10+ other ways** card to send logs, metrics, and traces, for example with OpenTelemetry or {{agent}}. Refer to [Get started with {{obs-serverless}}](/solutions/observability/get-started.md).
:::
::::

::::{step} Connect other sources (optional)
:anchor: nightshift-get-started-other-sources

Your telemetry shows *what* is wrong; your code often shows *why*. Connect GitHub so investigations can read the code, configuration, Helm charts, and runbooks behind your services, and check what changed recently.

:::{image} ../../../images/nightshift-get-started-other-sources.png
:alt: The Connect other sources step, with the GitHub card and the Skip this step button
:screenshot:
:::

{{nightshift}} doesn't copy or index your repositories. Refer to [Your code](../cost-and-models.md#nightshift-data).

1. In GitHub, create a [fine-grained personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token), ideally on a bot or service account, so it keeps working when people change teams.

   - **Repository access**: select only the repositories that {{nightshift}} needs.
   - **Repository permissions**: give read-only access to **Contents**, **Metadata**, **Pull requests**, and **Issues**. A read-only token makes sure {{nightshift}} only reads.

   If your organization uses SAML single sign-on or requires approval for tokens, authorize or approve the token for the organization.
1. In {{nightshift}}, on the **GitHub** card, select **Connect**.
1. Enter a **Connector name** and a **Connector ID**. Leave **Receive events** turned off.
1. Under **Outbound**, select **Personal Access Token (PAT)** and paste your token. Don't use **OAuth 2.0 Authorization Code**: it stores per-user credentials, which the {{nightshift}} service account can't use.
1. Select **Save**.

:::{image} ../../../images/nightshift-connector-github.png
:alt: The GitHub connector flyout with the Inbound and Outbound authentication options
:screenshot:
:::

To skip GitHub, select **Skip this step**; you can add it later on the **Settings** page. To reach other tools over HTTP, refer to [Connect your data and tools](../investigation/set-up.md).
::::

::::{step} Try your first investigation
:anchor: nightshift-get-started-first-investigation

You don't need a problem in mind. {{nightshift}} looks at your data first and finds something worth investigating.

:::{image} ../../../images/nightshift-get-started-first-investigation.png
:alt: The Try first investigation step while Elastic nightshift gathers and triages signals
:screenshot:
:::

While the step shows **Gathering and triaging signals that can be investigated**, {{nightshift}} scans your recent data for error spikes, latency changes, and other trouble. After a couple of minutes, it suggests problems, each with a type, such as **Latency** or **Error spike**, a title, and the numbers behind it.

:::{image} ../../../images/nightshift-get-started-suggestions.png
:alt: A list of suggested investigations, each with a type such as Latency or Error spike, the evidence behind it, and an Investigate button, followed by an Ask your own question box
:screenshot:
:::

1. Pick a suggestion and select **Investigate**. If you already know what you want to look at, describe it in **Ask your own question** instead, for example "Why is checkout latency up?", and select **Investigate**.

   A card appears with **Agent is investigating**. This usually takes up to five minutes, and the checklist moves on while it runs.

   :::{image} ../../../images/nightshift-get-started-investigating.png
   :alt: The investigation card shows Agent is investigating while the Create first automation step is shown below
   :screenshot:
   :::

1. When the card shows **Investigation results are ready**, select **View results** and read the results. Refer to [Read an investigation](../investigation/index.md#nightshift-read-investigation).

   :::{image} ../../../images/nightshift-investigation-results.png
   :alt: The investigation flyout with the What's happened and Impact sections, including a chart of failed calls
   :screenshot:
   :::

1. Select **View hypothesis tree** to check the reasoning: every explanation that {{nightshift}} tested, with a confidence, confirmed or dismissed.

   :::{image} ../../../images/nightshift-hypothesis-tree.png
   :alt: The hypothesis tree, with the trigger at the top and four hypotheses below it, each with a confidence percentage
   :screenshot:
   :::

1. Review the proposed actions: make the change yourself and select **Mark as applied**, or select **Decline**.

   :::{image} ../../../images/nightshift-investigation-conclusion.png
   :alt: The Conclusion and Proposed actions sections of an investigation, with three actions that need review
   :screenshot:
   :::

Have a question? Select **Open chat** and ask, for example "How did you reach this conclusion?". For more, refer to [Investigate anything](../use-cases/investigate-anything.md).
::::

::::{step} Create your first automation
:anchor: nightshift-get-started-first-automation

An automation starts investigations for you, for example each time an alert fires or every morning at 09:00, and posts the results to a Slack channel.

1. In the **Create first automation** card, select **Create automation**.
1. Enter a **Name**, for example `Investigate critical alerts`.
1. Under **Trigger**, select **Add trigger**, then **Alert triggered**. Select **Any rule** and choose the rules, or a rule tag, that you want investigated.

   :::{image} ../../../images/nightshift-automation-create-trigger.png
   :alt: The Create automation flyout with the Add trigger menu open, listing Alert triggered, New message in channel, and Every…
   :screenshot:
   :::

1. Optional: Under **Actions**, select **Add action**, then **Post in Slack**, and pick a channel that an admin connected. Refer to [Slack](../investigation/set-up.md#nightshift-set-up-slack).
1. Select **Save and enable**.

The automation now investigates each matching alert, within the daily limits. In the checklist, select **Done**. Not ready? Select **Skip this step**. For a full example, refer to [Automatically investigate your alerts](../use-cases/auto-investigate-alerts.md).
::::

:::::

## Review what {{nightshift}} learned [nightshift-get-started-learned]

After your first investigation, {{nightshift}} has started a picture of your system: which services you run, which databases they use, and where their telemetry lives. Later investigations start from there. To review it, open the {icon}`boxes_vertical` menu on the home page and select **Knowledge**. The **Wiki** and **Memory** tabs hold what it learned.

:::{image} ../../../images/nightshift-knowledge-wiki.png
:alt: The Wiki tab on the Knowledge page, with pages for the postgres database, the inventory-api service, and the Elasticsearch telemetry cluster
:screenshot:
:::

Something wrong or out of date? Archive it so that {{nightshift}} stops using it. Refer to [How {{nightshift}} builds context](../context/index.md).

## What's next [nightshift-get-started-next]

Your home page now lists every investigation, grouped by severity. Refer to [The home page](../homepage.md).

:::{image} ../../../images/nightshift-home-after-setup.png
:alt: The Elastic nightshift home page after setup, with severity tiles and the first investigation listed under Medium
:screenshot:
:::

| I want to… | Go to |
| --- | --- |
| Find problems that none of my alerts catch | [Set up detection](./detection.md) |
| Ask {{nightshift}} about any problem, in my own words | [Investigate anything](../use-cases/investigate-anything.md) |
| Ask {{nightshift}} for help from a Slack channel | [Investigate in Slack](../use-cases/investigate-in-slack.md) |
| Find out why an alert fired | [Investigate your alerts](../use-cases/investigate-alerts.md) |
| Compare every use case | [What you can do with {{nightshift}}](../use-cases/index.md) |
