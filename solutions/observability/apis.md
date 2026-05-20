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

* Alerting API ([Stack]({{kib-apis}}group/endpoint-alerting) | [Serverless]({{kib-serverless-apis}}group/endpoint-alerting)): Create and manage alerting rules, and their alerts and actions.
* APM agent configuration API ([Stack]({{kib-apis}}group/endpoint-apm-agent-configuration) | [Serverless]({{kib-serverless-apis}}group/endpoint-apm-agent-configuration)): Adjust APM agent configuration without redeploying your application.
* APM agent keys API ([Stack]({{kib-apis}}group/endpoint-apm-agent-keys) | [Serverless]({{kib-serverless-apis}}group/endpoint-apm-agent-keys)): Create APM agent keys to authorize requests from APM agents to APM Server.
* APM annotations API ([Stack]({{kib-apis}}group/endpoint-apm-annotations) | [Serverless]({{kib-serverless-apis}}group/endpoint-apm-annotations)): Create and search for annotations on APM visualizations.
* APM sourcemaps API ([Stack]({{kib-apis}}group/endpoint-apm-sourcemaps) | [Serverless]({{kib-serverless-apis}}group/endpoint-apm-sourcemaps)): Upload and manage APM source maps.
* [Cases API]({{kib-apis}}group/endpoint-cases): Open and manage cases.
* Connectors API ([Stack]({{kib-apis}}group/endpoint-connectors) | [Serverless]({{kib-serverless-apis}}group/endpoint-connectors)): Create and manage connectors for use with alerting rules and cases.
* Observability AI Assistant API ([Stack]({{kib-apis}}group/endpoint-observability_ai_assistant) | [Serverless]({{kib-serverless-apis}}group/endpoint-observability_ai_assistant)): Interact with the Observability AI Assistant.
* SLOs API ([Stack]({{kib-apis}}group/endpoint-slo) | [Serverless]({{kib-serverless-apis}}group/endpoint-slo)): Define, manage, and track service-level objectives.
* Streams API ([Stack]({{kib-apis}}group/endpoint-streams) | [Serverless]({{kib-serverless-apis}}group/endpoint-streams)): Create and manage streams.
* [Synthetics API]({{kib-apis}}group/endpoint-synthetics): Create and manage synthetic monitors, private locations, and parameters.
* [Uptime API]({{kib-apis}}group/endpoint-uptime): View and update uptime monitoring settings.

To view other APIs, such as {{kib}} or {{es}} APIs, refer to [Elastic APIs]({{apis}}).