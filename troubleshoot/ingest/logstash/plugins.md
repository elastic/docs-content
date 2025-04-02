---
navigation_title: "Plugins"
mapped_pages:
  - https://www.elastic.co/guide/en/logstash/current/ts-plugins-general.html
applies_to:
  stack: ga
  serverless: ga
---

# Troubleshoot Logstash plugins [ts-plugins-general]


## Plugin tracing [ts-plugin-tracing] 

When you troubleshoot {{ls}} deployments, you might check the node stats API to look for plugins that are taking too long to process data, dropping data, or never received the data in the first place. After you identify a plugin whose metrics indicate a potential issue, it’s time to identify which plugin this is, and where it is declared in the configuration files.

While you can define an "id" for each plugin to facilitate this discovery, naming each plugin is not practical, especially for very large pipelines containing hundreds of plugins.

You can use the information from the Logstash APIs to fetch link an auto generated ID of a plugin to its declaration (starting with 7.6.0).

Here’s how:

1. [Browse stats API and find a plugin you want to investigate](#browse-stats)
2. [Find the plugin declaration in the pipeline graph](#find-declaration)
3. [Lookup the plugin’s definition in the source files](#lookup-def)


### Browse stats API and find a plugin you want to investigate [browse-stats] 

Example: "Give me any filter whose in/out events counters don’t match"

```shell
❯ curl -s localhost:9600/_node/stats | jq '.pipelines.main.plugins.filters[] | select(.events.in!=.events.out)'
```

```json
{
  "id": "75afda0f03a5af46279c4cba9408ca87664b9c988bf477e2a2cca535e59e856f",
  "events": {
    "in": 1,
    "out": 0,
    "duration_in_millis": 5
  },
  "name": "drop"
}
```


### Find the plugin declaration in the pipeline graph [find-declaration] 

Take the id from step 1 and use it to find the plugin in the pipeline graph:

```shell
❯ curl -s localhost:9600/_node/pipelines?graph=true | jq '.pipelines.main.graph.graph.vertices[] | select(.id=="75afda0f03a5af46279c4cba9408ca87664b9c988bf477e2a2cca535e59e856f")'
```

```json
{
  "config_name": "drop",
  "plugin_type": "filter",
  "meta": {
    "source": {
      "protocol": "file",
      "id": "/private/tmp/logstash-7.9.1/cfg",
      "line": 10,
      "column": 5
    }
  },
  "id": "75afda0f03a5af46279c4cba9408ca87664b9c988bf477e2a2cca535e59e856f",
  "explicit_id": false,
  "type": "plugin"
}
```


### Lookup the plugin’s definition in the source files [lookup-def] 

Here’s a simple script to do the lookup.

```shell
❯ cat /private/tmp/logstash-7.9.1/cfg |  ruby -e 'line = 10; $stdin.read.split("\n").each_with_index {|l, i| puts "#{i+1}: #{l}" if (i+1).between?(line-1, line + 5) }'
9:   } else if [message] == "d" {
10:     drop {}
11:   } else if [message] == "e" {
12:     drop {}
13:   } else if [message] == "f" {
14:     drop {}
15:   } else if [message] == "g" {
```

Or, you can open the file and go to the line.

