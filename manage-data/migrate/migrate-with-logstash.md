---
navigation_title: Migrate with {{ls}}
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

# Migrate data with {{ls}} [migrate-with-ls]

You can use {{ls}} to migrate data from an {{ech}} deployment to an {{serverless-full}} project. 

The Logstash input has cursor like-functionality that keeps your place. 

[Tracking a field's value across runs](https://www.elastic.co/docs/reference/logstash/plugins/plugins-inputs-elasticsearch)

Familiarity with {{ech}}, {{es}}, and {{ls}} is helpful, but not required. 

:::{note}
This guide focuses on data migration. Dashboards, visualizations, pipelines, templates, and other {{kib}} assets must be migrated separately using the {{kib}} [export/import APIs](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-saved-objects) or recreated manually.
:::

## Prerequisites [migrate-prereqs]

Ensure that you have:

- {{ech}} deployment with data to migrate
- {{serverless-full}} project configured and running
- {{ls}} [installed](https://www.elastic.co/downloads/logstash) on your local machine or server 
- API keys in {{ls}} format for authentication with both deployments


## Process overview [migration-overview]
* [Configure {{ls}}](#configure-ls)
* [Run {{ls}}](#run-ls)
* [Verify data migration](#verify-migration)



## Step 1: Configure {{ls}} [configure-ls]
Create a new {{ls}} configuration file (migration.conf) with these settings:

```
input {
  elasticsearch {
    cloud_id => "<HOSTED_DEPLOYMENT_CLOUD_ID>"  # Your Hosted Deployment's Cloud ID
    api_key  => "<HOSTED_API_KEY>"              # Your Hosted Deployment API key
    index    => "index_pattern*"                # Your index or pattern (such as logs-*,metrics-*)
    docinfo  => true
  }
}

output {
  elasticsearch {
    hosts       => [ "https://<SERVERLESS_HOST_URL>:443" ] # URL for your Serverless project URL, set port as 443
    api_key     => "<SERVERLESS_API_KEY>"                  # API key (in Logstash format) for your Serverless project
    ssl_enabled => true
    index       => "%{[@metadata][input][elasticsearch][_index]}" # Retain original index names
  }

  stdout { codec => rubydebug { metadata => true } }
}
```

When you create an API key for Logstash, be sure to select **Logstash** from the **API key** format dropdown. This option formats the API key in the correct `id:api_key` format required by Logstash.


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





:::{tip}
To migrate multiple indexes at the same time, use a wildcard in the index name. 
For example, `index => "logs-*"` migrates all indices starting with `logs-`.
:::



## More resources [more-resources]
* https://www.elastic.co/docs/reference/logstash/plugins/plugins-inputs-elasticsearch
* https://www.elastic.co/docs/reference/logstash/plugins/plugins-inputs-elasticsearch#plugins-inputs-elasticsearch-cursor
* [API key in LS format](https://www.elastic.co/docs/reference/logstash/connecting-to-serverless#api-key)




## FAQ 

ToDo @karenzone:  Continue with FAQ


