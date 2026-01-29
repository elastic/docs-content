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

There are two approaches to migrating your {{ech}} data to {{serverless-full}}:

 - [Migrate with the reindex API](/manage-data/migrate/migrate-with-reindex-api.md) - Using this more straightforward approach, you can migrate your data with the various features available in the [reindex API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex), including the ability to run and control indexing, and to filter and transform documents as they are ingested into the target cluster. {applies_to}`serverless: preview`

 - [Migrate with {{ls}}](/manage-data/migrate/migrate-with-logstash.md) - Using {{ls}} with the {{es}} input and {{es}} output plugins you can take advantage of the various advanced configuration options, such as controlling how many documents are retrieved per scroll, enabling parallel reads from the source index, and the ability to track fields and resume migration after a {{ls}} restart. 

