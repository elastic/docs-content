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

:::{note}
To install sample data sets, you need `all` {{kib}} privileges for **Integrations**. Manage your roles, privileges, and spaces in **{{stack-manage-app}}**.
:::

1. Open the **Integrations** page using the global search field, then search for **Sample Data** using the integrations search field. 
2. Click **Sample Data** to open the **Add data** page. 
3. Select the sample data set you want to install and click **Install data**.
:::{image} /manage-data/images/sample-data-sets-9.4.png
:alt: Sample data sets
:screenshot:
:::

::::{note}
:applies_to: stack: ga 9.0-9.3

In versions 9.0 to 9.3, you must first expand the **Other sample data sets** section to see the available sample data sets.

:::{image} /manage-data/images/sample-data-sets.png
:alt: Sample data sets in versions 9.0 to 9.3
:screenshot:
:::
::::

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
