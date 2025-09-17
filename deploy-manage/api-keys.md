---
applies_to:
  deployment:
    eck: ga
    ess: ga
    ece: ga
    self: ga
  serverless: ga
navigation_title: API keys
---

# Elastic API keys

API keys are security mechanisms used to authenticate and authorize access to your deployments and {{es}} resources. 

They ensure that only authorized users or applications interact with these resources through [Elastic APIs](https://www.elastic.co/docs/api/).

For example, if you extract data from an {{es}} cluster on a daily basis, you might create an API key tied to your credentials, configure it with minimum access, and then put the API credentials into a cron job. Or you might create API keys to automate ingestion of new data from remote sources, without a live user interaction.

Depending on the APIs you want to use, the API keys to create are different, and managed at different locations:

- **[](api-keys/elasticsearch-api-keys.md)**, to use [{{es}}](https://www.elastic.co/docs/api/doc/elasticsearch/) and [{{kib}}](https://www.elastic.co/docs/api/doc/kibana/) APIs, and to manage remote cluster connections.
- **[](api-keys/serverless-project-api-keys.md)**, to use [{{es}}](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/) and [{{kib}}](https://www.elastic.co/docs/api/doc/serverless/) serverless APIs.
- **[](api-keys/elastic-cloud-api-keys.md)**, to manage your {{ecloud}} organization, {{ech}} deployments, and serverless projects using the [{{ecloud}}](https://www.elastic.co/docs/api/doc/cloud/) and [{{ecloud}} serverless](https://www.elastic.co/docs/api/doc/elastic-cloud-serverless/) APIs.
- **[](api-keys/elastic-cloud-enterprise-api-keys.md)**, to manage your {{ece}} platform and deployments using the [{{ece}}](https://www.elastic.co/docs/api/doc/cloud-enterprise/) API.