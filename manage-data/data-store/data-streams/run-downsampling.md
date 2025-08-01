---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Run downsampling on time series data [running-downsampling]

:::{warning}
🚧 Work in progress 🚧
:::

% TODO consider retitling to "Downsample time series data"

To downsample a time series index, you can use the `downsample API`, index lifecycle management (ILM), or a data stream lifecycle.


::::{tab-set}
:::{tab-item} Downsample API

## Use the downsample API

Issue a [downsample API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-downsample) request,  setting `fixed_interval` to your preferred level of granularity:

```console
POST /my-time-series-index/_downsample/my-downsampled-time-series-index
{
    "fixed_interval": "1d"
}
```
:::

:::{tab-item} Index lifecycle
    
## Downsample with index lifecycle management

To downsample time series data as part of index lifecycle management (ILM), include a [downsample action](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-downsample.md) in your ILM policy, setting `fixed_interval` to your preferred level of granularity:

```console
PUT _ilm/policy/my_policy
{
"policy": {
    "phases": {
    "warm": {
        "actions": {
        "downsample" : {
            "fixed_interval": "1h"
        }
        }
    }
    }
}
}
```
:::

:::{tab-item} Data stream lifecycle

Move tutorial here

:::

::::
