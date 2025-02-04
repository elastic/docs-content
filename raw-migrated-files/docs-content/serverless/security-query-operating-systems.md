# Osquery [security-query-operating-systems]

Osquery is an open source tool that lets you use SQL to query operating systems like a database. When you add the [Osquery manager integration](../../../solutions/security/investigate/manage-integration.md) to an {{agent}} policy, Osquery is deployed to all agents assigned to that policy. After completing this setup, you can [run live queries and schedule recurring queries](../../../solutions/security/investigate/osquery.md) for agents and begin gathering data from your entire environment.

Osquery is supported for Linux, macOS, and Windows. You can use it with {{elastic-sec}} to perform real-time incident response, threat hunting, and monitoring to detect vulnerability or compliance issues. The following Osquery features are available from {{elastic-sec}}:

* [Osquery Response Actions](../../../solutions/security/investigate/add-osquery-response-actions.md) - Use Osquery Response Actions to add live queries to custom query rules.
* [Live queries from investigation guides](../../../solutions/security/investigate/run-osquery-from-investigation-guides.md) - Incorporate live queries into investigation guides to enhance your research capabilities while investigating possible security issues.
* [Live queries from alerts](../../../solutions/security/investigate/run-osquery-from-alerts.md) - Run live queries against an alert’s host to learn more about your infrastructure and operating systems.
* [Osquery settings](../../../solutions/security/investigate/osquery.md) - Navigate to **Investigations** → **Osquery** to manage project-level Osquery settings.
