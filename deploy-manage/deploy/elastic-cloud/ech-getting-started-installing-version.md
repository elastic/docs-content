---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-getting-started-installing-version.html
---

# Install a specific version and plugins [ech-getting-started-installing-version]

If you want your add-on to run a specific version of Elasticsearch, use the `--elasticsearch-version` parameter. We also provide many of the plugins that are available for Elasticsearch. You use the `--plugins` parameter to specify a comma-separated list of plugins that you want installed.

To find which Elasticsearch versions and plugins are currently available, you can omit the version to default to the latest one and add plugins later on from the [Elasticsearch Add-On for Heroku console](https://cloud.elastic.co?page=docs&placement=docs-body). To use your own custom plugins, you can upload and select these plugins in the console as well.

For example: Install the add-on version 6.8.23 and include the phonetic analysis plugin for  MY_APP:

```term
heroku addons:create foundelasticsearch --elasticsearch-version 6.8.23 --plugins analysis-phonetic --app MY_APP
```

After the add-on gets added, you can perform future version upgrades and plugin changes through the [console](ech-getting-started-accessing.md).

