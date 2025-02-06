---
applies:
  stack: ga 9.0
  serverless:
mapped_urls:
  - https://www.elastic.co/guide/en/kibana/current/xpack-spaces.html
  - https://www.elastic.co/guide/en/serverless/current/spaces.html
---

# Manage spaces [xpack-spaces]

% What needs to be done: Refine

% GitHub issue: https://github.com/elastic/docs-projects/issues/348

% Scope notes: Create a new landing page including the content that is relevant for both serverless and stateful Highlight the differences in subheadings for serverless and stateful Link to solution topics on spaces

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/kibana/kibana/xpack-spaces.md
% - [ ] ./raw-migrated-files/docs-content/serverless/spaces.md

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):

$$$spaces-control-feature-visibility$$$

$$$spaces-control-user-access$$$

$$$spaces-managing$$$

**Spaces** let you organize your content and users according to your needs.

- **\[Not available in serverless]** Each space has its own navigation.
- Each space has its own saved objects. 
- Users can only access the spaces that they have been granted access to. This access is based on user roles, and a given role can have different permissions per space.

{{kib}} creates a default space for you. When you create more spaces, users are asked to choose a space when they log in, and can change their current space at any time from the top menu.

:::{image} ../images/kibana-change-space.png
:alt: Change current space menu
:class: screenshot
:::

To go to **Spaces**, find **Stack Management** in the navigation menu or use the [global search bar](/get-started/the-stack.md#kibana-navigation-search).

Spaces provide different capabilities depending on the type of environment you're running:
- [Managing spaces in Kibana version 9.0.0 or later](manage-spaces/manage-spaces-stack.md)
- [Managing spaces in Elastic Cloud Serverless](manage-spaces/manage-spaces-serverless.md)