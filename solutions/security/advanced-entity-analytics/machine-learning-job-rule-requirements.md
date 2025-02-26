---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/ml-requirements.html
  - https://www.elastic.co/guide/en/serverless/current/security-ml-requirements.html
---

# Machine learning job and rule requirements

To run and create {{ml}} jobs and rules in serverless, you need the appropriate [user role](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles). In {{stack}}, you need all of these:

* The [appropriate license](https://www.elastic.co/subscriptions)
* There must be at least one {{ml}} node in your cluster
* The `machine_learning_admin` user role

Additionally, to configure [alert suppression](/solutions/security/detect-and-alert/suppress-detection-alerts.md) for {{ml}} rules, your role needs the following [index privilege](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md#adding_index_privileges):

* `read` permission for the `.ml-anomalies-*` index

For more information, go to [Set up {{ml-features}}](/explore-analyze/machine-learning/setting-up-machine-learning.md).

::::{important} 
Some roles (for example, in {{stack}}, the `machine_learning_admin` and `machine_learning_user` built-in roles) give access to the results of *all* {{anomaly-jobs}}, irrespective of whether the user has access to the source indices. Likewise, a user who has full or read-only access to {{ml-features}} within a given {{kib}} space can view the results of *all* {{anomaly-jobs}} that are visible in that space. You must carefully consider who is given these roles and feature privileges; {{anomaly-job}} results may propagate field values that contain sensitive information from the source indices to the results.

::::


