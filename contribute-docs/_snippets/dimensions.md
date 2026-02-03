The `applies_to` keys fall into three dimensions:

| Dimension | Values |
| --- | --- |
| Stack/Serverless | `stack`, `serverless` |
| Deployment | `deployment` (with subkeys: `ece`, `eck`, `ess`, `self`), `serverless` |
| Product | `product` (with subkeys, including those for APM agents, EDOT SDKs, and client libraries) |

Use only one dimension at the page level. `serverless` can appear in both the Stack/Serverless and Deployment dimensions.
