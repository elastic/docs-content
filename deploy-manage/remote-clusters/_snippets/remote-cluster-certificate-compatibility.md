<!--
This snippet is in use in the following locations:
- eck-remote-clusters-landing.md
- remote-clusters-cert.md
- ece-enable-ccs.md
- ec-enable-ccs.md
-->

:::::{dropdown} Version compatibility table

* Any node can communicate with another node on the same major version. For example, 9.0 can talk to any 9.x node.
* Version compatibility is symmetric, meaning that if 7.16 can communicate with 8.0, 8.0 can also communicate with 7.16. The following table depicts version compatibility between local and remote nodes.

::::{note}
Version 8.19 is the final minor release in the 8.x series. Unlike past releases, 8.18 was launched simultaneously with 9.0, allowing cross-version compatibility between them. Hence, as shown in the compatibility table, 8.18 can search 9.0 clusters, but only 8.19 supports searching 9.1 and later.
::::

:::{include} ccs-compatibility-table.md
:::

:::::


