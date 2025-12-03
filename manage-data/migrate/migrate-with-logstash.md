---
navigation_title: Migrate Elastic Cloud Hosted data to Serverless with Logstash
applies_to:
  stack: ga
  deployment:
    ess: ga
    ece: ga
products:
  - id: elasticsearch
  - id: logstash
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
---

# Migrate {{ech}} data to {{serverless-full}} with {{ls}} [migrate-with-ls]

You can use {{ls}} to migrate data from an {{ech}} deployment to an {{serverless-full}} project. 
Familiarity with {{ech}}, {{es}}, and {{ls}} is helpful, but not required. 

:::{admonition} Basic migration
This guide focuses on a basic data migration scenario for moving static data from an {{ech}} deployment to a {{serverless-full}} project. Dashboards, visualizations, pipelines, templates, and other {{kib}} assets must be migrated separately using the {{kib}} [export/import APIs](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-saved-objects) or recreated manually.
:::

:::{admonition} Advanced migration
:applies_to: stack: preview

{{ls}} can handle more advanced migrations with field tracking settings in the [Elasticsearch input](https://www.elastic.co/docs/reference/logstash/plugins/plugins-inputs-elasticsearch) plugin. The field tracking feature adds cursor-like pagination functionality that can support more complex migrations and ongoing data migration over time.

More information is available in the Elasticsearch input plugin documentation: [Tracking a field's value across runs](https://www.elastic.co/docs/reference/logstash/plugins/plugins-inputs-elasticsearch#plugins-inputs-elasticsearch-cursor).
:::

## Prerequisites [migrate-prereqs]

- {{ech}} deployment with data to migrate
- [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md) project configured and running
- {{ls}} [installed](https://www.elastic.co/downloads/logstash) on your local machine or server 
- API keys in {{ls}} format for authentication with both deployments


## Process overview [migration-overview]
* [Configure {{ls}}](#configure-ls)
* [Run {{ls}}](#run-ls)
* [Verify data migration](#verify-migration)


## Step 1: Configure {{ls}} [configure-ls]
Create a new {{ls}} [pipeline configuration file](logstash://reference/creating-logstash-pipeline.md) (_migration.conf_) with these settings:

```
input {
  elasticsearch {
    cloud_id => "<HOSTED_DEPLOYMENT_CLOUD_ID>"  # Your Hosted deployment's Cloud ID
    api_key  => "<HOSTED_API_KEY>"              # Your Hosted deployment API key
    index    => "index_pattern*"                # Your index or pattern (such as logs-*,metrics-*)
    docinfo  => true
  }
}

output {
  elasticsearch {
    hosts       => [ "https://<SERVERLESS_HOST_URL>:443" ] # URL for your Serverless project URL, set port as 443
    api_key     => "<SERVERLESS_API_KEY>"                  # API key (in Logstash format) for your Serverless project
    ssl_enabled => true
    index       => "%{[@metadata][input][elasticsearch][_index]}" # Instruction to retain original index names
  }

  stdout { codec => rubydebug { metadata => true } }
}
```

:::{admonition} Tips

- When you create an [API key for {{ls}}](logstash://reference/connecting-to-serverless.md#api-key), be sure to select **Logstash** from the **API key** format dropdown. This option formats the API key in the correct `id:api_key` format required by {{ls}}.

- To migrate multiple indexes at the same time, use a wildcard in the index name. 
For example, `index => "logs-*"` migrates all indices starting with `logs-`.
:::

## Step 2: Run {{ls}} [run-ls]
 
Start {{ls}}:

```
bin/logstash -f migration.conf
```

## Step 3: Verify data migration [verify-migration]

After running {{ls}}, verify that the data has been successfully migrated:

1. Log in to your {{serverless-full}} project.
2. Navigate to Index Management and select the index.
3. Verify that the migrated data is visible.

