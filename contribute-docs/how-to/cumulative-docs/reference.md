# Quick reference

:::{note}
If you have questions about how to write cumulative documentation while contributing,
reach out to **@elastic/docs** in the related GitHub issue or PR. 
:::

The `applies_to` directive uses the following format:

```
<key>: <lifecycle> <version>
```

This page provides minimal reference information on the `applies_to` directive. For more detailed information, refer to [the applies_to syntax guide](https://elastic.github.io/docs-builder/syntax/applies).

## Dimensions

The `applies_to` keys fall into three dimensions:

| Dimension | Values |
| --- | --- |
| Stack/Serverless | `stack`, `serverless` |
| Deployment | `deployment` (with subkeys: `ece`, `eck`, `ess`, `self`), `serverless` |
| Product | `product` (with subkeys, including those for APM agents, EDOT SDKs, and client libraries) |

Use only one dimension at the page level. `serverless` can appear in both the Stack/Serverless and Deployment dimensions. [Learn more](/contribute-docs/how-to/cumulative-docs/guidelines.md#dimensions).

## Key reference

### key

:::{include} /contribute-docs/_snippets/applies_to-key.md
:::

### lifecycle

:::{include} /contribute-docs/_snippets/applies_to-lifecycle.md
:::

### version

:::{include} /contribute-docs/_snippets/applies_to-version.md
:::
