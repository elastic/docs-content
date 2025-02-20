# Manage data

Whether you're looking to build a fast and relevant full-text search solution, monitor business-critical applications and infrastructure, monitor endpoint security data, or one of the [many other use cases Elastic supports](/get-started/index.md#elasticsearch-intro-use-cases), you'll need to understand how to ingest and manage data stored in {{es}}.

## Learn how data is stored

% Topic: Learning about Elastic data store primitives

The fundamental unit of storage in {{es}}, the index, is a collection of documents uniquely identified by a name or an alias. These documents go through a process called mapping, which defines how a document and the fields it contains are stored and indexed, and a process called text analysis in which unstructured text is converted into a structured format that’s optimized for search.

**Learn more in [The Elasticsearch data store](/manage-data/data-store.md)**.

## Get data into {{es}}

% Topic: Evaluating and implementing ingestion and data enrichment technologies

Before you can start searching, visualizing, and pulling actionable insights from Elastic, you have to get your data into {{es}}.  Elastic offers a wide range of tools and methods for getting data into {{es}}. The best approach will depend on the kind of data you're ingesting and your specific use case.

**Learn more in [Ingestion](/manage-data/ingest.md).**

## Manage data over time

% Topic: Managing your data volume (lifecycle)

After you've added data to {{es}}, you'll need to manage it over time. For example, you may specify that data be deleted after a retention period or store data in multiple tiers with different performance characteristics.

Strategies for managing data depend on the type of data and how it's being used. For example, with a collection of items you want to search, like a catalog of products, the value of the content remains relatively constant over time so you want to be able to retrieve items quickly regardless of how old they are. Whereas with a stream of continuously-generated timestamped data, such as log entries, the data keeps accumulating over time, so you need strategies for balancing the value of the data against the cost of storing it.

**Learn more in [Data lifecycle](/manage-data/lifecycle.md).**

## Migrate data between Elasticsearch clusters

If you move to new infrastructure, there are several options for moving existing data between {{es}} clusters.

**Learn more in [Migrate your {{es}} data](/manage-data/migrate.md).**