---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-getting-started-accessing.html
applies_to:
  deployment:
    ess:
---

# Access the console [ech-getting-started-accessing]

You use the console to manage your cluster from a web browser. Tasks that are available from the console include upgrading versions, configuring security features, working with custom plugins, and more.

:::{image} /deploy-manage/images/cloud-heroku-ech-console.png
:alt: [{{es}} Add-On for Heroku console](https://cloud.elastic.co?page=docs&placement=docs-body)
:::

To access the console in a browser from the Heroku CLI:

```bash
heroku addons:open foundelasticsearch --app MY_APP
Opening https://addons-sso.heroku.com/apps/e286f875-cbdb-47a9-b445-e94bnnnnnnnn/addons/9b883e93-3db3-4491-b620-c3dfnnnnnnnn...
```

Alternatively, you can access the console by visiting the [Heroku Dashboard](https://dashboard.heroku.com/), selecting your app, and opening the {{es}} link.


To learn how to access {{kib}}, refer to [](/deploy-manage/deploy/elastic-cloud/access-kibana.md).