:::{note}
:applies_to: { stack: ga 9.4+, serverless: ga }

If the integration you're adding declares a minimum {{agent}} version requirement and some or all agents enrolled in the target policy don't meet that requirement, a warning indicates that these agents aren't compatible with the integration.

You can still add the integration to the policy. If you later upgrade your agents or enroll new agents that meet the minimum version requirement, they receive the integration configuration automatically. For more information, refer to [Version-specific agent policies](/reference/fleet/version-specific-agent-policies.md).
:::