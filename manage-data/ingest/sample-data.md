---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/sample-data.html
  - https://www.elastic.co/guide/en/kibana/current/connect-to-elasticsearch.html#_add_sample_data
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Sample data

Using sample data is a great way to start exploring the system and learn your way around. There are a few ways to easily ingest sample data into {{es}}.

## Add sample data sets

The simplest way is to add one or more of our sample data sets. These data sets come with sample visualizations, dashboards, and more to help you explore the interface before you add your own data.

If you have no data, you will be prompted to install these packages when running {{kib}} for the first time.

To install sample data sets:

1. Go to the **Integrations** page and search for **Sample data**.
2. Select the sample data set you want to install and click **Install data**.

:::{note}
{applies_to}`stack: ga 9.0-9.3` In versions 9.0 to 9.3, you must first expand the **Other sample data sets** section to see the available sample data sets.
:::

:::{image} /manage-data/images/sample-data-sets.png
:alt: Sample data sets
:screenshot:
:::

## Run the makelogs script

Alternatively, run the provided `makelogs` script to generate sample data.

```bash
node scripts/makelogs --auth <username>:<password>
```

The default username and password combination are `elastic:changeme`

:::{important}
Make sure to execute `node scripts/makelogs` *after* {{es}} is up and running.
:::

## Upload a file

You can also upload your own sample data using the **Upload a file** option on the **Integrations** page. For detailed instructions, refer to [Upload data files](/manage-data/ingest/upload-data-files.md).
