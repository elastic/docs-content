---
navigation_title: Fleet and Elastic Agent
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/release-notes.html
products:
  - id: fleet
  - id: elastic-agent
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

## 9.1.3 [fleet-elastic-agent-9.1.3-release-notes]

### Features and enhancements [fleet-elastic-agent-9.1.3-features-enhancements]

**Elastic Agent**

* Adjust the timeout for Elastic Defend check command. [#9213](https://github.com/elastic/elastic-agent/pull/9213)
* Update OTel components to v0.130.0. [#9362](https://github.com/elastic/elastic-agent/pull/9362)

### Fixes [fleet-elastic-agent-9.1.3-fixes]

**Elastic Agent**

* Upgrade Go version to 1.24.6. [#9287](https://github.com/elastic/elastic-agent/pull/9287)
* On Windows, retry saving the Agent information file to disk. [#9224](https://github.com/elastic/elastic-agent/pull/9224) [#5862](https://github.com/elastic/elastic-agent/issues/5862)

  Saving the Agent information file involves renaming/moving a file to its final destination. However, on Windows, it is sometimes not possible to rename/move a file to its destination file because the destination file is locked by another process (for example, an antivirus software). In such cases, we now retry the save operation on Windows.

* Correct hints annotations parsing to resolve only `${kubernetes.*}` placeholders instead of resolving all `${...}` patterns. [#9307](https://github.com/elastic/elastic-agent/pull/9307)
* Treat exit code 28 from Endpoint binary as non-fatal. [#9320](https://github.com/elastic/elastic-agent/pull/9320)
* Fixed jitter backoff strategy reset. [#9342](https://github.com/elastic/elastic-agent/pull/9342) [#8864](https://github.com/elastic/elastic-agent/issues/8864)
* Fix Docker container failing to start with `no matching vars: ${env.ELASTICSEARCH_API_KEY:}` and similar errors by restoring support for `:` to set default values. [#9451](https://github.com/elastic/elastic-agent/pull/9451) [#9328](https://github.com/elastic/elastic-agent/issues/9328)
* Fix deb upgrade by stopping `elastic-agent` service before stopping endpoint. [#9462](https://github.com/elastic/elastic-agent/pull/9462)

**Fleet Server**

* Fix 503 handling in enrollment. [#5232](https://github.com/elastic/fleet-server/pull/5232) [#5197](https://github.com/elastic/fleet-server/issues/5197)
* Remove extra ES search when preparing agent policy. [#5283](https://github.com/elastic/fleet-server/pull/5283)

## 9.1.2 [fleet-elastic-agent-9.1.2-release-notes]

There are no new features, enhancements, or fixes in this release.

## 9.1.1 [fleet-elastic-agent-9.1.1-release-notes]

### Features and enhancements [fleet-elastic-agent-9.1.1-features-enhancements]

**Elastic Agent**

* Add k8s leader elector OTel extension. [#9065]({{agent-pull}}9065)

### Fixes [fleet-elastic-agent-9.1.1-fixes]

**Elastic Agent**

* Do not overwrite Elasticsearch output headers from enrollment `--headers` flag. [#9199]({{agent-pull}}9199) [#9197]({{agent-issue}}9197)

**Fleet Server**

* Fix upgrade details `download_rate` as string handling. [#5198]({{fleet-server-pull}}5198) [#5214]({{fleet-server-pull}}5214) [#5183]({{fleet-server-pull}}5183) [#5176]({{fleet-server-pull}}5176) [#5164]({{fleet-server-issue}}5164)

## 9.1.0 [fleet-elastic-agent-9.1.0-release-notes]

### Features and enhancements [fleet-elastic-agent-9.1.0-features-enhancements]

**Elastic Agent**

* Adds a new configuration setting, `agent.upgrade.rollback.window` in preparation for enabling upgrade rollbacks in a future release. [#8065]({{agent-pull}}8065) [#6881]({{agent-issue}}6881)

* Removes resource/k8s processor and uses k8sattributes processor for service attributes. [#8599]({{agent-pull}}8599)

  This PR removes the `resource/k8s` processor in honour of the k8sattributes processor that
  provides native support for the service attributes:
  <https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/v0.127.0/processor/k8sattributesprocessor#configuring-recommended-resource-attributes>
  This change is aligned with the respective semantic conventions' guidance:
  <https://opentelemetry.io/docs/specs/semconv/non-normative/k8s-attributes/#service-attributes>
* Adds elastic.agent.fips to local_metadata. [#7112]({{agent-pull}}7112)
* Validates pbkdf2 settings when in FIPS mode. [#7187]({{agent-pull}}7187)
* Adds FIPS-capable agent file vault. [#7360]({{agent-pull}}7360)
* With this change FIPS-capable agents will only be able to upgrade to other FIPS-capable agents. This change also restricts non-FIPS to FIPS upgrades as well. [#7312]({{agent-pull}}7312)
* Updates the error messages returned for FIPS upgrades. [#7453]({{agent-pull}}7453)
* Retries enrollment requests on any error. [#8056]({{agent-pull}}8056)
* Removes deprecated otel Elasticsearch exporter config `*_dynamic_index` from code and samples. [#8592]({{agent-pull}}8592)
* Includes the forwardconnector as an EDOT collector component. [#8753]({{agent-pull}}8753)
* Updates otel components to v0.129.0. [#8819]({{agent-pull}}8819)
* Updates apm config extension to v0.4.0. [#8819]({{agent-pull}}8819)
* Updates elastic trace processor to v0.7.0. [#8819]({{agent-pull}}8819)
* Updates elastic apm connector to v0.4.0. [#8819]({{agent-pull}}8819)
* Updates api key auth extension to v0.2.0. [#8819]({{agent-pull}}8819)
* Updates elastic infra metrics processor to v0.16.0. [#8819]({{agent-pull}}8819)
* Bumps apmconfig extension to v0.3.0. [#8819]({{agent-pull}}8819)

**Fleet Server**

* Adds ability for enrollment to take an agent id. [#4290]({{fleet-server-pull}}4290) [#4226]({{fleet-server-issue}}4226)
* Adds migrate-action. [#4786]({{fleet-server-pull}}4786)

  Added new MIGRATE action type for moving agent to different cluster.
* Clears agent.upgrade_attempts when upgrade is complete. [#4528]({{fleet-server-pull}}4528)
* Makes pbkdf2 settings validation FIPS compliant. [#4542]({{fleet-server-pull}}4542)
* Updates to Go v1.24.0. [#4543]({{fleet-server-pull}}4543)
* Adds version metadata to version command output. [#4820]({{fleet-server-pull}}4820)
* Adds rollback attribute to upgrade actions in preparation for enabling upgrade rollbacks in a future release. [#4838]({{fleet-server-issue}}4838)

### Fixes [fleet-elastic-agent-9.1.0-fixes]

**Elastic Agent**

* Upgrade to Go 1.24.3. [#8109]({{agent-pull}}8109)
* Correctly handle sending signal to child process. [#7738]({{agent-pull}}7738) [#6875]({{agent-issue}}6875)
* Preserve agent run state on deb and rpm upgrades. [#7999]({{agent-pull}}7999)
* Use --header from enrollment when communicating with Fleet Server. [#8071]({{agent-pull}}8071) [#6823]({{agent-issue}}6823)
* Address a race condition that can occur in agent diagnostics if log rotation runs while logs are being zipped.
* Use paths.tempdir for diagnostics actions. [#8472]({{agent-pull}}8472)
* Use debian 11 to build linux/arm to match linux/amd64. Upgrades linux/arm64's statically linked glibc from 2.28 to 2.31. [#8497]({{agent-pull}}8497)
* Relax file ownership check to allow admin re-enrollment on Windows. [#8503]({{agent-pull}}8503) [#7794]({{agent-issue}}7794)
* Remove incorrect logging that unprivileged installations are in beta. [#8715]({{agent-pull}}8715) [#8689]({{agent-issue}}8689)
* Ensure standalone Elastic Agent uses log level from configuration instead of persisted state. [#8784]({{agent-pull}}8784) [#8137]({{agent-issue}}8137)
* Resolve deadlocks in runtime checkin communication. [#8881]({{agent-pull}}8881) [#7944]({{agent-issue}}7944)
* Remove init.d support from rpm packages. [#8896]({{agent-pull}}8896) [#8840]({{agent-issue}}8840)

**Fleet Server**

* Upgrade golang.org/x/net to v0.34.0 and golang.org/x/crypto to v0.32.0. [#4405]({{fleet-server-pull}}4405)
* Update Go to v1.24.3. [#4891]({{fleet-server-pull}}4891)
* Fix host parsing in Elasticsearch output diagnostics. [#4765]({{fleet-server-pull}}4765)
* Redact output in bootstrap config logs. [#4775]({{fleet-server-pull}}4775)
* Mutex protection for remote bulker config. [#4776]({{fleet-server-pull}}4776)
* Enable dead code elimination. [#4784]({{fleet-server-pull}}4784)
* Include the base error for JSON decode error responses. [#5069]({{fleet-server-pull}}5069)

## 9.0.6 [fleet-elastic-agent-9.0.6-release-notes]

### Features and enhancements [fleet-elastic-agent-9.0.6-features-enhancements]

**Elastic Agent**

* Adjust the timeout for Elastic Defend check command. [#9213](https://github.com/elastic/elastic-agent/pull/9213)

### Fixes [fleet-elastic-agent-9.0.6-fixes]

**Elastic Agent**

* Upgrade Go version to 1.24.6. [#9287](https://github.com/elastic/elastic-agent/pull/9287)
* On Windows, retry saving the Agent information file to disk. [#9224](https://github.com/elastic/elastic-agent/pull/9224) [#5862](https://github.com/elastic/elastic-agent/issues/5862)

  Saving the Agent information file involves renaming/moving a file to its final destination. However, on Windows, it is sometimes not possible to rename/move a file to its destination file because the destination file is locked by another process (for example, an antivirus software). In such cases, we now retry the save operation on Windows.

* Correct hints annotations parsing to resolve only `${kubernetes.*}` placeholders instead of resolving all `${...}` patterns. [#9307](https://github.com/elastic/elastic-agent/pull/9307)
* Treat exit code 28 from Endpoint binary as non-fatal. [#9320](https://github.com/elastic/elastic-agent/pull/9320)
* Fixed jitter backoff strategy reset. [#9342](https://github.com/elastic/elastic-agent/pull/9342) [#8864](https://github.com/elastic/elastic-agent/issues/8864)
* Fix Docker container failing to start with `no matching vars: ${env.ELASTICSEARCH_API_KEY:}` and similar errors by restoring support for `:` to set default values. [#9451](https://github.com/elastic/elastic-agent/pull/9451) [#9328](https://github.com/elastic/elastic-agent/issues/9328)
* Fix deb upgrade by stopping `elastic-agent` service before upgrading. [#9462](https://github.com/elastic/elastic-agent/pull/9462)

**Fleet Server**

* Fix 503 handling in enrollment. [#5232](https://github.com/elastic/fleet-server/pull/5232) [#5197](https://github.com/elastic/fleet-server/issues/5197)
* Remove extra ES search when preparing agent policy. [#5283](https://github.com/elastic/fleet-server/pull/5283)

## 9.0.5 [fleet-elastic-agent-9.0.5-release-notes]

### Fixes [fleet-elastic-agent-9.0.5-fixes]

**Fleet Server**

* Fix upgrade details `download_rate` as string handling. [#5217]({{fleet-server-pull}}5217) [#5227]({{fleet-server-pull}}5227) [#5176]({{fleet-server-pull}}5176) [#5164]({{fleet-server-issue}}5164)

## 9.0.4 [fleet-elastic-agent-9.0.4-release-notes]

### Features and enhancements [fleet-elastic-agent-9.0.4-features-enhancements]

**Elastic Agent**

* Add file logs only managed OTLP input kube-stack configuration. [#8785]({{agent-pull}}8785)

### Fixes [fleet-elastic-agent-9.0.4-fixes]

**Elastic Agent**

* Remove incorrect logging that unprivileged installations are in beta. [#8715]({{agent-pull}}8715) [#8689]({{agent-issue}}8689)
* Ensure standalone Elastic Agent uses log level from configuration instead of persisted state. [#8784]({{agent-pull}}8784) [#8137]({{agent-issue}}8137)
* Resolve deadlocks in runtime checkin communication. [#8881]({{agent-pull}}8881) [#7944]({{agent-issue}}7944)
* Remove init.d support from RPM packages. [#8896]({{agent-pull}}8896) [#8840]({{agent-issue}}8840)

**Fleet Server**

* Include the base error for JSON decode error responses. [#5069]({{fleet-server-pull}}5069)

## 9.0.3 [fleet-elastic-agent-9.0.3-release-notes]

### Features and enhancements [fleet-elastic-agent-9.0.3-features-enhancements]

**Elastic Agent**

* Add `Cumulativetodeltaprocessor` To EDOT Collector. [#8372]({{agent-pull}}8372)

**Fleet Server**

* Update Go version to v1.24.4. [#5025]({{fleet-server-pull}}5025)

### Fixes [fleet-elastic-agent-9.0.3-fixes]

**Elastic Agent**

* Address a race condition that can occur in agent diagnostics if log rotation runs while logs are being zipped. [#8215]({{agent-pull}}8215)
* Use `paths.tempdir` for diagnostics actions. [#8472]({{agent-pull}}8472)
* relax file ownership check to allow admin re-enrollment on Windows. [#8503]({{agent-pull}}8503)

## 9.0.2 [fleet-elastic-agent-9.0.2-release-notes]

### Features and enhancements [fleet-elastic-agent-9.0.2-features-enhancements]

* Updates Go version to v1.24.3 in {{fleet}} [#4891]({{fleet-server-pull}}4891)

* Updates Go version to v1.24.3 in {{agent}} [#8109]({{agent-pull}}8109)

### Fixes [fleet-elastic-agent-9.0.2-fixes]

* Improves the upgrade process for {{agent}} installed using DEB or RPM packages by copying the run directory from the previous installation into the new version's folder [#7999]({{agent-pull}}7999) [#3832]({{agent-issue}}3832)

## 9.0.1 [fleet-elastic-agent-9.0.1-release-notes]

### Features and enhancements [fleet-elastic-agent-9.0.1-features-enhancements]

* Reuse shared integration policies when duplicating {{agent}} policies in {{fleet}} [#217872](https://github.com/elastic/kibana/pull/217872)
* Update OTel components to v0.121.0 [#7686]({{agent-pull}}7686)
* Add nopexporter to Elastic Distribution of OTel Collector (EDOT) Collector [#7788]({{agent-pull}}7788)
* In {{agent}}, use `fullnameOverride` to set the fully qualified application names in the EDOT Kube-Stack Helm chart. [#7754]({{agent-pull}}7754) [#7381]({{agent-issue}}7381)

### Fixes [fleet-elastic-agent-9.0.1-fixes]
* In the EDOT Collector, fix Managed OTLP Helm config to use the current image repository [#7882]({{agent-pull}}7882)

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




