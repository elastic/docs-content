---
applies_to:
  stack: ga 9.1
  serverless: ga
  elasticsearch:
products:
 - id: elasticsearch
---

# Query rules UI
Use query rules to pin or exclude specific documents when queries contain specific keywords or phrases, or match specific search patterns.
The Query rules UI provides a graphical interface to manage these rules without writing API calls or JSON configuration.

The UI enables you to:

- Set keyword or numerical conditions. For a full list of options, refer to [Rule criteria](elasticsearch://reference/elasticsearch/rest-apis/searching-with-query-rules.md#query-rule-criteria).
- Pin or exclude specific documents in results
- Organize rules into rulesets and set execution priority
- Test rules against sample queries before publishing

## UI versus API: What's the difference?

The Query Rules UI provides the same functionality as the API with one key difference:

* The UI defaults to `docs` for creating and editing rules. You cannot edit an `id` based rule that was created through the API.

For examples of how to search using query rules, refer to [Search using Query Rules API](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/searching-with-query-rules).

If you prefer to use the Query Rules API, refer to [Query Rules API]({{es-apis}}group/endpoint-query_rules).

## Requirements

For full access to the Query Rules UI, you need the following privileges:

* Appropriate roles to access Kibana. For more information, refer to [Built-in roles](elasticsearch://reference/elasticsearch/roles.md) or  [Kibana privileges](https://www.elastic.co/docs/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges)
* A role with `manage_search_query_rules` cluster privilege
* `ALL` option for `Query Rules` role privilege in the respective Kibana space

## Accessing the Query Rules UI

Go to the **Query Rules** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). If the option does not appear, contact your administrator to review your privileges.

### Create a query rule
Use the following steps to first create a query ruleset, and then a query rule:

1. Select **Query Rules** in the navigation menu under **Relevance**.
2. Select **Create ruleset**:
	- Enter a name for the ruleset.
	- Select **Create ruleset** to confirm.
3. When the rule creation section opens, select one of the following rule types:
	- **Pin**: Pin selected documents to the top of the search results.
	- **Exclude**: Exclude selected documents from the results.
   
   For more information on rule types, refer to [Rule types](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/searching-with-query-rules#query-rule-type).
4. Select one or more documents for the rule to apply to.
5. Select one of the following rule criteria:
    - **Always**: Apply the rule to all queries
    - **Custom**: Define conditions when the rule is applied.

   For a full list of options, refer to [Rule criteria](elasticsearch://reference/elasticsearch/rest-apis/searching-with-query-rules.md#query-rule-criteria).
6. Select **Create rule**.
7. Select **Save** in the top right corner of the ruleset section.

:::{note}
Each ruleset must contain at least one rule.
:::

### Delete a ruleset
Use the following steps to delete a query ruleset:
1. Select **Query Rules** in the navigation menu under **Relevance**.
2. Select **Delete** or select it from the action menu (**...**).
3. Select if the ruleset is safe to delete.
4. Select **Delete ruleset**.

### Manage existing rules
The following sections describe how to edit, delete, and re-order rules:

#### Edit a rule
Use the following steps to edit a query rule:
1. Select **Query Rules** in the navigation menu under **Relevance**.
2. Select a ruleset.
3. Select **Edit** from the action menu (**...**).
4. Apply changes to the rule.
5. Select **Update rule** to confirm your changes.
6. Select **Save** in the top right corner of the ruleset section.

:::{important}
Don't forget to save your changes, because unsaved rules are not applied.
:::

#### Delete a rule
Use the following steps to delete a query rule:
1. Select **Query Rules** in the navigation menu under **Relevance**.
2. Select a ruleset.
3. Select **Delete rule** from the action menu (**...**)
4. Select **Delete rule**.
5. Select **Save** in the top right corner of the ruleset section.

#### Re-order rules
Use the following steps to re-order query rules:
1. Select **Query Rules** in the navigation menu under **Relevance**.
2. Select a ruleset.
3. Drag a rule using the handle icon (≡) on the left.
4. Drop it in the new position.
5. Select **Save** in the top right corner of the ruleset section.

### Test and validate a ruleset
To test a query ruleset, do the following:
1. Select **Query Rules** in the navigation menu under **Relevance**.
2. Select a ruleset.
3. Select **Test in Console**.
4. Run the query.
5. Review results to confirm if the rule actions were applied as expected.


## Learn more

The following resources can help you understand query rules better:

Blogs:

- [Query rules blog](https://www.elastic.co/search-labs/blog/elasticsearch-query-rules-generally-available)
- [Semantic search for query rules](https://www.elastic.co/search-labs/blog/semantic-search-query-rules)

Other documentation links:
- [Query Rules API]({{es-apis}}group/endpoint-query_rules)
- [Search using query rules](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/searching-with-query-rules)
   - [Rule types](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/searching-with-query-rules#query-rule-type)
   - [Rule criteria](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/searching-with-query-rules#query-rule-criteria)
   - [Rule actions](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/searching-with-query-rules#query-rule-actions)

	

