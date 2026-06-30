To create an {{apm-agent}} key:

1. In {{kib}}, find **Applications** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select any **Applications** page. 
3. Go to **Settings** > **Agent keys**.
4. Select **Create {{apm-agent}} key**.
5. Enter a name for your API key.
6. Assign at least one privilege:
   - **Agent configuration** (`config_agent:read`): Required to use agent central configuration for remote configuration.
   - **Ingest** (`event:write`): Required to ingest agent events.
7. Select **Create {{apm-agent}} key**.
8. Copy the API key now. The key is shown only once.

:::{note}
API keys do not expire.
:::

:::{image} /solutions/images/observability-apm-ui-api-key.png
:alt: {{apm-agent}} key creation
:screenshot:
:::