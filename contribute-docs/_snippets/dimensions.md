The `applies_to` keys fall into three dimensions:

| Dimension | Values |
| --- | --- |
| Stack/Serverless | `stack`, `serverless` |
| Deployment | `deployment` (with subkeys: `ece`, `eck`, `ech`, `self`), `serverless` |
| Product | `product` (with subkeys: APM agents, EDOT items, etc.) |

Use only one dimension at the page level. `serverless` can appear in both the Stack/Serverless and Deployment dimensions.
