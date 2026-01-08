:::::::{tab-set}

::::::{tab-item} {{fleet}}-managed or {{apm-server}} binary

To create an {{apm-agent}} key:

1. In {{kib}}, find **Applications** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select any **Applications** page. 
3. Go to **Settings** > **Agent keys**.
4. Select **Create {{apm-agent}} key**.
5. Enter a name for your API key.
6. Assign at least one privilege:
   - **Ingest** (`event:write`): Required to ingest agent events.
   - **Agent configuration** (`config_agent:read`): Required to use agent central configuration for remote configuration.
7. Select **Create {{apm-agent}} key**.
8. Copy the API key now. You won't be able to view it again.

:::{image} /solutions/images/observability-apm-ui-api-key.png
:alt: {{apm-agent}} key creation
:screenshot:
:::

::::::

::::::{tab-item} {{serverless-full}}

To create an {{apm-agent}} key:

1. In your {{obs-serverless}} project, go to any **Applications** page.
2. Select **Settings** > **Agent keys**.
3. Select **Create {{apm-agent}} key**.
4. Enter a name for your API key.
5. Assign at least one privilege:
   - **Ingest** (`event:write`): Required to ingest agent events.
   - **Agent configuration** (`config_agent:read`): Required to use agent central configuration for remote configuration.
6. Select **Create {{apm-agent}} key**.
7. Copy the API key now. You won't be able to view it again. API keys do not expire.

:::{image} /solutions/images/observability-apm-ui-api-key-serverless.png
:alt: {{apm-agent}} key creation
:screenshot:
:::

::::::

:::::::
