{{elastic-sec}} apps have partial {{cps-init}} support. The following features work across linked projects:

- **Detection rules:** Rules that run on the origin project query data across linked projects and write the alerts they generate back to the origin project. This lets a single project hold your detections and alert triage while the data stays in the projects that produce it. The **Max alerts per run** limit applies across all linked projects in the rule's scope. 

    :::{note}
    Rules run with the API key of the user who created or last updated them, so they need an {{ecloud}} API key to search across linked projects. For details, refer to [{{cps-cap}} and detection rules](/solutions/security/detect-and-alert/cross-project-search-detection-rules.md).
    :::

- **{{ml-cap}}:** {{anomaly-detect-cap}} job {{dfeeds}} and transforms can read data from linked projects. Jobs and results live on the origin project. {{ml-cap}} rules alert on those origin results, including anomalies produced from linked-project data.
- **Timeline:** Tables display documents from linked projects. Actions that don't apply to documents in linked projects are disabled.
- **Alert, event, and attack flyouts:** Flyouts render correctly for documents from linked projects. Documents in linked projects are clearly identified, and actions that don't apply to these documents are hidden or disabled. Investigate in Timeline remains available. Session View is not available for documents from linked projects.
- **Explore page:** Host, network, and user exploration searches follow the {{cps-init}} scope configured for the space, so they can return events from linked projects.
- **Overview page:** The event widgets on the Security Overview page follow the {{cps-init}} scope configured for the space. The alert widgets show origin project alerts only.
- **Dashboards:** The Detection & Response and Data Quality dashboards support {{cps-init}}.
- **Intelligence:** Threat intelligence indicator searches support {{cps-init}}.
- **Entity store:** Entity profiles on the origin project include entities extracted from linked-project data. Each project still builds its own store, and risk scoring stays on the origin project. A host that appears in more than one project is not combined into a single entity at the origin.
- **{{elastic-defend}} and Osquery:** The **Endpoints** page, host details, **Response actions history**, and Osquery query results include data from linked projects. Policies, artifacts, response action dispatch, and Osquery saved queries and packs stay per project because they're managed through Fleet.

The following features remain scoped to the origin project:

- **Alerts:** The Alerts page doesn't display alerts that a linked project generated on its own. Origin project rules write the alerts they create from linked project data to the origin project, so those alerts do appear here.
- **Cases:** Cases are stored in the origin project. You can't attach an alert or event from a linked project to a case.
- **Attack Discovery:** AI-generated attack discoveries are based on alerts from the origin project only.
- **Value report:** The **Value report** page reflects data from the origin project only.
- **SIEM Readiness:** SIEM Readiness assesses the data posture of the origin project only.
