---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/data-views.html
  - https://www.elastic.co/guide/en/serverless/current/data-views.html
  - https://www.elastic.co/guide/en/kibana/current/managing-data-views.html
description: Learn what a Kibana data view is, the three ways you end up with one, and where to go to create, delete, duplicate, or customize one.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
---

# Data views [data-views]

By default, analytics features such as Discover require a {{data-source}} to access the {{es}} data that you want to explore. A {{data-source}} can point to one or more indices, [data streams](../../manage-data/data-store/data-streams.md), or [index aliases](/manage-data/data-store/aliases.md). For example, a {{data-source}} can point to your log data from yesterday, or all indices that contain your data.

::::{note}
In certain apps, you can also query your {{es}} data using [{{esql}}](elasticsearch://reference/query-languages/esql.md). With {{esql}}, data views aren't required.
::::

## How you end up with a data view [data-views-how-you-get-one]

There are three ways a {{data-source}} ends up in your space:

* **Created for you** — Some workflows create a {{data-source}} automatically. Adding [sample data](../../manage-data/ingest/sample-data.md), [uploading a file](../../manage-data/ingest/upload-data-files.md), and running some {{ml}} [data frame analytics](../machine-learning/data-frame-analytics.md) jobs each create one for you, ready to use in Discover and Lens. These are ordinary {{data-sources}} that you can edit like any other. Installing an Elastic integration through Fleet also creates {{data-sources}} for you, but those are managed by Elastic (see below).
* **Created by you** — For your own data, you often need to create the {{data-source}} yourself. Refer to [Create a data view](data-views/create-data-view.md).
* **Managed by Elastic** — Some {{data-sources}} are configured and managed by Elastic, for example by Fleet integrations, {{elastic-sec}}, and Cases. Managed {{data-sources}} carry a **Managed** tag. You can view and use them, but you can't edit them, and {applies_to}`stack: ga 9.4` you can't delete them either. If you'd like to use a modified version of a managed {{data-source}}, [duplicate it](data-views/duplicate-data-view.md) and edit the copy instead.

Not sure whether you already have one? Open the data view menu in **Discover** or **Lens**, or go to the **Data Views** management page: both list every {{data-source}} available in your space.

## Search across clusters, projects, or rolled-up data [management-cross-cluster-search]

To point a data view at another cluster, another project, or a rollup index, refer to [Data view search syntax](data-views/data-view-search-syntax.md).

## Manage your data views

* [Create a data view](data-views/create-data-view.md)
* [Delete a data view](data-views/delete-data-view.md)
* [Duplicate a data view](data-views/duplicate-data-view.md)
* [Customize data view fields](data-views/customize-data-view-fields.md) — add runtime or scripted fields, and change how fields are formatted
