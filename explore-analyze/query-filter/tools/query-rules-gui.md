---
applies_to:
  stack: ga 9.1
  serverless: ga
---
# Query rules GUI

Query rules GUI is a user interface that helps you create, edit, and delete query rules. The interface is implemented on top of the existing Query Rules API and provides non-technical users with an intuitive, streamlined interface to manage query rules.

Query rules help customize search results, giving you more control over how results are returned based on the contextual information in the query. For more information on query rules, refer to our [Query Rules blog](https://www.elastic.co/search-labs/blog/elasticsearch-query-rules-generally-available).

You can do the following using the GUI without the need of any API calls:

* For a new deployment setup, create new rules
* For an existing deployment setup, edit and delete rules
* Reorder rules in a query ruleset

If you'd still prefer to use the Query Rules API, refer to [Query Rules API](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-query_rules).
For examples how to search using query rules, refer [Search using Query Rules API](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/searching-with-query-rules).

## Security privileges

If you want to get full access to the Query Rules GUI, you must have the following privileges:

* Appropriate roles to access Kibana. For more information, refer to [Built-in roles](https://www.elastic.co/docs/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles) or  [Kibana privileges](https://www.elastic.co/docs/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges)
* A custom role with `manage_search_query_rules` cluster privilege
* `ALL` option for `Query Rules` role privilege in the respective Kibana space

## GUI vs. API: What's the difference?

All the functionality in the GUI works the same as in API calls. The only difference is that the Query Rules GUI will create pinning by `docs` over `ids`. It'll still allow edits in a simple form for `id` pinning. For more information on Rule actions, refer [Rule actions](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/searching-with-query-rules#query-rule-actions).

## Using the GUI

Go to your hosted deployment and select **Query Rules** from the left navigation menu. If you're not able to see the option, contact the administrator to review the role assigned to you. The following screenshot shows the GUI for a new cloud hosted setup.

:::{image} /explore-analyze/images/query-rules-gui-home.png
:alt: Landing page for Query Rules GUI.
:screenshot:
:::

### Create a query rule

1. Select **Query Rules** in the navigation menu under **Relevance**.
2. Select **Create ruleset**:
	- Enter a name for the ruleset.
	- Select **Create ruleset** to confirm.
3. When the rule creation section opens, select one of the following rule types:
	- **Pin**: Pin selected documents to the top of the search results.
	- **Exclude**: Exclude selected documents from the results.
   
   For more information on rule types, refer [Rule types](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/searching-with-query-rules#query-rule-type).
4. Select one or more documents for the rule to apply to.
5. Select one of the following rule criteria:
    - **Always**: Apply the rule to all queries
    - **Custom**: Define conditions when the rule is applied.

   For a full list of options, refer [Rule criteria](elasticsearch://reference/elasticsearch/rest-apis/searching-with-query-rules.md#query-rule-criteria).
6. Select **Create rule**.
7. Select **Save** in the top right corner of the ruleset section.

:::{note}
Each ruleset must contain at least one rule.
:::

:::{image} /explore-analyze/images/elasticsearch-query-rules-create-rule.png
:alt: Creating a query rule.
:screenshot:
:::

### Delete a ruleset
1. Select **Query Rules** in the navigation menu under **Relevance**.
2. Select **Delete** or select it from the action menu (**...**).
3. Select if the ruleset is safe to delete.
4. Select **Delete ruleset**.

### Manage existing rules

#### Edit a rule
1. Select **Query Rules** in the navigation menu under **Relevance**.
2. Select a ruleset.
3. Select **Edit** from the action menu (**...**).
4. Apply changes to the rule.
5. Select **Update rule** to confirm your changes.
6. Select **Save** in the top right corner of the ruleset section.

:::{important}
After modifying any rules, make sure to save the changes in the ruleset section as well.
Unsaved rules will not be applied even if they're displayed in the UI.
:::

#### Delete a rule
1. Select **Query Rules** in the navigation menu under **Relevance**.
2. Select a ruleset.
3. Select **Delete rule** from the action menu (**...**)
4. Select **Delete rule**.
5. Select **Save** in the top right corner of the ruleset section.

#### Re-order rules

1. Select **Query Rules** in the navigation menu under **Relevance**.
2. Select a ruleset.
3. Drag a rule using the handle icon (≡) on the left.
4. Drop it in the new position.
5. Select **Save** in the top right corner of the ruleset section.

### Test and validate a ruleset

1. Select **Query Rules** in the navigation menu under **Relevance**.
2. Select a ruleset.
3. Select **Test in Console**.

	A console window opens containing a sample query using the [rule retriever](elasticsearch://reference/elasticsearch/rest-apis/retrievers/rule-retriever.md).

	```console
	GET books/_search
	{
	  "retriever": {
	    "rule": {
	      // Update your criteria to test different results
	      "match_criteria": {
	       "query_string": "Stephenson"
	     },
	      "ruleset_ids": [
	        "first-ruleset"
	      ],
	      "retriever": {
	        "standard": {
	          "query": {
	            "match_all": {} <1>
	          }
	        }
	      }
	    }
	  }
	}
	```
	1. Modify the search query if needed.

4. Run the query.
5. Review results to confirm if the rule actions were applied as expected.



