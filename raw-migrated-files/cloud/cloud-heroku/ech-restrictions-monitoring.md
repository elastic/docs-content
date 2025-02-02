# Restrictions and limitations [ech-restrictions-monitoring]

* To avoid compatibility issues, ensure your monitoring cluster and production cluster run on the same {{stack}} version. Monitoring clusters that use 8.x do work with production clusters that use the latest release of 7.x, but this setup should only occur when upgrading clusters to the same version.
* $$$cross-region-monitor$$$ Monitoring across regions is not supported. If you need to move your existing monitoring to the same region, you can do a reindex or create a new deployment and select the snapshot from the old deployment.
* The logs shipped to a monitoring cluster use an ILM managed data stream (elastic-cloud-logs-<version>). If you need to delete indices due to space, do not delete the current is_write_enabled: true index.
* When sending metrics to a dedicated monitoring deployment, the graph for IO Operations Rate(/s) is blank. This is due to the fact that this graph actually contains metrics from of all of the virtualized resources from the provider.

