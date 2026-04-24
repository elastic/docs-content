{{elastic-sec}} apps have partial {{cps-init}} support. The following features work across linked projects:

- **Timeline:** All tabs, including non-{{esql}} tabs, return results from remote projects.
- **Alerts:** The Alerts page displays remote alerts, and the alert details flyout renders correctly for alerts from linked projects.
- **Dashboards:** The Detection & Response and Data Quality dashboards support {{cps-init}}.
- **Intelligence:** Threat Intel workflows support {{cps-init}}.

The following features remain scoped to the origin project:

- **Explore page:** Host, network, and user exploration searches are scoped to the origin project only.
- **Entity store:** Entity risk scoring and entity profiles do not include data from linked projects.
- **Attack Discovery**: AI-generated attack discoveries are based on alerts from the origin project only.
- **Overview**: The Security Overview page reflects data from the origin project only.