---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-view-and-analyze-data.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-view-and-analyze-traces.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
  - id: cloud-serverless
---

# View and analyze data [apm-view-and-analyze-data]

After you’ve started [sending application data to Elastic](/solutions/observability/apm/ingest/index.md), you can open the Applications UI to view your data in a variety of visualizations and start analyzing data.

The Applications UI allows you to monitor your software services and applications in real-time. You can visualize detailed performance information on your services, identify and analyze errors, and monitor host-level and APM agent-specific metrics like JVM and Go runtime metrics.

Having access to application-level insights with just a few clicks can drastically decrease the time you spend debugging errors, slow response times, and crashes.

For example, you can see information about response times, requests per minute, and status codes per endpoint. You can even dive into a specific request sample and get a complete waterfall view of what your application is spending its time on. You might see that your bottlenecks are in database queries, cache calls, or external requests. For each incoming request and each application error, you can also see contextual information such as the request header, user information, system values, or custom data that you manually attached to the request.

To get started with the Applications UI:

* Start with quick, high-level [overviews](/solutions/observability/apm/overviews.md) that show you the overall health and performance of your application.
* [Drill down into data](/solutions/observability/apm/drill-down-into-data.md) for specific services or traces to get additional insight into your application.
* Learn how to get the most out of your data by mastering how to [search and filter data](/solutions/observability/apm/filter-search-data.md), getting tips on [how to interpret data](/solutions/observability/apm/interpret-data.md), and taking advantage of [machine learning](/solutions/observability/apm/machine-learning.md).
