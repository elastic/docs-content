---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/data-views.html
  - https://www.elastic.co/guide/en/serverless/current/data-views.html
  - https://www.elastic.co/guide/en/kibana/current/managing-data-views.html
description: A Kibana data view selects Elasticsearch indices, data streams, or aliases for Discover, Lens, and other analytics features. Create one yourself, or use one created automatically or managed by Elastic.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
---

# Data views [data-views]

A {{data-source}} tells {{kib}} which {{es}} indices, [data streams](../../manage-data/data-store/data-streams.md), or [index aliases](/manage-data/data-store/aliases.md) to query. Analytics features such as **Discover** and **Lens** use a {{data-source}} to access your data. For example, a {{data-source}} can point to your log data from yesterday, or to all indices that contain your data.

::::{note}
In some apps, you can query {{es}} with [{{esql}}](elasticsearch://reference/query-languages/esql.md) instead. {{esql}} doesn't require a {{data-source}}.
::::

## How data views are created [data-views-how-you-get-one]

A {{data-source}} in your space is created automatically or by you.

**Created automatically**
:   Some ingest and onboarding workflows create a {{data-source}} for you. Adding [sample data](../../manage-data/ingest/sample-data.md) installs one. [Uploading a file](../../manage-data/ingest/upload-data-files.md) creates one when **Create data view** is turned on. These are ordinary {{data-sources}} that you can edit.

    Installing an Elastic integration through Fleet also creates {{data-sources}}. Those {{data-sources}} are [managed by Elastic](#managed-data-views).

**Created by you**
:   For your own data, you often need to create the {{data-source}} yourself. Refer to [Create a data view](data-views/create-data-view.md).

To see which {{data-sources}} already exist in your space, open the data view menu in **Discover** or **Lens**, or go to the **Data Views** management page.

## Managed data views [managed-data-views]

Some {{data-sources}} are configured and managed by Elastic, including those created by Fleet integrations, {{elastic-sec}}, and Cases. Managed {{data-sources}} carry a **Managed** tag.

You can view and use a managed {{data-source}}, but you can't edit it.

{applies_to}`stack: ga 9.4` You also can't delete a managed {{data-source}}.

To customize a managed {{data-source}}, [duplicate it](data-views/duplicate-data-view.md) and edit the copy.

## Search across clusters, projects, or rolled-up data [management-cross-cluster-search]

To point a {{data-source}} at another cluster, another project, or a rollup index, refer to [Data view search syntax](data-views/data-view-search-syntax.md).

## Work with data views

* [Create a data view](data-views/create-data-view.md)
* [Delete a data view](data-views/delete-data-view.md)
* [Duplicate a data view](data-views/duplicate-data-view.md)
* [Customize data view fields](data-views/customize-data-view-fields.md)
* [Data view search syntax](data-views/data-view-search-syntax.md)
