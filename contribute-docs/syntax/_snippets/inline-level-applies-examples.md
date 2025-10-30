::::::{dropdown} Basic example

:::::{tab-set}

::::{tab-item} Output

**Spaces** let you organize your content and users according to your needs.

- Each space has its own saved objects.
- {applies_to}`serverless: unavailable` Each space has its own navigation, called solution view.

::::

::::{tab-item} Markdown
```markdown
**Spaces** let you organize your content and users according to your needs.

- Each space has its own saved objects.
- {applies_to}`serverless: unavailable` Each space has its own navigation, called solution view.
```
::::

:::::

::::::

::::::{dropdown} Product-specific applicability with version information

This example shows how to use directly a key from the second level of the `applies_to` data structure, like `edot_python:`.

:::::{tab-set}

::::{tab-item} Output

- {applies_to}`edot_python: preview 1.7.0`
- {applies_to}`apm_agent_java: beta 1.0.0`

::::

::::{tab-item} Markdown
```markdown
- {applies_to}`edot_python: preview 1.7.0`
- {applies_to}`apm_agent_java: beta 1.0.0`
```
::::

:::::

::::::

::::::{dropdown} Multiple products and states in a single inline statement

:::::{tab-set}

::::{tab-item} Output

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.1.0`
- {applies_to}`edot_python: preview 1.7.0, ga 1.8.0` {applies_to}`apm_agent_java: beta 1.0.0, ga 1.2.0`
- {applies_to}`stack: ga 9.0` {applies_to}`eck: ga 3.0`

::::

::::{tab-item} Markdown
```markdown
- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.1.0`
- {applies_to}`edot_python: preview 1.7.0, ga 1.8.0` {applies_to}`apm_agent_java: beta 1.0.0, ga 1.2.0`
- {applies_to}`stack: ga 9.0` {applies_to}`eck: ga 3.0`
```
::::

:::::
::::::

::::::{dropdown} The functionality is available in the same lifecycle in multiple versions

:::::{tab-set}

::::{tab-item} Output

- {applies_to}`stack: ga 9.1.2` {applies_to}`stack: ga 9.0.6`

::::

::::{tab-item} Markdown
```markdown
- {applies_to}`stack: ga 9.1.2` {applies_to}`stack: ga 9.0.6`
```
::::

:::::
::::::