### Configuration management

Follow these best practices for managing configuration:

* After initial installation or enrollment, manage most settings through {{fleet}} policies rather than CLI flags.
* Document your configuration to keep track of which settings are configured using CLI, environment variables, and policies.
* Test policy changes in a non-production environment before applying to production.
* For containerized deployments, use environment variables to provide host-specific settings while keeping policies generic.