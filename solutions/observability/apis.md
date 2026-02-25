---
applies_to:
  stack: all
  serverless:
    observability: all
navigation_title: APIs
products:
  - id: observability
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# {{observability}} APIs

You can use these APIs to interface with {{observability}} features:

* [Alerting API]({{kib-apis}}group/endpoint-alerting): Create and manage alerting rules, and their alerts and actions.
* [APM agent configuration API]({{kib-apis}}group/endpoint-apm-agent-configuration): Adjust APM agent configuration without redeploying your application.
* [APM agent keys API]({{kib-apis}}group/endpoint-apm-agent-keys): Create APM agent keys to authorize requests from APM agents to APM Server.
* [APM annotations API]({{kib-apis}}group/endpoint-apm-annotations): Create and search for annotations on APM visualizations.
* [APM sourcemaps API]({{kib-apis}}group/endpoint-apm-sourcemaps): Upload and manage APM source maps.
* [Cases API]({{kib-apis}}group/endpoint-cases): Open and manage cases.
* [Connectors API]({{kib-apis}}group/endpoint-connectors): Create and manage connectors for use with alerting rules and cases.
* [Observability AI Assistant API]({{kib-apis}}group/endpoint-observability_ai_assistant): Interact with the Observability AI Assistant.
* [SLOs API]({{kib-apis}}group/endpoint-slo): Define, manage, and track service-level objectives.
* [Streams API]({{kib-apis}}group/endpoint-streams): Create and manage streams.
* [Synthetics API]({{kib-apis}}group/endpoint-synthetics): Create and manage synthetic monitors, private locations, and parameters.
* [Uptime API]({{kib-apis}}group/endpoint-uptime): View and update uptime monitoring settings.

To view other APIs, such as {{kib}} or {{es}} APIs, refer to [Elastic APIs]({{apis}}).