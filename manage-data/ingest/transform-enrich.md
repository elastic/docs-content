---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest-overview/current/ingest-addl-proc.html
applies_to:
  stack: ga
  serverless: ga
products: []
---

# Transform and enrich data [ingest-addl-proc]

% You can start with {{agent}} and Elastic [integrations](https://docs.elastic.co/en/integrations), and still take advantage of additional processing options if you need them.

For many use cases you'll want to enhance your data as it's being ingested into {{es}}. Your goal might be to filter out unwanted parts of the data before it gets indexed. Another goal might be to reshape the data, such as to process incoming log files to conform to a standard format.

You might also want to enrich your data with additional information, for example to append product information based on product IDs or vendor information based on a set of known IP addresses.

According to your use case, you may want to control the structure of your ingested data by customizing how {{es}} maps an incoming document to fields and data types.

Finally, to help ensure optimal query results, you may want to customize how text is analyzed and how text fields are defined inside {{es}}.

Note that you can also perform transforms on existing {{es}} indices to pivot data into a summarized format, for example to break down web requests by geography or browser type. To learn more, refer to [Transforming data](../../explore-analyze/transforms.md).

{{agent}} processors
:   You can use [{{agent}} processors](/reference/fleet/agent-processors.md) to sanitize or enrich raw data at the source. Use {{agent}} processors if you need to control what data is sent across the wire, or if you need to enrich the raw data with information available on the host.

{{es}} ingest pipelines
:   You can use [{{es}} ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md) to enrich incoming data or normalize field data before the data is indexed. {{es}} ingest pipelines enable you to manipulate the data as it comes in. This approach helps you avoid adding processing overhead to the hosts from which you’re collecting data.

:   When you define a pipeline, you can configure one or more processors to operate on the incoming data. A typical use case is to transform specific strings to lowercase, or to sort the elements of incoming arrays into a given order. This section describes:
* How to create, view, edit, and delete an ingest pipeline
* How to set up processors to transform the data
* How to test a pipeline before putting it into production.

:   You can try out the [Parse logs](/manage-data/ingest/transform-enrich/example-parse-logs.md) example which shows you how to set up in ingest pipeline to transform incoming server logs into a standard format.

:   The {{es}} enrich processor enables you to add data from existing indices to your incoming data, based on an enrich policy. The enrich policy contains a set of rules to match incoming documents to the fields containing the data to add. Refer to [Data enrichment](transform-enrich/data-enrichment.md) to learn how to set up an enrich processor. You can also try out a few examples that show how to enrich data based on geographic location, exact values such as email addresses or IDs, or a range of values such as a date or set of IP addresses.

{{ls}} and the {{ls}} `elastic_integration filter`
:   If you're using {{ls}} as your primary ingest tool, you can take advantage of its built-in pipeline capabilities to transform your data. You configure a pipeline by stringing together a series of input, output, filtering, and optional codec plugins to manipulate all incoming data.

:   If you're ingesting using {{agent}} with Elastic {{integrations}}, you can use the {{ls}} [`elastic_integration filter`](logstash://reference/index.md) and other [{{ls}} filters](logstash-docs-md://lsr/filter-plugins.md) to [extend Elastic integrations](logstash://reference/using-logstash-with-elastic-integrations.md) by transforming data before it goes to {{es}}.

Ingest lag
:   Calculate the time it takes for data to travel from its source to {{es}}. This is key for monitoring performance and finding bottlenecks in your data pipelines. Learn how in [Calculate ingest lag](https://www.elastic.co/blog/calculating-ingest-lag-and-storing-ingest-time-in-elasticsearch-to-improve-observability).

Index mapping
:   Index mapping lets you control the structure that incoming data has within an {{es}} index. You can define all of the fields that are included in the index and their respective data types. For example, you can set fields for dates, numbers, or geolocations, and define the fields to have specific formats.

:   Ingested data can be mapped dynamically, where {{es}} adds all fields automatically based on the detected data types, or explicitly, where {{es}} maps the incoming data to fields based on your custom rules.

:   You can use {{es}} [runtime fields](../data-store/mapping/runtime-fields.md) to define or alter the schema at query time. You can start working with your data without needing to understand how it is structured, add fields to existing documents without reindexing your data, override the value returned from an indexed field, and/or define fields for a specific use without modifying the underlying schema.

:   Refer to the [Index mapping](../data-store/mapping.md) pages to learn about the dynamic mapping rules that {{es}} runs by default, which ones you can customize, and how to configure your own explicit data to field mappings.

Text analysis
:   Like index mapping, text analysis is another form of data transformation that runs on data as it's being ingested. This process analyzes incoming, unstructured text and organizes it in a way to ensure that all relevant documents are matched for a given text query, and not just exact string matches.

:   Refer to the [Text analysis](../data-store/text-analysis.md) pages to learn how to configure an analyzer to run on incoming text. You can opt to use one of several built-in analyzers, or create a custom analyzer for specific use cases.
