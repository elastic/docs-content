[Beats](beats://reference/index.md) open source data shippers that you install as agents on your servers to send operational data to {{es}}. Elastic provides separate Beats for different types of data, such as logs, metrics, and uptime. 

Beats has been replaced by {{agent}} for most use cases. When you use {{agent}}, you’re getting core Beats functionality, but with more added features. Where you might need to install multiple Beats shippers on a host depending on your data requirements, single {{agent}} installed on a host can collect and transport multiple types of data.
