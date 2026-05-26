{{elastic-sec}} apps have partial {{cps-init}} support. The following features work across linked projects:

- **Timeline:** Tables display documents from linked projects. Actions that don't apply to remote documents are disabled.
- **Alert, event, and attack flyouts:** Flyouts render correctly for documents from linked projects. Remote documents are clearly identified, and actions that don't apply to remote documents are hidden or disabled. Investigate in Timeline remains available.
- **Dashboards:** The Detection & Response and Data Quality dashboards support {{cps-init}}.
- **Intelligence:** Threat intelligence indicator searches support {{cps-init}}.

The following features remain scoped to the origin project:

- **Alerts:** The Alerts page does not display remote alerts from linked projects.
- **Explore page:** Host, network, and user exploration searches are scoped to the origin project only.
- **Entity store:** Entity risk scoring and entity profiles do not include data from linked projects.
- **Attack Discovery**: AI-generated attack discoveries are based on alerts from the origin project only.
- **Overview**: The Security Overview page reflects data from the origin project only.
- **Defend and Osquery**: Elastic Defend and Osquery are scoped to the origin project only. Defend and Osquery are managed through Fleet, meaning their configuration is tied to a single project. Endpoint artifacts, policies, response actions, and Osquery saved queries and packs are managed per project and are not shared across linked projects.