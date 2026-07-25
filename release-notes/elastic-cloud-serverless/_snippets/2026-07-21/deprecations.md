## July 21, 2026 [elastic-2026-07-21-deprecations]

* Deprecate `include_comments` in the `cases.getCase` workflow step.
  For more information, check [#277542](https://github.com/elastic/kibana/pull/277542).

  **Impact:** Workflows that set `include_comments` continue to work for now, but the field is marked deprecated and may be removed in a later release.

  **Action:** Stop relying on `include_comments` in new workflows. Use the unified attachment APIs when you need case attachments beyond the legacy comments contract.

