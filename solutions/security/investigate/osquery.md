---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/use-osquery.html
  - https://www.elastic.co/guide/en/serverless/current/security-query-operating-systems.html
  - https://www.elastic.co/guide/en/kibana/current/osquery.html
---

# Osquery

% What needs to be done: Refine

% Scope notes: Align serverless/stateful + combine with Kibana Osquery intro page

% Use migrated content from existing pages that map to this page:

% - [x] ./raw-migrated-files/security-docs/security/use-osquery.md
% - [ ] ./raw-migrated-files/docs-content/serverless/security-query-operating-systems.md
% - [ ] ./raw-migrated-files/kibana/kibana/osquery.md

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):

$$$osquery-map-fields$$$

$$$osquery-prebuilt-packs$$$

$$$osquery-manage-query$$$

$$$osquery-results$$$

$$$osquery-status$$$

$$$osquery-prebuilt-packs-queries$$$

Osquery is an open source tool that lets you use SQL to query operating systems like a database. When you add the [Osquery manager integration](/solutions/security/investigate/manage-integration.md) to an {{agent}} policy, Osquery is deployed to all agents assigned to that policy. After completing this setup, you can [run live queries and schedule recurring queries](/solutions/security/investigate/osquery.md) for agents and begin gathering data from your entire environment.

Osquery is supported for Linux, macOS, and Windows. You can use it with {{elastic-sec}} to perform real-time incident response, threat hunting, and monitoring to detect vulnerability or compliance issues. The following Osquery features are available from {{elastic-sec}}:

* **[Osquery Response Actions](/solutions/security/investigate/add-osquery-response-actions.md)** - Use Osquery Response Actions to add live queries to custom query rules.
* **[Live queries from investigation guides](/solutions/security/investigate/run-osquery-from-investigation-guides.md)** - Incorporate live queries into investigation guides to enhance your research capabilities while investigating possible security issues.
* **[Live queries from alerts](/solutions/security/investigate/run-osquery-from-alerts.md)** - Run live queries against an alert’s host to learn more about your infrastructure and operating systems.






