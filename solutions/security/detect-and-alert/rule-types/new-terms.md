---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/rules-ui-create.html#create-new-terms-rule
  - https://www.elastic.co/guide/en/serverless/current/security-rules-create.html#create-new-terms-rule
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Create a new terms rule [create-new-terms-rule]

New terms rules generate alerts for each new term detected in source documents within a specified time range. These rules are ideal for detecting first-time occurrences or never-before-seen combinations of field values.

**When to use**: Detect first-time occurrence of field values (e.g., "first time seeing this user/host combination", "new process name for this host", "previously unseen destination domain").

**Performance**: Medium resource usage (~300ms per execution). Maintains history of seen terms in memory.

## Create the rule

1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Create new rule**.
2. To create a rule that searches for each new term detected in source documents, select **New Terms** on the **Create new rule** page, then:

    1. Specify what data to search by entering individual {{es}} index patterns or selecting an existing data view.
    2. Use the filter and query fields to create the criteria used for detecting alerts.

        ::::{note}
        You can use saved queries and queries from saved Timelines (**Import query from saved Timeline**) as rule conditions.
        ::::

    3. Use the **Fields** menu to select a field to check for new terms. You can also select up to three fields to detect a combination of new terms (for example, a `host.ip` and `host.id` that have never been observed together before).

        ::::{important}
        When checking multiple fields, each unique combination of values from those fields is evaluated separately. For example, a document with `host.name: ["host-1", "host-2", "host-3"]` and `user.name: ["user-1", "user-2", "user-3"]` has 9 (3x3) unique combinations of `host.name` and `user.name`. A document with 11 values in `host.name` and 10 values in `user.name` has 110 (11x10) unique combinations. The new terms rule only evaluates 100 unique combinations per document, so selecting fields with large arrays of values might cause incorrect results.
        ::::

    4. Use the **History Window Size** menu to specify the time range to search in minutes, hours, or days to determine if a term is new. The history window size must be larger than the rule interval plus additional look-back time, because the rule will look for terms where the only time(s) the term appears within the history window is *also* within the rule interval and additional look-back time.

        For example, if a rule has an interval of 5 minutes, no additional look-back time, and a history window size of 7 days, a term will be considered new only if the time it appears within the last 7 days is also within the last 5 minutes. Configure the rule interval and additional look-back time when you [set the rule's schedule](/solutions/security/detect-and-alert/create-detection-rule.md#rule-schedule).

3. (Optional) Use **Suppress alerts by** to reduce the number of repeated or duplicate alerts created by the rule. Refer to [Suppress detection alerts](/solutions/security/detect-and-alert/suppress-detection-alerts.md) for more information.
4. (Optional) Create a list of **Required fields** that the rule needs to function. This list is informational only, to help users understand the rule; it doesn't affect how the rule actually runs.

    1. Click **Add required field**, then select a field from the index patterns or data view you specified for the rule. You can also start typing a field's name to find it faster, or type in an entirely new custom field.
    2. Enter the field's data type.

5. (Optional) Add **Related integrations** to associate the rule with one or more [Elastic integrations](https://docs.elastic.co/en/integrations). This indicates the rule's dependency on specific integrations and the data they generate, and allows users to confirm each integration's [installation status](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-prerequisites) when viewing the rule.

    1. Click **Add integration**, then select an integration from the list. You can also start typing an integration's name to find it faster.
    2. Enter the version of the integration you want to associate with the rule, using [semantic versioning](https://semver.org). For version ranges, you must use tilde or caret syntax. For example, `~1.2.3` is from 1.2.3 to any patch version less than 1.3.0, and `^1.2.3` is from 1.2.3 to any minor and patch version less than 2.0.0.

6. Click **Continue** to [configure basic rule settings](/solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-basic-params).

