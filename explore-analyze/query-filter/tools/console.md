---
navigation_title: Console
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/console-kibana.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-api-console.html
  - https://www.elastic.co/guide/en/serverless/current/devtools-run-api-requests-in-the-console.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-enterprise
  - id: cloud-serverless
---

# Run API requests with Console [console-kibana]

**Console** is an interactive UI for sending requests to [{{es}} APIs](elasticsearch://reference/elasticsearch/rest-apis/index.md) and [{{kib}} APIs](https://www.elastic.co/docs/api) and viewing their responses.

:::{image} /explore-analyze/images/kibana-console.png
:alt: Console
:screenshot:
:::

To go to **Console**, find **Dev Tools** in the navigation menu or use the [global search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md).

You can also find Console directly on certain Search solution and Elasticsearch serverless project pages, where you can expand it from the footer. This Console, called **Persistent Console**, has the same capabilities and shares the same history as the Console in **Dev Tools**.

:::{image} /explore-analyze/images/kibana-persistent-console.png
:alt: Console
:screenshot:
:::


## Write requests [console-api]

**Console** accepts commands in a simplified HTTP request syntax. For example, the following `GET` request calls the {{es}} `_search` API:

```js
GET /_search
{
  "query": {
    "match_all": {}
  }
}
```

Here is the equivalent command in cURL:

```bash
curl -XGET "http://localhost:9200/_search" -d'
{
  "query": {
    "match_all": {}
  }
}'
```

Prepend requests to a {{kib}} API endpoint with `kbn:`

```bash
GET kbn:/api/index_management/indices
```


### Autocomplete [console-autocomplete]

When you’re typing a command, **Console** makes context-sensitive suggestions. These suggestions show you the parameters for each API and speed up your typing.

You can configure your preferences for autocomplete in the [Console settings](#configuring-console).


### Comments [console-comments]

You can write comments or temporarily disable parts of a request by using double forward slashes or pound signs to create single-line comments.

```js
# This request searches all of your indices.
GET /_search
{
  // The query parameter indicates query context.
  "query": {
    "match_all": {} // Matches all documents.
  }
}
```

You can also use a forward slash followed by an asterisk to mark the beginning of multi-line comments. An asterisk followed by a forward slash marks the end.

```js
GET /_search
{
  "query": {
    /*"match_all": {
      "boost": 1.2
    }*/
    "match_none": {}
  }
}
```


### Variables [console-variables]

Click **Variables** to create, edit, and delete variables.

:::{image} /explore-analyze/images/kibana-variables.png
:alt: Variables
:screenshot:
:::

You can refer to these variables in the paths and bodies of your requests. Each variable can be referenced multiple times.

```js
GET ${pathVariable}
{
  "query": {
    "match": {
      "${bodyNameVariable}": "${bodyValueVariable}"
    }
  }
}
```

By default, variables in the body may be substituted as a boolean, number, array, or object by removing nearby quotes instead of a string with surrounding quotes. Triple quotes overwrite this default behavior and enforce simple replacement as a string.

```js
GET /locations/_search
{
  "query": {
    "bool": {
      "must": {
        "match": {
          // ${shopName} shall be replaced as a string if the variable exists.
          "shop.name": """${shopName}"""
        }
      },
      "filter": {
        "geo_distance": {
          "distance": "12km",
          // "${pinLocation}" may be substituted with an array such as [-70, 40].
          "pin.location": "${pinLocation}"
        }
      }
    }
  }
}
```


### Auto-formatting [auto-formatting]

The auto-formatting capability can help you format requests to be more readable. Select one or more requests that you want to format, open the contextual menu, and then select **Auto indent**.


### Keyboard shortcuts [keyboard-shortcuts]

Go to line number
:   `Ctrl/Cmd` + `L`

Auto-indent current request
:   `Ctrl/Cmd` + `I`

Jump to next request end
:   `Ctrl/Cmd` + `↓`

Jump to previous request end
:   `Ctrl/Cmd` + `↑`

Open documentation for current request
:   `Ctrl/Cmd` + `/`

Run current request
:   `Ctrl/Cmd` + `Enter`

Apply current or topmost term in autocomplete menu
:   `Enter` or `Tab`

Close autocomplete menu
:   `Esc`

Navigate items in autocomplete menu
:   `↓` + `↑`


### View API docs [console-view-api]

To view the documentation for an API endpoint, select the request, then open the contextual menu and select **Open API reference**.


## Run requests [console-request]

When you’re ready to run a request, select the request, and click the play button.

The result of the request execution is displayed in the response panel, where you can see:

* the JSON response
* the HTTP status code corresponding to the request
* The execution time, in ms.

::::{tip}
You can select multiple requests and submit them together. **Console** executes the requests one by one. Submitting multiple requests is helpful when you’re debugging an issue or trying query combinations in multiple scenarios.
::::



## Import and export requests [import-export-console-requests]

You can export requests:

* **to a TXT file**, by using the **Export requests** button. When using this method, all content of the input panel is copied, including comments, requests, and payloads. All of the formatting is preserved and allows you to re-import the file later, or to a different environment, using the **Import requests** button.

  ::::{tip}
  When importing a TXT file containing Console requests, the current content of the input panel is replaced. Export it first if you don’t want to lose it, or find it in the **History** tab if you already ran the requests.
  ::::

* by copying them individually as **curl**, **JavaScript**, or **Python**. To do this, select a request, then open the contextual menu and select **Copy as**. When using this action, requests are copied individually to your clipboard. You can save your favorite language to make the copy action faster the next time you use it.

    When running copied requests from an external environment, you’ll need to add [authentication information](https://www.elastic.co/docs/api/doc/kibana/authentication) to the request.



## Get your request history [console-history]

**Console** maintains a list of the last 500 requests that you tried to execute. To view them, open the **History** tab.

You can run a request from your history again by selecting the request and clicking **Add and run**. If you want to add it back to the Console input panel without running it yet, click **Add** instead. It is added to the editor at the current cursor position.


## Configure Console settings [configuring-console]

Go to the **Config** tab of **Console** to customize its display, autocomplete, and accessibility settings.


## Disable Console [disable-console]

If you don’t want to use **Console**, you can disable it by setting `console.ui.enabled` to `false` in your [`kibana.yml`](/deploy-manage/stack-settings.md) configuration file. Changing this setting causes the server to regenerate assets on the next startup, which might cause a delay before pages start being served.

You can also choose to only disable the persistent console that shows in the footer of several Kibana pages. To do that, go to **Stack Management** > **Advanced Settings**, and turn off the `devTools:enablePersistentConsole` setting.
