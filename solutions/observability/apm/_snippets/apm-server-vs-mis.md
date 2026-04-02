:::{admonition} APM Server vs managed intake service
In {{ech}}, the _APM Server_ receives data from Elastic APM agents and transforms it into Elasticsearch documents. In {{serverless-full}} there is in fact no APM Server running, instead the _managed intake service_ receives and transforms data.
:::