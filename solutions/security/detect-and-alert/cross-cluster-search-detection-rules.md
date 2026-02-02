---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/rules-cross-cluster-search.html
applies_to:
  stack: all
products:
  - id: security
---

# Cross-cluster search and detection rules [rules-cross-cluster-search]

[Cross-cluster search](/explore-analyze/cross-cluster-search.md) is an {{es}} feature that allows one cluster (the *local* cluster) to query data in a separate cluster (the *remote* cluster). {{elastic-sec}}'s detection rules can perform a cross-cluster search to query data in remote clusters.

::::{admonition} Requirements
* To learn about the requirements for using cross-cluster search in the {{stack}}, refer to [Cross-cluster search](/explore-analyze/cross-cluster-search.md). 
* Using cross-cluster search for {{esql}} rules in the {{stack}} requires an [Enterprise subscription](https://www.elastic.co/pricing). 

::::

## Set up cross-cluster search in detection rules [set-up-ccs-rules]

This section explains the general process for setting up cross-cluster search in detection rules. For specific instructions on each part of the process, refer to the linked documentation.

1. On the local cluster, establish trust and set up a connection to the remote cluster, using one of the following methods. With either method, note the unique name that you give to the remote cluster, because you’ll need to use it throughout this process.

    * [Add remote clusters using API key authentication](../../../deploy-manage/remote-clusters/remote-clusters-api-key.md) — Clusters must be on {{stack}} version 8.14 or later.
    * [Add remote clusters using TLS certificate authentication](../../../deploy-manage/remote-clusters/remote-clusters-cert.md)

2. On both the local and remote clusters, [create a role for cross-cluster search privileges](../../../deploy-manage/remote-clusters/remote-clusters-cert.md#clusters-privileges-ccs-kibana-cert), and make sure the two roles have *identical* names. Assign each role the following privileges:

    1. **Local cluster role**: Assign the `read` privilege to the indices you want to search, using *both* the local and remote index patterns for each index. To specify a remote index, use the pattern `<remote_cluster_name>:<index_name>`.

        For example, if the remote cluster’s name is `remote-security-data` and you want to query the `logs-*` indices, include both the `logs-*` and `remote-security-data:logs-*` index patterns and assign them the `read` privilege.

        :::{image} /solutions/images/security-ccs-local-role.png
        :alt: Local cluster role configuration
        :screenshot:
        :::

    2. **Remote cluster role**: Assign the `read` and `read_cross_cluster` privileges to the indices you want to search. You don’t need to include the remote cluster’s name here.

        :::{image} /solutions/images/security-ccs-remote-role.png
        :alt: Remote cluster role configuration
        :screenshot:
        :::

3. On the local cluster:

    1. Assign the role you just created to a user who you want to configure your cross-cluster detection rules.

        ::::{important}
        * This step ensures that the privileges to read remote indices are applied from the user to the rule itself. When a user creates a new rule or saves edits to an existing rule, their current privileges are saved to the rule’s API key. If that user’s privileges change in the future, the rule’s API key will not update until you manually update it. Refer to [Update a rule’s API key](#update-api-key) for details.
        * This user must also have the [appropriate privileges](detections-requirements.md#enable-detections-ui) to manage and preview rules.

        ::::

    2. As this user, [configure a rule](create-detection-rule.md) that searches the remote indices: create or edit a rule, then enter the `<remote_cluster_name>:<index_name>` pattern in the **Source** section.

        :::{image} /solutions/images/security-ccs-rule-source.png
        :alt: Rule source configuration
        :screenshot:
        :::

        ::::{note}
        If the rule’s **Source** uses a data view instead of index patterns, you must define the data view for cross-cluster search separately, using the `<remote_cluster_name>:<index_name>` pattern. Refer to [Use data views with cross-cluster search](../../../explore-analyze/find-and-organize/data-views.md#management-cross-cluster-search) for more on defining a data view.
        ::::

    3. (Optional) [Preview the rule](create-detection-rule.md#preview-rules) to test its expected results.

        ::::{important}
        The rule preview uses the current user’s cross-cluster search privileges, while the rule itself runs using the privileges snapshot saved in its API key the moment the key is created. The preview results could be different from the rule’s actual behavior if the user performing the preview has different privileges than what’s saved in the rule’s API key.
        ::::

    4. Save and enable the rule.



## Update a rule’s API key [update-api-key]

Each detection rule has its own [API key](../../../explore-analyze/alerts-cases/alerts/alerting-setup.md#alerting-authorization), which determines the data and actions the rule is allowed to access. When a user creates a new rule or changes an existing rule, their current privileges are saved to the rule’s API key. If that user’s privileges change in the future, the rule **does not** automatically update with the user’s latest privileges — you must update the rule’s API key if you want to update its privileges.

::::{important}
A rule’s API key is different from the API key you might have created for [authentication between local and remote clusters](#set-up-ccs-rules).
::::


To update a rule’s API key, log into the local cluster as a user with the privileges you want to apply to the rule, then do either of the following:

* Edit and save the rule.
* Update the rule’s API key manually:

    1. Find **Stack Management** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Rules**.
    2. Use the search box and filters to find the rules you want to update. For example, use the **Type** filter to find rules under the **Security** category.
    3. Select the rule’s actions menu (**…**), then **Update API key**.

        ::::{tip}
        To update multiple rules, select their checkboxes, then click **Selected *x* rules** → **Update API keys**.
        ::::
