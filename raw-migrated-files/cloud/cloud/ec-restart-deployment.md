# Restart your deployment [ec-restart-deployment]

You might need to restart your deployment while addressing issues, like cycling garbage collection.

On the deployment overview, from the **Action** drop-down menu select **Restart {{es}}**.

You can choose to restart without downtime or you can restart all nodes simultaneously.

Note that if you are looking to restart {{es}} to clear out [deployment activity](../../../deploy-manage/deploy/elastic-cloud/keep-track-of-deployment-activity.md) plan failures, you may instead run a [no-op plan](../../../troubleshoot/monitoring/deployment-health-warnings.md) to re-synchronize the last successful configuration settings between Elasticsearch Service and {{es}}.

