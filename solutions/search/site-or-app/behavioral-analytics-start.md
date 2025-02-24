---
navigation_title: "Get started"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/behavioral-analytics-start.html
applies_to:
  stack:
---



# Get started [behavioral-analytics-start]


You can manage your analytics in the {{kib}} UI. Go to **Search > Behavioral Analytics** to get started.

Using behavioral analytics is a three-step process:

1. **Create a [collection](#behavioral-analytics-start-collections)**. A collection is a logical grouping of your analytics events.
2. **Set up** a [UI integration](#behavioral-analytics-start-ui-integration).
3. **Analyze** the data collected.


## Collections [behavioral-analytics-start-collections] 

::::{note} 
This guide focuses on using the Behavioral Analytics UI in {{kib}} to create and manage collections. You can also use the [Behavioral Analytics APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-analytics) to create, list, and delete collections, as well as post events to a collection.

::::


A collection is a set of analytics events.

The first step in setting up behavioral analytics is to create a collection. To do this in the {{kib}} UI:

1. Go to **Search > Behavioral Analytics**.
2. Select **Create collection**.
3. Name your collection carefully, because you can’t change it later.
4. Select **Create**.

When you create a collection we automatically create a [data view^](../../../explore-analyze/find-and-organize/data-views.md) for the collection. This allows {{kib}} to access your analytics data stored in {{es}}.

This means that once you integrate analytics into your application or website, you can immediately use [Discover^](../../../explore-analyze/discover.md) to view events, set filters, and create visualizations using [Lens^](../../../explore-analyze/visualize/lens.md).

Once you’ve created a collection, you need to complete your UI integration.


## UI integration [behavioral-analytics-start-ui-integration] 

::::{note} 
Detailed integration instructions are provided in the {{kib}} UI. Find these in the **Integrate** tab under **Search > Behavioral Analytics >** *<your-collection>*.

::::


Choose *one* of the following integration options:

* [Option 1: Browser tracker](#behavioral-analytics-start-ui-integration-js-embed)
* [Option 2: JavaScript tracker](#behavioral-analytics-start-ui-integration-js-client)

Once embedded, users of the [Search UI](https://docs.elastic.co/search-ui/getting-started) JavaScript library can use the following integration for simplified event shipping:

* [Search UI integration](#behavioral-analytics-start-ui-integration-search-ui)


### Option 1: Browser tracker [behavioral-analytics-start-ui-integration-js-embed] 

Add a JavaScript snippet to your website or application source files, using the [Browser tracker](https://github.com/elastic/behavioral-analytics-tracker/blob/main/packages/browser-tracker/README.md).

This approach is best for web browsers. Node apps and Search UI users shouldn’t choose this option.

Instructions for getting started are available in the {{kib}} UI.

**Follow these steps**:

1. Embed the behavioral analytics JavaScript snippet on every page of the website or application you’d like to track.

    ```js
    <script src="https://cdn.jsdelivr.net/npm/@elastic/behavioral-analytics-browser-tracker@2"></script>
    ```

2. Initialize the client to start tracking events. For example:

    ```js
    <script type="text/javascript">
    window.elasticAnalytics.createTracker({
      endpoint: "https://77561m8ivn1olhs5fczpls0xa85bueqt.us-west2.gcp.elastic-cloud.com:443",
      collectionName: "my-collection",
      apiKey: "########",
      // Optional: sampling rate percentage: 0-1, 0 = no events, 1 = all events
      // sampling: 1,
    });
    </script>
    ```

3. Track search events, like result clicks and searches, by using the `trackSearch` or `trackSearchClick` methods.


### Option 2: JavaScript tracker [behavioral-analytics-start-ui-integration-js-client] 

The JavaScript client is available as an [NPM package](https://www.npmjs.com/package/@elastic/behavioral-analytics-javascript-tracker). We recommend this approach if your application bundles JavaScript from NPM packages. This is a good option for Node apps (server-side apps). Analytics will be bundled with your app.

This allows the browser to optimize the JavaScript download.

Instructions for getting started are also available in the {{kib}} UI.

**Follow these steps** to get started:

1. **Download** the behavioral analytics JavaScript tracker client from NPM:

    `npm install @elastic/behavioral-analytics-javascript-tracker`

2. **Import** the client into your application:

    ```js
    import {
      createTracker,
      trackPageView,
      trackSearch,
      trackSearchClick
    } from "@elastic/behavioral-analytics-javascript-tracker";
    ```

3. **Initialize** the client to start tracking events:

    Use the `createTracker` method to initialize the tracker with your configuration. You can then use the tracker to send events to Behavioral Analytics.

    Example initialization:

    ```js
    createTracker({
      endpoint: "https://77561m8ivn1olhs5fczpls0xa85bueqt.us-west2.gcp.elastic-cloud.com:443",
      collectionName: "my-collection",
      apiKey: "<api-key>"
    });
    ```

4. **Dispatch** Pageview and search behavior events.

    Once you have called `createTracker`, you can use the tracker methods such as `trackPageView` to send events to Behavioral Analytics.


Once integrated, you should be able to see page view events within the **Explorer** tab.

::::{tip} 
**Session-based sampling**

You don’t always want all sessions to be sent to your Elastic cluster. You can introduce session-based sampling by adding a sampling parameter to the `createTracker` method.

If sampling is set to 1 (default), all sessions will send events. If sampling is set to 0, no sessions will send events.

Here’s an example:

```js
createTracker({
  // ... tracker settings
  sampling: 0.3, // 30% of sessions will send events to the server
});
```

::::



## Search UI integration [behavioral-analytics-start-ui-integration-search-ui] 

[Search UI](https://docs.elastic.co/search-ui) is a JavaScript library for building search experiences. Use the [Search UI analytics plugin](https://www.npmjs.com/package/@elastic/search-ui-analytics-plugin) available on NPM to integrate behavioral analytics with Search UI.

This integration enables you to dispatch events from Search UI to the behavioral analytics client. The advantage of this integration is that you don’t need to set up custom events. Events fired by Search UI are dispatched automatically.

To use this integration, follow these steps:

1. Embed Behavioral Analytics into your site using [Option 1: Browser tracker](#behavioral-analytics-start-ui-integration-js-embed) **or** the [Option 2: JavaScript tracker](#behavioral-analytics-start-ui-integration-js-client).
2. Install the [`@elastic/search-ui-analytics-plugin`](https://www.npmjs.com/package/@elastic/search-ui-analytics-plugin) by importing it into your app.
3. Add the plugin to your Search UI configuration.

See the [Search UI analytics plugin documentation](https://docs.elastic.co/search-ui/api/core/plugins/analytics-plugin) for details.


## Next steps [behavioral-analytics-start-next-steps] 

* Refer to the [analytics API reference](behavioral-analytics-api.md).

