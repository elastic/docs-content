---
navigation_title: Local installation (quickstart)
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/run-elasticsearch-locally.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
---

# Local development installation (quickstart) [run-elasticsearch-locally]

::::{warning}
**DO NOT USE THESE INSTRUCTIONS FOR PRODUCTION DEPLOYMENTS**

The instructions on this page are for **local development only**. Do not use this configuration for production deployments, because it is not secure. Refer to [deployment options](/get-started/deployment-options.md) for a list of production deployment options.
::::

Quickly set up {{es}} and {{kib}} in Docker for local development or testing, using this one-liner in the command line.

:::{info}
This setup comes with a one-month trial license that includes all Elastic features.
:::

## Prerequisites [local-dev-prerequisites]

* If you don’t have Docker installed, [download and install Docker Desktop](https://www.docker.com/products/docker-desktop) for your operating system.
* If you’re using Microsoft Windows, then install [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install).

## Step 1: Run `start-local` script [local-dev-quick-start]

To set up {{es}} and {{kib}} locally, run the `start-local` script in the command line:

```sh
curl -fsSL https://elastic.co/start-local | sh
```

After running the script, you can access Elastic services at the following endpoints:

* **{{es}}**: [http://localhost:9200](http://localhost:9200)
* **{{kib}}**: [http://localhost:5601](http://localhost:5601)

That's it! There's no step 2.

## Learn more [local-dev-additional-info]

For more detailed information about the `start-local` setup, refer to the [README on GitHub](https://github.com/elastic/start-local). Learn about customizing the setup, logging, and more.

## Next steps [local-dev-next-steps]

Use our [quick start guides](/solutions/elasticsearch-solution-project/get-started/quickstarts.md) to learn the basics of {{es}}.
