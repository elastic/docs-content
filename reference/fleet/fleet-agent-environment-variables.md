---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-agent-environment-variables.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Set environment variables in an Elastic Agent policy [fleet-agent-environment-variables]

As an advanced use case, you may wish to configure environment variables in your {{agent}} policy. This is useful, for example, if there are configuration details about the system on which {{agent}} is running that you may not know in advance. As a solution, you may want to configure environment variables to be interpreted by {{agent}} at runtime, using information from the running environment.

For {{fleet}}-managed {{agents}}, you can configure environment variables using the [Env Provider](/reference/fleet/env-provider.md). Refer to [Variables and conditions in input configurations](/reference/fleet/dynamic-input-configuration.md) in the standalone {{agent}} documentation for more detail.

