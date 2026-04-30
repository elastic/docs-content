During the free 14-day trial, Elastic provides access to one hosted deployment and three {{serverless-short}} projects. If all you want to do is try out Elastic, the trial includes more than enough to get you started. During the trial period, some limitations apply.

**Hosted deployments**

* You can only have one active deployment at a time.
* The deployment size is limited to 8GB RAM and approximately 360GB of storage, depending on the specified hardware profile.
* {{ml-cap}} nodes are available up to 4GB RAM, or up to 8GB when using Reranker.
* Custom {{es}} plugins are not enabled.
* Token usage for LLMs and other ML models is restricted during the trial period. If you require higher limits, reach out to [Support](https://cloud.elastic.co/support).

**Serverless projects**

* You can have three active {{serverless-short}} projects at a time.
* Search Power is limited to 100 and Search Boost Window is limited to 7 days. These [settings](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-ai-lake-settings) apply only to {{es-serverless}} projects.
* Scaling is limited for {{serverless-short}} projects in trials. Failures might occur if the workload requires memory or compute beyond what the above search power and search boost window setting limits can provide.
* Token usage for LLMs and other ML models is restricted during the trial period. If you require higher limits, reach out to [Support](https://cloud.elastic.co/support).
