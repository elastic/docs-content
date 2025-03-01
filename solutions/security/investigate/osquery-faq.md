---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/osquery-faq.html
---

# Osquery FAQ [osquery-faq]

This list of frequently asked questions answers common questions about using Osquery in {{kib}}.


## How is Osquery Manager different from Osquery? [osquery-differences]

The Osquery Manager integration brings [Osquery](https://osquery.io/) capabilities to the Elastic Stack and makes it easier to manage Osquery across a large number of hosts. Most Osquery functionality works the same way in {{kib}} as it does when you deploy Osquery yourself. However, there are a few differences and known issues, outlined below.


## How do I grant Full Disk Access? [osquery-fda]

Full Disk Access (FDA) is required to fully query some tables on MacOS. Granting FDA is not yet supported for Osquery Manager. This impacts a small set of tables that access file directories that are restricted due to heightened permissions from Apple, including [file](https://osquery.io/schema/current#file), [file_events](https://osquery.io/schema/current#file_events), [es_process_events](https://osquery.io/schema/current#es_process_events), and any custom tables configured with [ATC](https://osquery.readthedocs.io/en/stable/deployment/configuration/#automatic-table-construction) that require access to these directories. When querying these tables, you won’t get results from the restricted directories.


## Why can’t I query the carves table? [osquery-carves]

File carving is not yet supported in the Elastic Stack, and [carves](https://osquery.io/schema/current#carves) table queries do not return results.


## Does the Osquery `.help` command work in {{kib}}? [osquery-help-command]

The [Osquery `.help` command](https://osquery.readthedocs.io/en/stable/introduction/sql/#shell-help) is not available when running live queries in {{kib}}. Instead, refer to the [Osquery schema](https://osquery.io/schema/) for all available tables, fields, and supported Operating Systems for each.


## Can I use Osquery extensions in {{kib}}? [osquery-extensions]

Osquery Manager does not currently support [Osquery extensions](https://osquery.readthedocs.io/en/stable/deployment/extensions/).


## Can I  do File Integrity Monitoring (FIM)? [osquery-fim]

Yes, you can set up [Osquery FIM](https://osquery.readthedocs.io/en/stable/deployment/file-integrity-monitoring/) using the Advanced configuration option for Osquery Manager (see [Customize Osquery configuration](manage-integration.md#osquery-custom-config)). However, Elastic also provides a [File Integrity Monitoring](https://docs.elastic.co/en/integrations/fim) integration for Elastic Agent, which might prove to be easier to configure than the current options available for Osquery Manager.


## Where can I get help with osquery syntax? [osquery-syntax]

Osquery uses a superset of SQLite for queries. To get started with osquery SQL, refer to the [Osquery documentation](https://osquery.readthedocs.io/en/stable/introduction/sql/). For help with more advanced questions, the Osquery community has an active Slack workspace and GitHub project. You can find links for both at [osquery.io](https://osquery.io/).


## How often is Osquery updated for Osquery Manager? [osquery-updates]

When a new [version of Osquery is released](https://github.com/osquery/osquery/releases), it is included in a subsequent Elastic Agent release and applied when the agent is upgraded. After that, when running queries from Osquery Manager in {{kib}}, the updated Osquery version is used. Refer to the Fleet and Elastic Agent Guide for help with [upgrading Fleet-managed Elastic Agents](/reference/ingestion-tools/fleet/upgrade-elastic-agent.md).

To check what Osquery version is installed on an Elastic Agent, you can run `SELECT version FROM osquery_info;` as a live query in {{kib}}. The `version` in the response is the Osquery version installed on the agent.

