---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-getting-started-installing.html
---

# Install the add-on [ech-getting-started-installing]

These steps walk you through installing the Elasticsearch Add-On for Heroku from the Heroku CLI. You can either install the latest default version of the add-on or you can install a specific version and include plugins at the same time.


## Before you begin [echbefore_you_begin] 

The installation steps in this section assume that you have a basic working knowledge of the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) and are familiar with using the command line. To work with the Elasticsearch Add-On for Heroku from the command line, you need to have the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) already installed.

If you prefer to install the add-on through your web browser, go to the [Elasticsearch add-on](https://elements.heroku.com/addons/foundelasticsearch) page in the Elements Marketplace, select **Install Elasticsearch**, pick the add-on plan you want, and select **Provision add-on**.


## Steps [echsteps] 

To install the latest add-on for MY_APP using the Heroku CLI:

```bash
heroku addons:create foundelasticsearch --app MY_APP
```

After the Elasticsearch Add-On for Heroku gets added, you can find the canonical URL you use to access your newly provisioned cluster in the configuration for the app. Look for the `FOUNDELASTICSEARCH_URL` setting when you grep on the output of the `heroku config` command:

```bash
heroku config --app MY_APP | grep FOUNDELASTICSEARCH_URL
FOUNDELASTICSEARCH_URL: https://74f176887fdef36bb51e6e37nnnnnnnn.us-east-1.aws.found.io
```



