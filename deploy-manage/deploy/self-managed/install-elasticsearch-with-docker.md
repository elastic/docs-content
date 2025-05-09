---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html
navigation_title: "Install with Docker"
applies_to:
  deployment:
    self:
---

# Install {{es}} with Docker [docker]

Docker images for {{es}} are available from the Elastic Docker registry. A list of all published Docker images and tags is available at [www.docker.elastic.co](https://www.docker.elastic.co). The source code is in [GitHub](https://github.com/elastic/elasticsearch/blob/master/distribution/docker).

:::{include} _snippets/trial.md
:::

::::{tip}
If you just want to test {{es}} in local development, refer to [Run {{es}} locally](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md). Note that this setup is not suitable for production environments.
::::

Review the following guides to install {{es}} with Docker:

* [](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-basic.md)
* [](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-compose.md)
* [](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-prod.md)
* [](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-configure.md)
