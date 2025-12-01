---
navigation_title: Example
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/common-log-format-example.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---



# Example: Parse logs [common-log-format-example]


In this example tutorial, you’ll use an [ingest pipeline](ingest-pipelines.md) to parse server logs in the [Common Log Format](https://en.wikipedia.org/wiki/Common_Log_Format) before indexing. Before starting, check the [prerequisites](ingest-pipelines.md#ingest-prerequisites) for ingest pipelines.

The logs you want to parse look similar to this:

```txt
212.87.37.154 - - [05/May/2099:16:21:15 +0000] "GET /favicon.ico HTTP/1.1" 200 3638 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
```

These logs contain a timestamp, IP address, and user agent. You want to give these three items their own field in {{es}} for faster searches and visualizations. You also want to know where the request is coming from.

1. In {{kib}}, go to the **Ingest Pipelines** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

    :::{image} /manage-data/images/elasticsearch-reference-ingest-pipeline-list.png
    :alt: Kibana's Ingest Pipelines list view
    :screenshot:
    :::

2. Click **Create pipeline > New pipeline**.
3. Set **Name** to `my-pipeline` and optionally add a description for the pipeline.
4. Add a [grok processor](elasticsearch://reference/enrich-processor/grok-processor.md) to parse the log message:

    1. Click **Add a processor** and select the **Grok** processor type.
    2. Set **Field** to `message` and **Patterns** to the following [grok pattern](../../../explore-analyze/scripting/grok.md):

        ```text
        %{IPORHOST:source.ip} %{USER:user.id} %{USER:user.name} \[%{HTTPDATE:@timestamp}\] "%{WORD:http.request.method} %{DATA:url.original} HTTP/%{NUMBER:http.version}" %{NUMBER:http.response.status_code:int} (?:-|%{NUMBER:http.response.body.bytes:int}) %{QS:http.request.referrer} %{QS:user_agent}
        ```

    3. Click **Add** to save the processor.
    4. Set the processor description to `Extract fields from 'message'`.

5. Add processors for the timestamp, IP address, and user agent fields. Configure the processors as follows:

    | Processor type | Field | Additional options | Description |
    | --- | --- | --- | --- |
    | [**Date**](elasticsearch://reference/enrich-processor/date-processor.md) | `@timestamp` | **Formats**: `dd/MMM/yyyy:HH:mm:ss Z` | `Format '@timestamp' as 'dd/MMM/yyyy:HH:mm:ss Z'` |
    | [**GeoIP**](elasticsearch://reference/enrich-processor/geoip-processor.md) | `source.ip` | **Target field**: `source.geo` | `Add 'source.geo' GeoIP data for 'source.ip'` |
    | [**User agent**](elasticsearch://reference/enrich-processor/user-agent-processor.md) | `user_agent` |  | `Extract fields from 'user_agent'` |

    Your form should look similar to this:

    :::{image} /manage-data/images/elasticsearch-reference-ingest-pipeline-processor.png
    :alt: Processors for Ingest Pipelines
    :screenshot:
    :::

    The four processors will run sequentially:<br> Grok > Date > GeoIP > User agent<br> You can reorder processors using the arrow icons.

    Alternatively, you can click the **Import processors** link and define the processors as JSON:

    ```js
    {
      "processors": [
        {
          "grok": {
            "description": "Extract fields from 'message'",
            "field": "message",
            "patterns": ["%{IPORHOST:source.ip} %{USER:user.id} %{USER:user.name} \\[%{HTTPDATE:@timestamp}\\] \"%{WORD:http.request.method} %{DATA:url.original} HTTP/%{NUMBER:http.version}\" %{NUMBER:http.response.status_code:int} (?:-|%{NUMBER:http.response.body.bytes:int}) %{QS:http.request.referrer} %{QS:user_agent}"]
          }
        },
        {
          "date": {
            "description": "Format '@timestamp' as 'dd/MMM/yyyy:HH:mm:ss Z'",
            "field": "@timestamp",
            "formats": [ "dd/MMM/yyyy:HH:mm:ss Z" ]
          }
        },
        {
          "geoip": {
            "description": "Add 'source.geo' GeoIP data for 'source.ip'",
            "field": "source.ip",
            "target_field": "source.geo"
          }
        },
        {
          "user_agent": {
            "description": "Extract fields from 'user_agent'",
            "field": "user_agent"
          }
        }
      ]

    }
    ```

6. To test the pipeline, click **Add documents**.
7. In the **Documents** tab, provide a sample document for testing:

    ```js
    [
      {
        "_source": {
          "message": "212.87.37.154 - - [05/May/2099:16:21:15 +0000] \"GET /favicon.ico HTTP/1.1\" 200 3638 \"-\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36\""
        }
      }
    ]
    ```

8. Click **Run the pipeline** and verify the pipeline worked as expected.
9. If everything looks correct, close the panel, and then click **Create pipeline**.

    You’re now ready to index the logs data to a [data stream](../../data-store/data-streams.md).

10. Create an [index template](../../data-store/templates.md) with [data stream enabled](../../data-store/data-streams/set-up-data-stream.md#create-index-template).

    ```console
    PUT _index_template/my-data-stream-template
    {
      "index_patterns": [ "my-data-stream*" ],
      "data_stream": { },
      "priority": 500
    }
    ```

11. Index a document with the pipeline you created.

    ```console
    POST my-data-stream/_doc?pipeline=my-pipeline
    {
      "message": "89.160.20.128 - - [05/May/2099:16:21:15 +0000] \"GET /favicon.ico HTTP/1.1\" 200 3638 \"-\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36\""
    }
    ```

12. To verify, search the data stream to retrieve the document. The following search uses [`filter_path`](elasticsearch://reference/elasticsearch/rest-apis/common-options.md#common-options-response-filtering) to return only the [document source](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md).

    ```console
    GET my-data-stream/_search?filter_path=hits.hits._source
    ```

    The API returns:

    ```console-result
    {
      "hits": {
        "hits": [
          {
            "_source": {
              "@timestamp": "2099-05-05T16:21:15.000Z",
              "http": {
                "request": {
                  "referrer": "\"-\"",
                  "method": "GET"
                },
                "response": {
                  "status_code": 200,
                  "body": {
                    "bytes": 3638
                  }
                },
                "version": "1.1"
              },
              "source": {
                "ip": "89.160.20.128",
                "geo": {
                  "continent_name" : "Europe",
                  "country_name" : "Sweden",
                  "country_iso_code" : "SE",
                  "city_name" : "Linköping",
                  "region_iso_code" : "SE-E",
                  "region_name" : "Östergötland County",
                  "location" : {
                    "lon" : 15.6167,
                    "lat" : 58.4167
                  }
                }
              },
              "message": "89.160.20.128 - - [05/May/2099:16:21:15 +0000] \"GET /favicon.ico HTTP/1.1\" 200 3638 \"-\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36\"",
              "url": {
                "original": "/favicon.ico"
              },
              "user": {
                "name": "-",
                "id": "-"
              },
              "user_agent": {
                "original": "\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36\"",
                "os": {
                  "name": "Mac OS X",
                  "version": "10.11.6",
                  "full": "Mac OS X 10.11.6"
                },
                "name": "Chrome",
                "device": {
                  "name": "Mac"
                },
                "version": "52.0.2743.116"
              }
            }
          }
        ]
      }
    }
    ```
