## June 30, 2026 [elastic-2026-06-30-breaking-changes]

::::{dropdown} Add AgentlessPolicy response model and remove legacy fields from Agentless API
  For more information, check [#272894](https://github.com/elastic/kibana/pull/272894).

  **Impact:** Changes `POST /api/fleet/agentless_policies` to return a new dedicated `AgentlessPolicy` response model instead of the internal `PackagePolicy` shape. Removes the `format` query parameter. The following request body fields are no longer accepted: `description`, `var_group_selections`, `additional_datastreams_permissions`, and `condition`.

  **Action:** External API clients that consume `PackagePolicy` fields such as `policy_ids`, `revision`, `supports_agentless`, `secret_references`, `output_id`, `fleet_server_host_id`, or `enabled` from the response must migrate to the new model.
::::
