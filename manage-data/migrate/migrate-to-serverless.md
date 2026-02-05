---
navigation_title: Migrate {{ech}} data to {{serverless-short}}
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-migrate-data-internal.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-migrate-data-internal.html
applies_to:
  serverless:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Migrate {{ech}} data to {{serverless-full}} [migrate-to-serverless]

You might currently be using ECH and want to switch to {{serverless-short}}. To better understand the differences between these offerings, refer to [Compare {{ech}} and {{serverless-short}}](/deploy-manage/deploy/elastic-cloud/differences-from-other-elasticsearch-offerings.md).

To make the change, you first need to [create a {{serverless-short}} project](/deploy-manage/deploy/elastic-cloud/create-serverless-project.md). Once the new project is set up, you're ready to migrate your data.

There are two approaches to migrating ECH data into {{serverless-short}}:

 - [Migrate with the reindex API](/manage-data/migrate/migrate-with-reindex-api.md): The [reindex API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) is a built-in component of {{es}}. You can use it to migrate your data from source indices, aliases, or data streams, and optionally to filter and transform documents as they are ingested into the target cluster. {applies_to}`serverless: preview`

 - [Migrate with {{ls}}](/manage-data/migrate/migrate-with-logstash.md): [{{ls}}](logstash://reference/index.md) is a separately installable {{es}} product that, with its {{es}} input and {{es}} output plugins, allows for various advanced configuration options during data migration. For example, you can control how many documents are retrieved in a single HTTP request, enable parallel reads from the source index, or track documents fields in order to resume data migration in the event that {{ls}} needs to be restarted.
