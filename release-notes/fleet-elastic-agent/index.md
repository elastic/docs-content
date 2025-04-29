---
navigation_title: "Fleet and Elastic Agent"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/release-notes.html
---

# {{fleet}} and {{agent}} release notes [fleet-elastic-agent-release-notes]

Review the changes, fixes, and more in each version of {{fleet}} and {{agent}}.

To check for security updates, go to [Security announcements for the Elastic stack](https://discuss.elastic.co/c/announcements/security-announcements/31).

{{agent}} integrates and manages {{beats}} for data collection, and Beats changes may impact {{agent}} functionality. To check for {{agent}} changes in {{beats}}, go to [{{beats}} release notes](beats://release-notes/index.md).

% Release notes include only features, enhancements, and fixes. Add breaking changes, deprecations, and known issues to the applicable release notes sections.
% For each new version section, include the Fleet and Elastic Agent and Kibana changes.

% ## version.next [fleet-elastic-agent-next-release-notes]

% ### Features and enhancements [fleet-elastic-agent-next-features-enhancements]
% *

% ### Fixes [fleet-elastic-agent-next-fixes]
% *


## 9.0.0 [fleet-elastic-agent-900-release-notes]

### Features and enhancements [fleet-elastic-agent-900-features-enhancements]
* New setting allowing automatic deletion of unenrolled agents in Fleet settings [#195544]({{kib-pull}}195544)
* Adds the Azure Asset Inventory definition to Cloudbeat for {{agent}} [#5323]({{agent-pull}}5323)
* Adds Kubernetes deployment of the Elastic Distribution of OTel Collector named "gateway" to the Helm kube-stack deployment for {{agent}} [#6444]({{agent-pull}}6444)
* Adds the filesource provider to composable inputs. The provider watches for changes of the files and updates the values of the variables when the content of the file changes for {{agent}} [#6587]({{agent-pull}}6587) and [#6362]({{agent-issue}}6362)
* Adds the jmxreceiver to the Elastic Distribution of OTel Collector for {{agent}} [#6601]({{agent-pull}}6601)
* Adds support for context variables in outputs as well as a default provider prefix for {{agent}} [#6602]({{agent-pull}}6602) and [#6376]({{agent-issue}}6376)
* Adds the Nginx receiver and Redis receiver OTel components for {{agent}} [#6627]({{agent-pull}}6627)
* Adds --id (ELASTIC_AGENT_ID environment variable for container) and --replace-token (FLEET_REPLACE_TOKEN environment variable for container) enrollment options for {{agent}} [#6498]({{agent-pull}}6498)
* Updates Go version to 1.22.10 in {{agent}} [#6236]({{agent-pull}}6236)
* Improves filtering and visibility of Uninstalled and Orphaned agents in {{fleet}}, by differentiating them from Offline agents [#205815]({{kib-pull}}205815)
* Introduces air-gapped configuration for bundled packages in {{fleet}} [#202435]({{kib-pull}}202435)
* Updates removed parameters of the {{fleet}} -> {{ls}} output configurations [#210115]({{kib-pull}}210115)
* Updates the maximum supported package version in {{fleet}} [#196675]({{kib-pull}}196675)
* Replaces the use of context.TODO and context.Background in logger function calls for most {{fleet-server}} use cases [#4168]({{fleet-server-pull}}4168) and [#3087]({{fleet-server-issue}}3087)
* Refactor the {{fleet-server}} API constructor to use functional opts instead of a long list of pointers [#4169]({{fleet-server-pull}}4169) and [#3823]({{fleet-server-issue}}3823)
* Removes the deprecated policy_throttle configuration setting in favour of the newer policy-limit for {{fleet-server}} [#4288]({{fleet-server-pull}}4288)
* Adds the ability for {{agent}} to enroll using a specific ID [#4290]({{fleet-server-pull}}4290) and [#4226]({{fleet-server-issue}}4226)
* Adds the Filebeat receiver into {{agent}} [#5833]({{agent-pull}}5833)
* Updates OTel components to v0.119.0 in {{agent}} [#6713]({{agent-pull}}6713)
* Removes old bundled.yaml from oas, fixed tags [#194788]({{kib-pull}}194788)

### Fixes [fleet-elastic-agent-900-fixes]
* Fixes a validation error that occurs on multi-text input fields in {{fleet}} [#205768]({{kib-pull}}205768)
* Adds a context timeout to the bulker flush in {{fleet-server}} so it times out if it takes more time than the deadline [#3986]({{fleet-server-pull}}3986)
* Removes a race condition that may occur when remote {{es}} outputs are used in {{fleet-server}} [#4171]({{fleet-server-pull}}4171)
* Uses the chi/middleware.Throttle package to track in-flight requests and return a 429 response when the limit is reached in {{fleet-server}} [#4402]({{fleet-server-pull}}4402) and [#4400]({{fleet-server-issue}}4400)
* Fixes logical race conditions in the kubernetes_secrets provider in {{agent}} [#6623]({{agent-pull}}6623)
* Resolves the proxy to inject into agent component configurations using the Go http package in {{agent}} [#6675]({{agent-pull}}6675) and [#6209]({{agent-issue}}6209)




