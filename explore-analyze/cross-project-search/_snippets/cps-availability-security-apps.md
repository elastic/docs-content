<!-- TODO (docs-content#8050): Three entries below are contested by the CPS GA issue and could not be resolved against Kibana source at HEAD. Hold them until Security PM (@chuddy-elastic) confirms:

1. Entity store. The current bullet saying entity profiles exclude linked-project data is wrong, but the issue's claim that retrieval federates across every linked project's entity store is also wrong. Source pins entity retrieval to `_alias:_origin`; linked-project data reaches the origin store through CPS log extraction and relationship maintainers instead. Risk scoring and entity resolution stay origin-only. Rewrite once the intended user-facing framing is settled.

2. Defend and Osquery. Cross-project read support exists but is gated behind `defendCrossProjectSearch` and Osquery's `crossProjectSearch`, both defaulting to false, layered on `cps.cpsEnabled`. Only read paths fan out. Policies, artifacts, response action dispatch, and saved queries and packs stay per project through Fleet. Confirm whether the flags ship on by default at GA before changing "origin only".

3. Flyouts and Session Viewer. The issue says Session Viewer flyouts are unsupported. No code-level block was found. Session Viewer qualifies the remote index, and a generic callout reads "This alert originates from a linked project. Some features may not be available." Need a concrete repro before naming Session Viewer specifically.

Also pending from the same issue: a "Using cross-project search with Elastic Security" guidance page, blocked on the PM support doc.
-->

{{elastic-sec}} apps have partial {{cps-init}} support. The following features work across linked projects:

- **Detection rules:** Rules that run on the origin project query data across linked projects and write the alerts they generate back to the origin project. This lets a single project hold your detections and alert triage while the data stays in the projects that produce it. {{ml-cap}} rules are an exception and search the origin project only. For details, refer to [{{cps-cap}} and detection rules](/solutions/security/detect-and-alert/cross-project-search-detection-rules.md).
- **Timeline:** Tables display documents from linked projects. Actions that don't apply to remote documents are disabled.
- **Alert, event, and attack flyouts:** Flyouts render correctly for documents from linked projects. Remote documents are clearly identified, and actions that don't apply to remote documents are hidden or disabled. Investigate in Timeline remains available.
- **Explore page:** Host, network, and user exploration searches follow the {{cps-init}} scope configured for the space, so they can return events from linked projects.
- **Overview page:** The event widgets on the Security Overview page follow the {{cps-init}} scope configured for the space. The alert widgets show origin project alerts only.
- **Dashboards:** The Detection & Response and Data Quality dashboards support {{cps-init}}.
- **Intelligence:** Threat intelligence indicator searches support {{cps-init}}.

The following features remain scoped to the origin project:

- **Alerts:** The Alerts page doesn't display alerts that a linked project generated on its own. Origin project rules write the alerts they create from linked project data to the origin project, so those alerts do appear here.
- **Cases:** Cases are stored in the origin project. You can't attach an alert or event from a linked project to a case.
- **Entity store:** Entity risk scoring and entity profiles do not include data from linked projects.
- **Attack Discovery:** AI-generated attack discoveries are based on alerts from the origin project only.
- **Defend and Osquery:** Elastic Defend and Osquery are scoped to the origin project only. Defend and Osquery are managed through Fleet, meaning their configuration is tied to a single project. Endpoint artifacts, policies, response actions, and Osquery saved queries and packs are managed per project and are not shared across linked projects.
