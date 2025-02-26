---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/migrate-auditbeat-to-agent.html
---

# Migrate from Auditbeat to Elastic Agent [migrate-auditbeat-to-agent]

Before you begin, read [*Migrate from {{beats}} to {{agent}}*](/reference/ingestion-tools/fleet/migrate-from-beats-to-elastic-agent.md) to learn how to deploy {{agent}} and install integrations.

Then come back to this page to learn about the integrations available to replace functionality provided by {{auditbeat}}.


## Compatibility [compatibility]

The integrations that provide replacements for `auditd` and `file_integrity` modules are only available in {{stack}} version 8.3 and later.


## Replace {{auditbeat}} modules with {{agent}} integrations [use-integrations]

The following table describes the integrations you can use instead of {{auditbeat}} modules and datasets.

| If you use…​ | You can use this instead…​ | Notes |
| --- | --- | --- |
| [Auditd](beats://docs/reference/auditbeat/auditbeat-module-auditd.md) module | [Auditd Manager](integration-docs://docs/reference/auditd_manager.md) integration | This integration is a direct replacement of the module. You can port rules andconfiguration to this integration. Starting in {{stack}} 8.4, you can also set the`immutable` flag in the audit configuration. |
| [Auditd Logs](integration-docs://docs/reference/auditd.md) integration | Use this integration if you don’t need to manage rules. It only parses logs fromthe audit daemon `auditd`. Please note that the events created by this integrationare different than the ones created by[Auditd Manager](integration-docs://docs/reference/auditd_manager.md), since the latter merges allrelated messages in a single event while [Auditd Logs](integration-docs://docs/reference/auditd.md)creates one event per message. |
| [File Integrity](beats://docs/reference/auditbeat/auditbeat-module-file_integrity.md) module | [File Integrity Monitoring](integration-docs://docs/reference/fim.md) integration | This integration is a direct replacement of the module. It reports real-timeevents, but cannot report who made the changes. If you need to track thisinformation, use [{{elastic-defend}}](/reference/security/elastic-defend/install-endpoint.md)instead. |
| [System](beats://docs/reference/auditbeat/auditbeat-module-system.md) module | It depends…​ | There is not a single integration that collects all this information. |
| [System.host](beats://docs/reference/auditbeat/auditbeat-dataset-system-host.md) dataset | [Osquery](integration-docs://docs/reference/osquery.md) or [Osquery Manager](integration-docs://docs/reference/osquery_manager.md) integration | Schedule collection of information like:<br><br>* [system_info](https://www.osquery.io/schema/5.1.0/#system_info) for hostname, unique ID, and architecture<br>* [os_version](https://www.osquery.io/schema/5.1.0/#os_version)<br>* [interface_addresses](https://www.osquery.io/schema/5.1.0/#interface_addresses) for IPs and MACs<br> |
| [System.login](beats://docs/reference/auditbeat/auditbeat-dataset-system-login.md) dataset | [Endpoint](/reference/security/elastic-defend/install-endpoint.md) | Report login events. |
| [Osquery](integration-docs://docs/reference/osquery.md) or [Osquery Manager](integration-docs://docs/reference/osquery_manager.md) integration | Use the [last](https://www.osquery.io/schema/5.1.0/#last) table for Linux and macOS. |
| {{fleet}} [system](integration-docs://docs/reference/system.md) integration | Collect login events for Windows through the [Security event log](integration-docs://docs/reference/system.md#system-security). |
| [System.package](beats://docs/reference/auditbeat/auditbeat-dataset-system-package.md) dataset | [System Audit](integration-docs://docs/reference/system_audit.md) integration | This integration is a direct replacement of the System Package dataset. Starting in {{stack}} 8.7, you can port rules and configuration settings to this integration. This integration currently schedules collection of information such as:<br><br>* [rpm_packages](https://www.osquery.io/schema/5.1.0/#rpm_packages)<br>* [deb_packages](https://www.osquery.io/schema/5.1.0/#deb_packages)<br>* [homebrew_packages](https://www.osquery.io/schema/5.1.0/#homebrew_packages)<br> |
| [Osquery](integration-docs://docs/reference/osquery.md) or [Osquery Manager](integration-docs://docs/reference/osquery_manager.md) integration | Schedule collection of information like:<br><br>* [rpm_packages](https://www.osquery.io/schema/5.1.0/#rpm_packages)<br>* [deb_packages](https://www.osquery.io/schema/5.1.0/#deb_packages)<br>* [homebrew_packages](https://www.osquery.io/schema/5.1.0/#homebrew_packages)<br>* [apps](https://www.osquery.io/schema/5.1.0/#apps) (MacOS)<br>* [programs](https://www.osquery.io/schema/5.1.0/#programs) (Windows)<br>* [npm_packages](https://www.osquery.io/schema/5.1.0/#npm_packages)<br>* [atom_packages](https://www.osquery.io/schema/5.1.0/#atom_packages)<br>* [chocolatey_packages](https://www.osquery.io/schema/5.1.0/#chocolatey_packages)<br>* [portage_packages](https://www.osquery.io/schema/5.1.0/#portage_packages)<br>* [python_packages](https://www.osquery.io/schema/5.1.0/#python_packages)<br> |
| [System.process](beats://docs/reference/auditbeat/auditbeat-dataset-system-process.md) dataset | [Endpoint](/reference/security/elastic-defend/install-endpoint.md) | Best replacement because out of the box it reports events forevery process in [ECS](ecs://docs/reference/index.md) format and has excellentintegration in [Kibana](/get-started/the-stack.md). |
| [Custom Windows event log](integration-docs://docs/reference/winlog.md) and{{integrations-docs}}/windows#sysmonoperational[Sysmon] integrations | Provide process data. |
| [Osquery](integration-docs://docs/reference/osquery.md) or[Osquery Manager](integration-docs://docs/reference/osquery_manager.md) integration | Collect data from the [process](https://www.osquery.io/schema/5.1.0/#process) table on some OSeswithout polling. |
| [System.socket](beats://docs/reference/auditbeat/auditbeat-dataset-system-socket.md) dataset | [Endpoint](/reference/security/elastic-defend/install-endpoint.md) | Best replacement because it supports monitoring network connections on Linux,Windows, and MacOS. Includes process and user metadata. Currently does notdo flow accounting (byte and packet counts) or domain name enrichment (but doescollect DNS queries separately). |
| [Osquery](integration-docs://docs/reference/osquery.md) or [Osquery Manager](integration-docs://docs/reference/osquery_manager.md) integration | Monitor socket events via the [socket_events](https://www.osquery.io/schema/5.1.0/#socket_events) tablefor Linux and MacOS. |
| [System.user](beats://docs/reference/auditbeat/auditbeat-dataset-system-user.md) dataset | [Osquery](integration-docs://docs/reference/osquery.md) or [Osquery Manager](integration-docs://docs/reference/osquery_manager.md) integration | Monitor local users via the [user](https://www.osquery.io/schema/5.1.0/#user) table for Linux, Windows, and MacOS. |

