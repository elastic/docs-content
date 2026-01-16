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

They ensure that only authorized users or applications interact with these resources through [Elastic APIs]({{apis}}).

For example, if you extract data from an {{es}} cluster on a daily basis, you might create an API key tied to your credentials, configure it with minimum access, and then put the API credentials into a cron job. Or you might create API keys to automate ingestion of new data from remote sources, without a live user interaction.

Depending on the APIs you want to use, the API keys to create are different, and managed at different locations:

| Type | Applicability | Purpose | 
| --- | --- | --- |
| [](api-keys/elasticsearch-api-keys.md) | {applies_to}`stack: ga` | • Use [{{es}}]({{es-apis}}) and [{{kib}}]({{kib-apis}}) APIs in stack-versioned deployments, including ECH, ECE, ECK, and self-managed clusters.<br><br>• Manage remote cluster connections. |
| [](api-keys/serverless-project-api-keys.md) | {applies_to}`serverless: ga`| Use [{{es}} {{serverless-short}}]({{es-serverless-apis}}) and [{{kib}} {{serverless-short}}]({{kib-serverless-apis}}) APIs. |
| [](api-keys/elastic-cloud-api-keys.md) | {applies_to}`ess: ga` {applies_to}`serverless: ga` | • Manage your {{ecloud}} organization, {{ech}} deployments, and {{serverless-short}} projects using the [{{ecloud}}]({{cloud-apis}}) and [{{ecloud}} {{serverless-short}}]({{cloud-serverless-apis}}) APIs.<br><br>• {applies_to}`serverless: ga` Use [{{es}} {{serverless-short}}]({{es-serverless-apis}}) and [{{kib}} {{serverless-short}}]({{kib-serverless-apis}}) APIs. Using {{ecloud}} keys for project-level API access allows you to create keys that can interact with multiple projects,and manage API access centrally from the {{ecloud}} console. |
|[](api-keys/elastic-cloud-enterprise-api-keys.md) | {applies_to}`ece: ga` | Manage your {{ece}} platform and deployments using the [{{ece}}]({{ece-apis}}) API. |