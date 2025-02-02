# Documentation sections [doc-sections]

The documentation is broken-down in two parts:

## Setup & Requirements [_setup_requirements]

This [section](https://www.elastic.co/guide/en/elasticsearch-hadoop/current/features.html) provides an overview of the project, its requirements (and supported environment and libraries) plus information on how to easily install elasticsearch-hadoop in your environment.


## Reference Documentation [_reference_documentation]

This part of the documentation explains the core functionality of elasticsearch-hadoop starting with the configuration options and architecture and gradually explaining the various major features. At a higher level the reference is broken down into architecture and configuration section which are general, Map/Reduce and the libraries built on top of it, upcoming computation libraries (like Apache Spark) and finally mapping, metrics and troubleshooting.

We recommend going through the entire documentation even superficially when trying out elasticsearch-hadoop for the first time, however those in a rush, can jump directly to the desired sections:

[*Architecture*](https://www.elastic.co/guide/en/elasticsearch-hadoop/current/arch.html)
:   overview of the elasticsearch-hadoop architecture and how it maps on top of Hadoop

[*Configuration*](https://www.elastic.co/guide/en/elasticsearch-hadoop/current/configuration.html)
:   explore the various configuration switches in elasticsearch-hadoop

[*Map/Reduce integration*](https://www.elastic.co/guide/en/elasticsearch-hadoop/current/mapreduce.html)
:   describes how to use elasticsearch-hadoop in vanilla Map/Reduce environments - typically useful for those interested in data loading and saving to/from {{es}} without little, if any, ETL (extract-transform-load).

[*Apache Hive integration*](https://www.elastic.co/guide/en/elasticsearch-hadoop/current/hive.html)
:   Hive users should refer to this section.

[*Apache Spark support*](https://www.elastic.co/guide/en/elasticsearch-hadoop/current/spark.html)
:   describes how to use Apache Spark with {{es}} through elasticsearch-hadoop.

[*Mapping and Types*](https://www.elastic.co/guide/en/elasticsearch-hadoop/current/mapping.html)
:   deep-dive into the strategies employed by elasticsearch-hadoop for doing type conversion and mapping to and from {{es}}.

[*Hadoop Metrics*](https://www.elastic.co/guide/en/elasticsearch-hadoop/current/metrics.html)
:   Elasticsearch Hadoop metrics

[*Troubleshooting*](https://www.elastic.co/guide/en/elasticsearch-hadoop/current/troubleshooting.html)
:   tips on troubleshooting and getting help


