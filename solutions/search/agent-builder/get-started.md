---
applies_to:
  stack: preview 9.2
  deployment: 
    self: unavailable
  serverless:
    elasticsearch: preview
---

# Get started 

Learn how get started by enabling the {{agent-builder}} features and begin chatting with your data.

{{agent-builder}} is disabled by default. Follow these steps to enable the features and start using Chat.

:::::{stepper}
::::{step} Choose your deployment type

- **Option 1:** [{{es}} {{serverless-short}}](/solutions/search/serverless-elasticsearch-get-started.md)
- **Option 2:** [{{ech}}](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md)

:::{tip}
Not sure which deployment type to choose? Learn more in [Compare {{ech}} and {{serverless-short}}](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md).
:::

::::

::::{step} Enable features

Choose your preferred method to enable the {{agent-builder}} features.

::::{tab-set}

:::{tab-item} API
:sync: api

Run the following command in the Dev Tools [Console](/explore-analyze/query-filter/tools/console.md):

```console
POST kbn://internal/kibana/settings
{
   "changes": {
      "agentBuilder:enabled": true
   }
}
```

:::

:::{tab-item} {{ech}} UI
:sync: stack
```{applies_to}
serverless: unavailable
```

On {{ech}} deployments, you can also enable the features in **Advanced Settings**:

1. Access your Kibana settings through **Stack Management > Advanced Settings**.
2. Enable the `agentBuilder` settings:
```json
uiSettings.overrides:
  agentBuilder:enabled: true
```

:::

::::

::::

::::{step} Start chatting

Refresh the browser page and find **Chat/Conversations** in the navigation menu to start using the feature.
You can also search for **Chat** in the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md).

The Chat UI provides a conversational interface where you can interact with agents and explore your data using natural language. Learn more in [Conversations](conversations.md).

:::{note}
For {{ech}} deployments, make sure you are using the solution navigation instead of classic navigation.
You can set up a new [space](/deploy-manage/manage-spaces.md) to use the solution nav.
:::

::::
:::::
