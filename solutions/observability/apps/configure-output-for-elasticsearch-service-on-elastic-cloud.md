---
navigation_title: "{{ech}}"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-configure-cloud-id.html
applies_to:
  stack: all
---



# Configure the output for {{ech}} [apm-configure-cloud-id]


::::{note}
![supported deployment methods](../../../images/observability-binary-yes-fm-no.svg "")

This documentation only applies to APM Server binary users.

::::


::::{note}
This page refers to using a separate instance of APM Server with an existing [{{ech}} deployment](https://www.elastic.co/cloud/elasticsearch-service?page=docs&placement=docs-body). If you want to use APM on {{ech}}, see: [Create your deployment](../../../deploy-manage/deploy/elastic-cloud/create-an-elastic-cloud-hosted-deployment.md) and [Add APM user settings](configure-apm-server.md).
::::


APM Server comes with two settings that simplify the output configuration when used together with [{{ech}}](https://www.elastic.co/cloud/elasticsearch-service?page=docs&placement=docs-body). When defined, these setting overwrite settings from other parts in the configuration.

Example:

```yaml
cloud.id: "staging:dXMtZWFzdC0xLmF3cy5mb3VuZC5pbyRjZWM2ZjI2MWE3NGJmMjRjZTMzYmI4ODExYjg0Mjk0ZiRjNmMyY2E2ZDA0MjI0OWFmMGNjN2Q3YTllOTYyNTc0Mw=="
cloud.auth: "elastic:{pwd}"
```

These settings can be also specified at the command line, like this:

```sh
apm-server -e -E cloud.id="<cloud-id>" -E cloud.auth="<cloud.auth>"
```


## `cloud.id` [_cloud_id]

The Cloud ID, which can be found in the {{ecloud}} Console, is used by APM Server to resolve the {{es}} and {{kib}} URLs. This setting overwrites the `output.elasticsearch.hosts` and `setup.kibana.host` settings.


## `cloud.auth` [_cloud_auth]

When specified, the `cloud.auth` overwrites the `output.elasticsearch.username` and `output.elasticsearch.password` settings. Because the {{kib}} settings inherit the username and password from the {{es}} output, this can also be used to set the `setup.kibana.username` and `setup.kibana.password` options.

