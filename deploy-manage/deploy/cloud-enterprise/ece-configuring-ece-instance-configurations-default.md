---
applies_to:
  deployment:
    ece: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-configuring-ece-instance-configurations-default.html
---

# Default instance configurations [ece-configuring-ece-instance-configurations-default]

{{ece}} ships with a number of default instance configurations:

| Instance configuration | Instance types / node types | Default size | Memory sizes | Memory to storage multiplier |
| --- | --- | --- | --- | --- |
| `apm` | APM | 512 MB | 512, 1, 2, 4, 8 | 4 |
| `appsearch` | Application server, Worker | 4 GB | 2, 4, 8 | 2 |
| `ccs.default` | Data, Master, Coordinating | 1 GB | 1, 2, 4, 8, 16, 32, 64 | 4 |
| `coordinating` | Coordinating | 1 GB | 1, 2, 4, 8 | 2 |
| `data.default` | Data, Master, Coordinating | 4 GB | 1, 2, 4, 8, 16, 32, 64 | 32 |
| `data.frozen` | Data | 4 GB | 4, 8, 16, 32, 64 | 80 |
| `data.highstorage` | Data, Master, Coordinating | 2 GB | 1, 2, 4, 8, 16, 32, 64 | 64 |
| `enterprise.search` | Application server, Connector, Worker | 4 GB | 2, 4, 8 | 2 |
| `integrations.server` | Integrations Server | 512 MB | 512, 1, 2, 4, 8 | 4 |
| `kibana` | {{kib}} | 1 GB | 1, 2, 4, 8 | 4 |
| `master` | Master | 1 GB | 1, 2, 4, 8, 16, 32, 64 | 4 |
| `ml` | Machine Learning | 1 GB | 1, 2, 4, 8, 16, 32, 64 | 4 |

