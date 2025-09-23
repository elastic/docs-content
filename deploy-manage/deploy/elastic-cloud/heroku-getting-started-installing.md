---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-getting-started-installing.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-getting-started-installing-version.html
applies_to:
  deployment:
    ess:
products:
  - id: cloud-hosted
---

# Install the add-on [ech-getting-started-installing]

These steps walk you through installing the {{heroku}} from the Heroku CLI. You can either install the latest default version of the add-on or you can install a specific version and include plugins at the same time.


## Before you begin [echbefore_you_begin]

The installation steps in this section assume that you have a basic working knowledge of the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) and are familiar with using the command line. To work with the {{heroku}} from the command line, you need to have the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) already installed.

If you prefer to install the add-on through your web browser, go to the [{{es}} add-on](https://elements.heroku.com/addons/foundelasticsearch) page in the Elements Marketplace, select **Install Elasticsearch**, pick the add-on plan you want, and select **Provision add-on**.


## Steps [echsteps]

To install the latest add-on for `MY_APP` using the Heroku CLI:

```bash
heroku addons:create foundelasticsearch --app MY_APP
```

After the {{heroku}} gets added, you can find the canonical URL you use to access your newly provisioned cluster in the configuration for the app. Look for the `FOUNDELASTICSEARCH_URL` setting when you grep on the output of the `heroku config` command:

```bash
heroku config --app MY_APP | grep FOUNDELASTICSEARCH_URL
FOUNDELASTICSEARCH_URL: <example-url>.aws.found.io
```

## Install a specific version and plugins [ech-getting-started-installing-version]

If you want your add-on to run a specific version of {{es}}, use the `--elasticsearch-version` parameter. We also provide many of the plugins that are available for {{es}}. You use the `--plugins` parameter to specify a comma-separated list of plugins that you want installed.

To find which {{es}} versions and plugins are currently available, you can omit the version to default to the latest one and add plugins later on from the [{{heroku}} console](https://cloud.elastic.co?page=docs&placement=docs-body). To use your own custom plugins, you can upload and select these plugins in the console as well.

For example: Install the add-on version {{version.stack}} and include the phonetic analysis plugin for  MY_APP:

```bash subs=true
heroku addons:create foundelasticsearch --elasticsearch-version {{version.stack}} --plugins analysis-phonetic --app MY_APP
```

After the add-on gets added, you can perform future version upgrades and plugin changes through the [console](heroku-getting-started-accessing.md).

## Next steps

- [](/deploy-manage/deploy/elastic-cloud/heroku-getting-started-accessing.md)
- [](/deploy-manage/deploy/elastic-cloud/heroku-working-with-elasticsearch.md)
- [](/deploy-manage/deploy/elastic-cloud/heroku.md#next-steps)

To learn how to remove the add-on, refer to [](/deploy-manage/deploy/elastic-cloud/heroku-getting-started-removing.md).