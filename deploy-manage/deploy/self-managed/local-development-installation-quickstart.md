---
navigation_title: "Run {{es}} locally"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/run-elasticsearch-locally.html
---



# Local development installation (quickstart) [run-elasticsearch-locally]


::::{warning}
**DO NOT USE THESE INSTRUCTIONS FOR PRODUCTION DEPLOYMENTS**

The instructions on this page are for **local development only**. Do not use this configuration for production deployments, because it is not secure. Refer to [deployment options](../../../get-started/deployment-options.md) for a list of production deployment options.

::::


Quickly set up {{es}} and {{kib}} in Docker for local development or testing, using the [`start-local` script](https://github.com/elastic/start-local?tab=readme-ov-file#-try-elasticsearch-and-kibana-locally).

This setup comes with a one-month trial license that includes all Elastic features. After the trial period, the license reverts to **Free and open - Basic**. Refer to [Elastic subscriptions](https://www.elastic.co/subscriptions) for more information.


## Prerequisites [local-dev-prerequisites]

* If you don’t have Docker installed, [download and install Docker Desktop](https://www.docker.com/products/docker-desktop) for your operating system.
* If you’re using Microsoft Windows, then install [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install).


## Run `start-local` [local-dev-quick-start]

To set up {{es}} and {{kib}} locally, run the `start-local` script:

```sh
curl -fsSL https://elastic.co/start-local | sh
```
%  NOTCONSOLE

This script creates an `elastic-start-local` folder containing configuration files and starts both {{es}} and {{kib}} using Docker.

After running the script, you can access Elastic services at the following endpoints:

* **{{es}}**: [http://localhost:9200](http://localhost:9200)
* **{{kib}}**: [http://localhost:5601](http://localhost:5601)

The script generates a random password for the `elastic` user, and an API key, stored in the `.env` file.

::::{warning}
This setup is for local testing only. HTTPS is disabled, and Basic authentication is used for {{es}}. For security, {{es}} and {{kib}} are accessible only through `localhost`.

::::



## Learn more [local-dev-additional-info]

For more detailed information about the `start-local` setup, refer to the [README on GitHub](https://github.com/elastic/start-local). Learn about customizing the setup, logging, and more.


## Next steps [local-dev-next-steps]

Use our [quick start guides](https://www.elastic.co/guide/en/elasticsearch/reference/current/quickstart.html) to learn the basics of {{es}}.
