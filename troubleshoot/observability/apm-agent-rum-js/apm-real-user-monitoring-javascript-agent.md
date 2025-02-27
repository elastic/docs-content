---
navigation_title: "APM Real User Monitoring JavaScript Agent"
mapped_pages:
  - https://www.elastic.co/guide/en/apm/agent/rum-js/current/troubleshooting.html
---

# Troubleshoot APM Real User Monitoring JavaScript Agent [troubleshooting]


## Some errors in the application appear to be originating from the agent’s JavaScript file [errors-originating-from-agent] 

In some cases when you look at the stack trace of an error, it appears to be originating from the agent’s JavaScript file. However, since we need to patch some browser APIs in order to provide some of the core functionalities of the agent, our JavaScript file appears in the error stack trace. Often, the error is generated from another part your application, you can follow the stack trace further to identify the offending code.

Of course, there are errors that might have been caused by the agent itself and we appreciate it if you [report them back to us](#get-in-touch).


## Some errors in the application only show `script error` [cross-origin-script-error] 

In some cases when you look at the details of an error, the only information you can see is the message `Script error`. This happens when an error originates from a JavaScript file served from a different origin than the page’s origin.

In order to get visibility of the error’s detail, you must do two things.

1. Add the attribute `crossorigin` to the `<script>` element:

    ```js
    <script src="https://example.com/example.js" crossorigin>
    ```

2. Make sure that the server response includes the `Access-Control-Allow-Origin` header when serving the JavaScript file.

    ```js
    // Either of the two values is valid:

    Access-Control-Allow-Origin: *
    Access-Control-Allow-Origin: your page's origin
    ```


::::{note} 
`Access-Control-Allow-Origin: *` will not match `localhost` in some browsers (e.g. [in Chrome](https://bugs.chromium.org/p/chromium/issues/detail?id=67743)), causing `Script error` messages in local development environments when the configuration is otherwise correct.
::::


::::{tip} 
To learn more about how browsers handle script errors, see the MDN page on the [onerror](https://developer.mozilla.org/en-US/docs/Web/API/GlobalEventHandlers/onerror#notes) event.
::::



## No stack trace available in the Span detail view [no-stack-trace-available] 

The RUM JS agent does not support stack traces for spans due to performance concerns related to gathering stack information.


## Debugging [debugging] 

In order to debug the agent consider performing the following steps:

1. Add `logLevel: 'debug'` to the agent configuration
2. Reload the application
3. Wait at least 5 seconds after the page has loaded
4. Monitor the Console and Network panel in your browsers developer tools


## Disable events payload compression [disable-events-payload-compression] 

In browsers such as Chrome, the RUM agent event payload is compressed with gzip. Because of this compression, you will not see readable content when inspecting the event with the Network panel of your browser developer tools.

There are situations where that can be an issue. For instance, HAR files will not show readable information. Therefore, inspecting events for debugging purposes will not be possible.

There are two ways to disable the payload compression:

1. Create an item named `_elastic_inspect_beacon_` using the sessionStorage browser API.
2. Load the webpage with the query param `_elastic_inspect_beacon_` in the URL. For example, `https://elastic.co?_elastic_inspect_beacon_=true`

The effect of this will remain until the tab or browser is closed.


## Disable the Agent [disable-agent] 

In the unlikely event the agent causes disruptions to a production application, you can disable the agent while you troubleshoot.

To disable the agent, set [`active`](asciidocalypse://docs/apm-agent-rum-js/docs/reference/configuration.md#active) to `false`.


## Get in touch [get-in-touch] 

If you have any questions, please create a new topic in the [Elastic APM discuss forum](https://discuss.elastic.co/c/apm).

For bug reports and feature requests, please [create an issue](https://github.com/elastic/apm-agent-rum-js/issues/new) on our [github repo](https://github.com/elastic/apm-agent-rum-js) and include as much information as possible. See [Debugging](#debugging) for how to gather debugging information.

