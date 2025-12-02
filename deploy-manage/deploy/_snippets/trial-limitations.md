During the free 14-day trial, Elastic provides access to one hosted deployment and three {{serverless-short}} projects. If all you want to do is try out Elastic, the trial includes more than enough to get you started. During the trial period, some limitations apply.

**Hosted deployments**

* You can only have one active deployment at a time.
* The deployment size is limited to 8GB RAM and approximately 360GB of storage, depending on the specified hardware profile.
* {{ml-cap}} nodes are available up to 4GB RAM, or up to 8GB when using Reranker.
* Custom {{es}} plugins are not enabled.
* We monitor token usage per account for the Elastic Managed LLM. If an account uses over one million tokens in 24 hours, we will inform you, then remove access to the LLM. This is in accordance with our fair use policy for trials. 

For more information, check the [{{ech}} documentation](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md).

**Serverless projects**

* You can have three active {{serverless-short}} projects at a time.
* Search Power is limited to 100 and Search Boost Window is limited to 7 days. These [settings](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-ai-lake-settings) apply only to {{es-serverless}} projects.
* Scaling is limited for {{serverless-short}} projects in trials. Failures might occur if the workload requires memory or compute beyond what the above search power and search boost window setting limits can provide.
* We monitor token usage per account for the Elastic Managed LLM. If an account uses over one million tokens in 24 hours, we will inform, then remove access to the LLM. This is in accordance with our fair use policy for trials. 
