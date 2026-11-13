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

By the end, {{nightshift}} has investigated a real problem in your data and learned the first things about your system. Before you start, check the [requirements](../get-started.md#nightshift-get-started-requirements).

:::::{stepper}

::::{step} Enable {{nightshift}}
:anchor: nightshift-get-started-enable

From the {{nightshift}} home page, an admin needs to select **Enable {{nightshift}}**.  If you don't see an **Enable {{nightshift}}** button, ask an admin to do this step.

{{nightshift}} runs every investigation as a service account. Refer to [Privileges that {{nightshift}} runs with](./privileges.md#nightshift-privileges-accounts).

::::

::::{step} Add data
:anchor: nightshift-get-started-add-data

Choose the {{es}} data that investigations query.

**If your data is in this project**: <br> {{nightshift}} automatically creates a **Local {{es}}** connector that can read your `logs-*`, `metrics-*`, and `traces-*` data. The **External Elasticsearch** card shows a **1 connector** badge. Select **Proceed**.

**If your data is in another cluster or project**: <br> Add an External {{es}} connector. You need this only when [{{cps}}](/deploy-manage/cross-project-search-config.md) can't access that data. For what works with each deployment type, refer to [Reference architecture](../reference-architecture.md).

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
1. From {{nightshift}}, on the **External Elasticsearch** card, select **Connect** → **Create connector**.
1. Enter a **Connector name** and a **Connector ID**, for example `prod-logs`.
1. In **Elasticsearch URL**, add the endpoint.
1. In **API Key**, add the `encoded` value you generated previously.
1. Keep the default **Actions**, and select **Save**.

The badge on the **External {{es}}** card should show one more connector. Select **Proceed**. For more options, refer to [External {{es}}](../investigation/set-up.md#nightshift-set-up-external-es).

:::{tip}
No data yet? Select **Add data** on the **Add data in 10+ other ways** card to send logs, metrics, and traces, for example with OpenTelemetry or {{agent}}. Refer to [Get started with {{obs-serverless}}](/solutions/observability/get-started.md).
:::
::::

::::{step} Connect other sources (optional)
:anchor: nightshift-get-started-other-sources

Your telemetry shows *what* is wrong, but your code often shows *why*. Connect GitHub so investigations can read the code, configuration, Helm charts, and runbooks behind your services, and check recent changes.

{{nightshift}} doesn't copy or index your repositories. Refer to [Your code](../cost-and-models.md#nightshift-data).

1. In GitHub, create a [fine-grained personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token), ideally on a bot or service account, so it keeps working when people change teams.

   - **Repository access**: select only the repositories that {{nightshift}} needs.
   - **Repository permissions**: give read-only access to **Contents**, **Metadata**, **Pull requests**, and **Issues**.

   If your organization uses SAML single sign-on or requires approval for tokens, authorize or approve the token for the organization.
1. From {{nightshift}}, on the **GitHub** card, select **Connect**.
1. Enter a **Connector name** and a **Connector ID**. Leave **Receive events** turned off.
1. Under **Outbound**, select **Personal Access Token (PAT)** and paste your token. Don't use **OAuth 2.0 Authorization Code** because it stores per-user credentials, which the {{nightshift}} service account can't use.
1. Select **Save**.

To skip GitHub setup, select **Skip this step**. You can add it later on the **Settings** page. To reach other tools over HTTP, refer to [Connect your data and tools](../investigation/set-up.md).
::::

::::{step} Try your first investigation
:anchor: nightshift-get-started-first-investigation

You don't need a problem in mind. {{nightshift}} looks at your data first and finds something worth investigating.

{{nightshift}} shows **Gathering and triaging signals that can be investigated** while it scans your recent data for error spikes, latency changes, and other potential issues. After a couple of minutes, it suggests problems, each with a type, such as **Latency** or **Error spike**, a title, and the numbers behind it.

1. Pick a suggestion and select **Investigate**. You can also **Ask your own question** at the end of the list of suggestions, for example "Why is checkout latency up?", and select **Investigate**.

   {{nightshift}} shows **Agent is investigating**.

1. When **Investigation results are ready**, select **View results** and review the results. Refer to [Read an investigation](../investigation/index.md#nightshift-read-investigation).
1. Select **View hypothesis tree** to check the reasoning: every explanation that {{nightshift}} tested, with a confidence, confirmed or dismissed.
1. Review the proposed actions: make the change yourself and select **Mark as applied**, or select **Decline**.

To ask more questions, select **Open chat** from the investigation results. For example, you could ask "How did you reach this conclusion?". For more, refer to [Investigate anything](../use-cases/investigate-anything.md).
::::

::::{step} Create your first automation
:anchor: nightshift-get-started-first-automation

An automation starts investigations for you. For example, you could have an investigation start each time an alert fires or every morning at 09:00, and post the results to a Slack channel.

1. Under **Create first automation**, select **Create automation**.
1. Enter a **Name**, for example `Investigate critical alerts`.
1. Under **Trigger**, select **Add trigger**.
1. Under **Elastic**, select **Alert triggered**. Select **Any rule** and choose the rules, or a rule tag, that you want investigated.
1. Optional: Under **Actions**, select **Add action**, then **Post in Slack**, and pick a channel that an admin has connected. Refer to [Set up Slack](../investigation/set-up.md#nightshift-set-up-slack).
1. Select **Save and enable**.

The automation now investigates each matching alert, within the daily limits. In the checklist, select **Done**. Not ready? Select **Skip this step**. For a full example, refer to [Automatically investigate your alerts](../use-cases/auto-investigate-alerts.md).
::::

:::::

## Review what {{nightshift}} learned [nightshift-get-started-learned]

After your first investigation, {{nightshift}} has started a picture of your system: which services you run, which databases they use, and where their telemetry lives. Later investigations start from there. To review this context, open the {icon}`boxes_vertical` menu on the home page and select **Knowledge**. Review the **Wiki** and **Memory** tabs to see what it's learned.

If any of the Wikie or Memory articles are outdated, archive them so {{nightshift}} stops using them. Refer to [How {{nightshift}} builds context](../context/index.md).

## What's next [nightshift-get-started-next]

Your home page now lists every investigation, grouped by severity. Refer to [The home page](../homepage.md).

Review the following next steps:

- [Set up detection](./detection.md): Find problems that none of your alerts catch.
- [Investigate anything](../use-cases/investigate-anything.md): Ask {{nightshift}} about any problem, in your own words.
- [Investigate in Slack](../use-cases/investigate-in-slack.md): Ask {{nightshift}} for help from a Slack channel.
- [Investigate your alerts](../use-cases/investigate-alerts.md): Find out why an alert fired.
- [What you can do with {{nightshift}}](../use-cases/index.md): Compare every use case.
