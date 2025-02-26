# Ingesting data from your application [ec-ingest-guides]

The following tutorials demonstrate how you can use the Elasticsearch language clients to ingest data from an application.

[Ingest data with Node.js on {{ech}}](../../../manage-data/ingest/ingesting-data-from-applications/ingest-data-with-nodejs-on-elasticsearch-service.md)
:   Get Node.js application data securely into {{ech}}, where it can then be searched and modified.

[Ingest data with Python on {{ech}}](../../../manage-data/ingest/ingesting-data-from-applications/ingest-data-with-python-on-elasticsearch-service.md)
:   Get Python application data securely into {{ech}}, where it can then be searched and modified.

[Ingest data from Beats to {{ech}} with Logstash as a proxy](../../../manage-data/ingest/ingesting-data-from-applications/ingest-data-from-beats-to-elasticsearch-service-with-logstash-as-proxy.md)
:   Get server metrics or other types of data from Filebeat and Metricbeat into Logstash as an intermediary, and then send that data to {{ech}}. Using Logstash as a proxy limits your Elastic Stack traffic through a single, external-facing firewall exception or rule.

[Ingest data from a relational database into {{ech}}](../../../manage-data/ingest/ingesting-data-from-applications/ingest-data-from-relational-database-into-elasticsearch-service.md)
:   Get data from a relational database into {{ech}} using the Logstash JDBC input plugin. Logstash can be used as an efficient way to copy records and to receive updates from a relational database as changes happen, and then send the new data to a deployment.

[Ingest logs from a Python application using Filebeat](../../../manage-data/ingest/ingesting-data-from-applications/ingest-logs-from-python-application-using-filebeat.md)
:   Get logs from a Python application and deliver them securely into an {{ech}} deployment. You’ll set up Filebeat to monitor an ECS-formatted log file, and then view real-time visualizations of the log events in Kibana as they occur.

[Ingest logs from a Node.js web application using Filebeat](../../../manage-data/ingest/ingesting-data-from-applications/ingest-logs-from-nodejs-web-application-using-filebeat.md)
:   Get HTTP request logs from a Node.js web application and deliver them securely into an {{ech}} deployment. You’ll set up Filebeat to monitor an ECS-formatted log file and then view real-time visualizations of the log events as HTTP requests occur on your Node.js web server.

::::{tip} 
You can use [Elasticsearch ingest pipelines](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md) to preprocess incoming data. This enables you to optimize how your data is indexed, and simplifies tasks such as extracting error codes from a log file and mapping geographic locations to IP addresses.
::::








