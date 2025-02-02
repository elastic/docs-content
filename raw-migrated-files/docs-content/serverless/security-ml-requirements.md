# {{ml-cap}} job and rule requirements [security-ml-requirements]

To run and create {{ml}} jobs and rules, you need the appropriate [user role](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

Additionally, for [custom roles](../../../deploy-manage/users-roles/cloud-organization/user-roles.md), to configure [alert suppression](../../../solutions/security/detect-and-alert/suppress-detection-alerts.md) for {{ml}} rules, your role needs the following index privilege:

* `read` permission for the `.ml-anomalies-*` index

For more information, go to [Set up {{ml-features}}](../../../explore-analyze/machine-learning/setting-up-machine-learning.md).

::::{important} 
Some roles give access to the results of *all* {{anomaly-jobs}}, irrespective of whether the user has access to the source indices. Likewise, a user who has full or read-only access to {{ml-features}} within a given {{kib}} space can view the results of *all* {{anomaly-jobs}} that are visible in that space. You must carefully consider who is given these roles and feature privileges; {{anomaly-job}} results may propagate field values that contain sensitive information from the source indices to the results.

::::


