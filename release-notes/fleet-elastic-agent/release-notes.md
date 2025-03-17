---
navigation_title: "Fleet and Elastic Agent"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/release-notes.html
---

# {{fleet}} and {{agent}} release notes [fleet-elastic-agent-release-notes]

Review the changes, fixes, and more in each version of {{fleet}} and {{agent}}.

To check for security updates, go to [Security announcements for the Elastic stack](https://discuss.elastic.co/c/announcements/security-announcements/31).

{{agent}} integrates and manages {{beats}} for data collection, and Beats changes may impact {{agent}} functionality. To check for {{agent}} changes in {{beats}}, go to [{{beats}} release notes](asciidocalypse://docs/beats/docs/release-notes/index.md).

% Release notes include only features, enhancements, and fixes. Add breaking changes, deprecations, and known issues to the applicable release notes sections.
% For each new version section, include the Fleet and Elastic Agent and Kibana changes.

% ## version.next [fleet-elastic-agent-next-release-notes]
% **Release date:** Month day, year

% ### Features and enhancements [fleet-elastic-agent-next-features-enhancements]
% *

% ### Fixes [fleet-elastic-agent-next-fixes]
% *


## 9.0.0 [fleet-elastic-agent-900-release-notes]
**Release date:** April 2, 2025

### Features and enhancements [fleet-elastic-agent-900-features-enhancements]
* New setting allowing automatic deletion of unenrolled agents in Fleet settings ({{kibana-pull}}195544[#195544])
* Adds the Azure Asset Inventory definition to Cloudbeat for {{agent}} {{agent-pull}}5323[#5323]
* Adds Kubernetes deployment of the Elastic Distribution of OTel Collector named "gateway" to the Helm kube-stack deployment for {{agent}} {{agent-pull}}6444[#6444]
* Adds the filesource providert to composable inputs. The provider watches for changes of the files and updates the values of the variables when the content of the file changes for {{agent}} {{agent-pull}}6587[#6587] and {{agent-issue}}6362[#6362]
* Adds the jmxreceiver to the Elastic Distribution of OTel Collector for {{agent}} {{agent-pull}}6601[#6601]
* Adds support for context variables in outputs as well as a default provider prefix for {{agent}} {{agent-pull}}6602[#6602] and {{agent-issue}}6376[#6376]
* Adds the Nginx receiver and Redis receiver OTel components for {{agent}} {{agent-pull}}6627[#6627]
* Adds `--id` (`ELASTIC_AGENT_ID` environment variable for container) and `--replace-token` (`FLEET_REPLACE_TOKEN` environment variable for container) enrollment options for {{agent}} {{agent-pull}}6498[#6498]
* Updates Go version to 1.22.10 in {{agent}} {{agent-pull}}6236[#6236]
* Improves filtering and visibility of `Uninstalled` and `Orphaned` agents in {{fleet}}, by differentiating them from `Offline` agents {{kibana-pull}}205815[#205815]
* Introduces air-gapped configuration for bundled packages in {{fleet}} {{kibana-pull}}202435[#202435]
* Updates removed parameters of the {{fleet}} -> {{ls}} output configurations {{kibana-pull}}210115[#210115]
* Updates the maximum supported package version in {{fleet}} {{kibana-pull}}196675[#196675]
* Replaces the use of `context.TODO` and `context.Background` in logger function calls for most {{fleet-server}} use cases {{fleet-server-pull}}4168[#4168] {{fleet-server-issue}}3087[#3087]
* Refactor the {{fleet-server}} API constructor to use functional opts instead of a long list of pointers {{fleet-server-pull}}4169[#4169] {{fleet-server-issue}}3823[#3823]
* Removes the deprecated `policy_throttle` configuration setting in favour of the newer `policy-limit` for {{fleet-server}} {{fleet-server-pull}}4288[#4288]
* Adds the ability for {{agent}} to enroll using a specific ID {{fleet-server-pull}}4290[#4290] and {{fleet-server-issue}}4226[#4226]
* Adds the Filebeat receiver into {{agent}} {{agent-pull}}5833[#5833]
* Updates OTel components to v0.119.0 in {{agent}} {{agent-pull}}6713[#6713]
% * Removes old bundled.yaml from oas, fixed tags ({{kibana-pull}}194788[#194788])

### Fixes [fleet-elastic-agent-900-fixes]
* Fixes a validation error that occurs on multi-text input fields in {{fleet}} ({{kibana-pull}}205768[#205768])
* Adds a context timeout to the bulker flush in {{fleet-server}} so it times out if it takes more time than the deadline {{fleet-server-pull}}3986[#3986]
* Removes a race condition that may occur when remote {es} outputs are used in {{fleet-server}} {{fleet-server-pull}}4171[#4171]
* Uses the `chi/middleware.Throttle` package to track in-flight requests and return a 429 response when the limit is reached in {{fleet-server}} {{fleet-server-pull}}4402[#4402] and {fleet-server-issue}4400[#4400]
* Fixes logical race conditions in the `kubernetes_secrets` provider in {{agent}} {{agent-pull}}6623[#6623]
* Resolves the proxy to inject into agent component configurations using the Go `http` package in {{agent}} {{agent-pull}}6675[#6675] and {{agent-issue}}6209[#6209]




