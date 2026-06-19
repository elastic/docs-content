:::{dropdown} Advanced settings
Several advanced options allow you to refine the behavior of the breakdown:

- **Include documents without the selected field**: Off by default.
- **Group remaining values as "Other"**: On by default.
- **Enable accuracy mode**: This option improves results for high-cardinality data, but increases the load on the {{es}} cluster.
- **Include values**: Values from the dimension to always include, even if they aren't among the top values. You can enter exact values or a regular expression.
- **Exclude values**: Values from the dimension to always exclude. You can enter exact values or a regular expression.
:::