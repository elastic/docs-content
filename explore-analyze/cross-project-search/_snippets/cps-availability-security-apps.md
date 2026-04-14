{{elastic-sec}} apps have limited {{cps-init}} support:

- **Timeline:** Only the **{{esql}}** tab supports `SET project_routing`. All other Timeline tabs search the origin project only.
- **Other Security features:** The **Explore** page, threat-hunting workflows, the alert details flyout, and entity store remain scoped to the origin project.
- **Alerting:** During technical preview, rules that query data across linked projects can generate alerts, and you can view those alerts in the UI. However, the alert response workflow, which includes actions after an alert is raised, such as triage, investigation, and case management across linked projects, is not yet fully supported with {{cps-init}}.
