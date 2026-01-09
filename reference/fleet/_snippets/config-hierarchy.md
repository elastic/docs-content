The configuration precedence is as follows (highest to lowest):

1. CLI flags (during installation/enrollment)
2. Environment variables (during installation/enrollment)
3. Policy configuration (after enrollment, downloaded from {{fleet}})

Settings provided using CLI or environment variables during installation are used for the initial bootstrap or enrollment. After enrollment, {{component_ref}} downloads its policy from {{fleet}}, and policy settings take precedence for most configuration options (except those that must be provided using CLI or environment variables).