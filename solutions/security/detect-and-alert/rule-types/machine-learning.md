---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/rules-ui-create.html#create-ml-rule
  - https://www.elastic.co/guide/en/serverless/current/security-rules-create.html#create-ml-rule
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Create a machine learning rule [create-ml-rule]

Machine learning rules create alerts when a {{ml}} job discovers an anomaly above a defined threshold. These rules detect unusual behavior based on learned baselines rather than specific patterns.

**When to use**: Detect anomalous or unusual behavior that deviates from normal patterns (e.g., rare process execution, unusual network activity, abnormal user behavior).

**Performance**: Fast rule execution (~50ms), but ML jobs require dedicated resources (approximately 2GB RAM per job).

::::{admonition} Requirements
To create or edit {{ml}} rules, you need:
* The appropriate [{{stack}} subscription](https://www.elastic.co/pricing) or [{{serverless-short}} project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md).
* The [`machine_learning_admin`](elasticsearch://reference/elasticsearch/roles.md#built-in-roles-ml-admin) in {{stack}} or the appropriate [user role](/deploy-manage/users-roles/cloud-organization/user-roles.md) in {{serverless-short}}.
* The selected {{ml}} job to be running for the rule to function correctly.
::::

::::{tip}
For an overview of using {{ml}} with {{elastic-sec}}, refer to [Anomaly detection](/solutions/security/advanced-entity-analytics/anomaly-detection.md).
::::

## Create the rule

1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Create new rule**.
2. To create a rule based on a {{ml}} anomaly threshold, select **Machine Learning** on the **Create new rule** page, then select:

    1. The required {{ml}} jobs.

    ::::{note}
    If a required job isn't currently running, it will automatically start when you finish configuring and enable the rule.
    ::::

    ::::{warning}
    **{{ml-cap}} job startup considerations**:

    * **Startup time**: {{ml}} jobs take 30-60 seconds to fully start. Your rule may show a "Failed" status during the first few executions while the job initializes. This is normal behavior.
    * **Resource requirements**: Each {{ml}} job requires approximately 2GB RAM. Ensure you have dedicated ML nodes or sufficient memory on data nodes. In production environments, dedicated ML nodes are recommended.
    * **Baseline period**: Newly started {{ml}} jobs need 7-14 days to establish a baseline of normal behavior. Expect a higher volume of alerts initially as the job "learns" what is normal in your environment.
    * **Shared jobs**: If multiple rules use the same {{ml}} job, only one instance of the job runs. Stopping the job will cause all dependent rules to fail.

    **Best practice**: Start {{ml}} jobs manually in **Machine Learning → Anomaly Detection** and verify they're running before enabling {{ml}} detection rules in production.
    ::::

    2. The anomaly score threshold above which alerts are created.

3. (Optional) Use **Suppress alerts by** to reduce the number of repeated or duplicate alerts created by the rule. Refer to [Suppress detection alerts](/solutions/security/detect-and-alert/suppress-detection-alerts.md) for more information.

    ::::{note}
    Because {{ml}} rules generate alerts from anomalies, which don't contain source event fields, you can only use anomaly fields when configuring alert suppression.
    ::::

4. (Optional) Add **Related integrations** to associate the rule with one or more [Elastic integrations](https://docs.elastic.co/en/integrations). This indicates the rule's dependency on specific integrations and the data they generate, and allows users to confirm each integration's [installation status](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-prerequisites) when viewing the rule.

    1. Click **Add integration**, then select an integration from the list. You can also start typing an integration's name to find it faster.
    2. Enter the version of the integration you want to associate with the rule, using [semantic versioning](https://semver.org/). For version ranges, you must use tilde or caret syntax. For example, `~1.2.3` is from 1.2.3 to any patch version less than 1.3.0, and `^1.2.3` is from 1.2.3 to any minor and patch version less than 2.0.0.

5. Click **Continue** to [configure basic rule settings](/solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-basic-params).

::::{tip}
To filter noisy {{ml}} rules, use [rule exceptions](/solutions/security/detect-and-alert/rule-exceptions.md).
::::

