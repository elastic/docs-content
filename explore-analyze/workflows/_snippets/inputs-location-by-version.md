The location of `inputs` in the YAML depends on your version:

- {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` `inputs` sits inside the `manual` trigger.
- {applies_to}`stack: preview 9.3, ga 9.4` `inputs` sits at the top level of the workflow.

The reference form `{{ inputs.<name> }}` is the same in either placement, and only the declaration moves. Refer to [Workflow anatomy](/explore-analyze/workflows/authoring-techniques/anatomy.md#workflows-anatomy-inputs) for the full reference.
