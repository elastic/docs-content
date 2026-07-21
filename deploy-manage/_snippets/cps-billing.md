{{cps-cap}} billing varies by project type:

| Project type | Billing |
|--------------|---------|
| {{es-serverless}} | {{cps-cap}} federated queries are handled by search VCUs, which scale the origin project to accommodate cross-project workloads. Refer to [](/deploy-manage/cloud-organization/billing/elasticsearch-billing-dimensions.md) for information about search VCUs. |
| {{obs-serverless}}<br><br>{{sec-serverless}} | During technical preview, there are no separate {{cps}} charges.<br><br>When {{cps-init}} becomes generally available, origin projects will incur an additional monthly charge for each GB of data retained in each project linked from the origin. Each retained GB in a linked project will be billed to the origin project on a monthly basis. |


When {{cps-init}} becomes generally available, all project types will also incur a charge for data moved between projects. Exact rates and billing mechanics will be provided closer to GA.