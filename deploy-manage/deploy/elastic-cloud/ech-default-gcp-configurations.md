---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-default-gcp-configurations.html
---

# Elasticsearch Add-On for Heroku GCP default provider instance configurations [ech-default-gcp-configurations]

Following are the preferred instance types / machine configurations, storage types, disk to memory ratios, and virtual CPU to RAM ratios for all instance configurations available on {{ech}} and provided by GCP.

| Instance configuration | Preferred Instance Type or Machine Configuration1 | Storage Type1 | Disk:Memory Ratio2 | vCPU/RAM Ratio |
| --- | --- | --- | --- | --- |
| gcp.es.datahot.n2.68x10x45 | N2 | NVMe | 45:1 | 0.156 |
| gcp.es.datahot.n2.68x10x95 | N2 | NVMe | 95:1 | 0.156 |
| gcp.es.datahot.n2.68x16x45 | N2 | NVMe | 45:1 | 0.250 |
| gcp.es.datahot.n2.68x32x45 | N2 | NVMe | 45:1 | 0.500 |
| gcp.es.datahot.n2d.64x8x11 | N2d | NVMe | 11:1 | 0.133 |
| gcp.es.datawarm.n2.68x10x190 | N2 | Zonal standard persistent disk | 190:1 | 0.156 |
| gcp.es.datacold.n2.68x10x190 | N2 | Zonal standard persistent disk | 190:1 | 0.156 |
| gcp.es.datafrozen.n2.68x10x95 | N2 | NVMe | 95:1 | 0.156 |


## Additional instances [ech-gcp-additional-instances] 

Following are the preferred instance configuration and virtual CPU to RAM ratios for additional instance configurations available on {{ech}} and provided by GCP.

| Instance configuration | Preferred Instance Type or Machine Configuration1 | vCPU/RAM Ratio |
| --- | --- | --- |
| gcp.es.master.n2.68x32x45 | N2 | 0.500 |
| gcp.es.ml.n2.68x16x45 | N2 | 0.250 |
| gcp.es.ml.n2.68x32x45 | N2 | 0.500 |
| gcp.es.coordinating.n2.68x16x45 | N2 | 0.250 |
| gcp.kibana.n2.68x32x45 | N2 | 0.500 |
| gcp.apm.n2.68x32x45 | N2 | 0.500 |
| gcp.integrationsserver.n2.68x32x45 | N2 | 0.500 |
| gcp.enterprisesearch.n2.68x32x45 | N2 | 0.500 |

1 Preferred instance and storage types are subject to provider availability. To learn more about our provider instances, check the [GCP](https://cloud.google.com/compute/docs/machine-types) reference page.

2 Ratios are estimations.

## Regional availability of instances per GCP region [ech-gcp-list-region]

The following table contains the complete list of instances available in Elastic Cloud deployments per GCP region:

| Regions | Instances |  |
| --- | --- | --- |
|  | N2 | N2d |
| Asia Pacific East 1 (Taiwan) | ✓ | ✓ |
| Asia Pacific Northeast 1 (Tokyo) | ✓ | ✓ |
| Asia Pacific Northeast 3 (Seoul) | ✓ | ✓ |
| Asia Pacific South 1 (Mumbai) | ✓ | ✓ |
| Asia Pacific Southeast 1 (Singapore) | ✓ | ✓ |
| Asia Pacific Southeast 2 (Jakarta) | ✓ |  |
| Australia Southeast 1 (Sydney) | ✓ | ✓ |
| Europe North 1 (Finland) | ✓ | ✓ |
| Europe West 1 (Belgium) | ✓ | ✓ |
| Europe West 2 (London) | ✓ | ✓ |
| Europe West 3 (Frankfurt) | ✓ | ✓ |
| Europe West 4 (Netherlands) | ✓ | ✓ |
| Europe West 9 (Paris) | ✓ | ✓ |
| ME West 1 (Tel Aviv) | ✓ | ✓ |
| North America Northeast 1 (Montreal) | ✓ | ✓ |
| South America East 1 (Sao Paulo) | ✓ | ✓ |
| US Central 1 (Iowa) | ✓ | ✓ |
| US East 1 (South Carolina) | ✓ | ✓ |
| US East 4 (N. Virginia) | ✓ | ✓ |
| US West 1 (Oregon) | ✓ | ✓ |


