---
navigation_title: "Get started"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
    observability: unavailable
    security: unavailable
---

# Get started with {{agent-builder}}

Learn how to get started by enabling the {{agent-builder}} features and begin chatting with your data.

::::::{stepper}
::::{step} Set up an Elastic deployment

If you don't already have an Elastic deployment, refer to [Get started with search](/solutions/search/get-started.md).

:::{note}
For {{ech}} deployments, make sure you are using the solution navigation instead of classic navigation.
You can set up a new [space](/deploy-manage/manage-spaces.md) to use the solution nav.
:::

::::

:::::{step} Enable {{agent-builder}}

::::{applies-switch}

:::{applies-item} { "serverless": "preview", "elasticsearch" }

{{agent-builder}} is enabled by default in serverless {{es}} projects.

Find **Agents** in the navigation menu to begin using the feature, or search for **Agents** in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::

:::{applies-item} stack: preview 9.2

You have to enable {{agent-builder}} to get started on non-serverless deployments.

You can enable the features using the UI:

1. Search for **AI / Agent Builder** in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Toggle **{{agent-builder}}** to on.
3. Select **Save changes**.

Find **Agents** in the navigation menu to begin using the feature, or search for **Agents** in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::

::::

:::{note}
To learn about required privileges for {{agent-builder}}, refer to [Permissions and access control](permissions.md).
:::

:::::

::::{step} Ingest some data

Before you begin with agents, you need some data in {{es}}. Otherwise, you will be chatting to the underlying LLM without any retrieval-augmented context.

To learn about adding data for search use cases, go to [](/solutions/search/ingest-for-search.md).
For a broader overview of ingestion options, go to [](/manage-data/ingest.md).

:::{tip}
If you're not ready to add your own data, you can:
- Use the Elastic [sample data](/manage-data/ingest/sample-data.md).
- Generate synthetic financial data using [this Python tool](https://github.com/jeffvestal/synthetic-financial-data?tab=readme-ov-file#synthetic-financial-data-generator-).  (This requires your [{{es}} URL and an API key](/solutions/elasticsearch-solution-project/search-connection-details.md)).

% TODO: we can link to a an agent builder tutorial if we add one in the docs
:::

::::

::::{step} Begin chatting

The **Agent Chat** UI provides a conversational interface where you can interact with agents and explore your data using natural language. {{agent-builder}} includes a default agent named `Elastic AI Agent` with access to all built-in tools, so you can begin chatting immediately.

Learn more in [Agent Chat](chat.md).

::::

::::{step} Configure model (optional)

By default, {{agent-builder}} uses the Elastic Managed LLM. To use a different model, refer to [model selection and configuration](models.md).

::::

::::{step} Begin building agents and tools

Once you've tested the default **Elastic AI Agent** with the [built-in Elastic tools](tools.md), you can begin [building your own agents](agent-builder-agents.md#create-a-new-agent) with custom instructions and [creating your own tools](tools.md#create-custom-tools) to assign them.

::::

::::::
