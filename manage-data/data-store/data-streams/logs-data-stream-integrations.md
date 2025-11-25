---
applies_to:
  stack: ga
  serverless: ga
navigation_title: "Enable logsdb for integrations"
products:
  - id: elasticsearch
---

# Enable `logsdb` for existing Elastic integrations [enable-logsdb-integrations]

::::{tip}
This section explains how to enable `logsdb` index mode on Elastic [integrations](reference://integrations.md) that are already installed. If you're creating a new logs data stream from scratch, refer to [Create a logs data stream](logs-data-stream.md#how-to-use-logsds).
::::

Integrations use [index templates](../templates.md) managed by Elastic. To enable `logsdb` mode for an existing integration, modify the integration's backing templates by applying custom component templates (`@custom`).

Before enabling `logsdb` mode for a specific integration, confirm its name and data stream types:

1. **Integration name**: The name of the integration in the package manifest. For example, the [MySQL integration](reference://integrations/mysql.md) is named `mysql`. If you're not sure which integration you need to modify, refer to [Find integrations with logs data streams](#find-integrations-logsdb).

2. **Logs data streams**: Make sure the integration includes logs data streams  configured with `type: logs`. For example, the MySQL error integration has data streams named `mysql.error` and `mysql.slowlog`.

To check for logs data streams using the command line:

```bash
curl -sL epr.elastic.co/package/mysql/1.28.1 | jq '.data_streams[] |
select(.type == "logs") | {dataset, type}'
```

Example output:
```json
{
  "dataset": "mysql.error",
  "type": "logs"
}
{
  "dataset": "mysql.slowlog",
  "type": "logs"
}
```

### Find integrations with logs data streams [find-integrations-logsdb]

If you're not sure which integration you need to work with, follow these steps to find installed integrations with logs data streams (or to check the index mode):

1. Navigate to **Stack Management** → **Index Management** → **Data Streams**.
2. Search for the integration name, or browse the list.
3. Check the **Index mode** column to confirm the current setting.

### Enable logsdb mode with custom component templates [enable-logsdb-custom-templates]

To enable logsdb mode by using custom component templates, follow the steps in this section.

% TODO confirm placement

::::{important}
For index mode changes to take effect, the data stream must be [rolled over](/manage-data/data-store/data-streams#data-streams-rollover.md) (automatically or manually).
::::

#### Step 1: Check for existing @custom component templates

First, check whether `@custom` component templates already exist for the integration:

1. Navigate to **Index Management** → **Component Templates**.
2. Search for `@custom`.

#### Step 2: Update or create custom component templates

Depending on whether `@custom` templates already exist, choose one of the following options:

% TODO this is not how we do options; fix it

**Option A: Edit existing @custom component templates**

If the integration already has `@custom` component templates, edit them to add the `logsdb` index mode setting.

% TODO expand

**Option B: Create new custom component templates**

If no `@custom` templates exist, create a new component template with the `logsdb` index mode setting.

% TODO confirm this kind of branching in other docs; apply tabs?

Using Dev Tools Console:

```console
PUT _component_template/logs-mysql.slowlog@custom
{
  "template": {
    "settings": {
      "mode": "logsdb"
    }
  }
}
```

Using the command line:

```bash
curl -s -XPOST -H'Authorization: ApiKey <API_KEY>' -H'Content-Type: application/json' \
'<ES_URL>/_component_template/logs-mysql.slowlog@custom' \
-d'{"template": {"settings": {"mode":"logsdb"}}}'
```


### Enable `logsdb` mode for all data streams in an integration
To create the required component templates for all logs data streams in a given integration at once:

```bash
curl -sL epr.elastic.co/package/mysql/1.28.1 | jq '.data_streams[] |
select(.type == "logs") | .dataset' | xargs -I% curl -s -XPOST \
-H'Authorization: ApiKey <API_KEY>' -H'Content-Type: application/json' \
'<ES_API>/_component_template/logs-%@custom' -d'{"template": {"settings": {"mode":"logsdb"}}}'
```

### Enable `logsdb` mode for all logs in a cluster [enable-logsdb-cluster-wide]

To enable `logsdb` mode for all logs data streams in a cluster (rather than for individual integrations), create or modify a component template named `logs@custom`. Add the  `mode:logsdb` setting.

% TODO confirm placement/addition

### Apply changes: Roll over data streams

For index mode changes to take effect, the data stream must be [rolled over](/manage-data/data-store/data-streams#data-streams-rollover.md) (automatically or manually).
