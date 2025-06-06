---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-version-policy.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-version-policy.html
applies_to:
  deployment:
    ess: ga
products:
  - id: cloud-hosted
---

# Available stack versions [ec-version-policy]

This section describes our version policy for {{ech}}, including:

* [What {{stack}} versions are available](#ec-version-policy-available)
* [When we make new {{stack}} versions available](#ec-version-policy-new)
* [When we might force an upgrade or restart to keep your cluster safe](#ec-version-policy-critical)
* [What release candidates and cutting edge builds we make available](#ec-release-builds)
* [What happens when a version reaches its end-of-life (EOL)](#ec-version-policy-eol)


## Available {{stack}} versions [ec-version-policy-available]

{{stack}} uses a versions code that is constructed of three numbers separated by dots: the leftmost number is the number of the major release, the middle number is the number of the minor release and the rightmost number is the number of the maintenance release (e.g., 8.3.2 means major release 8, minor release 3 and maintenance release 2).

You might sometimes notice additional versions listed in the user interface beyond the versions we currently support and maintain, such as [release candidate builds](#ec-release-builds) and older versions. If a version is listed in the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), it can be deployed.


## New {{stack}} versions [ec-version-policy-new]

Whenever a new {{stack}} version is released, we do our best to provide the new version on our hosted service at the same time. We send you an email and add a notice to the console, recommending an upgrade. You’ll need to decide whether to upgrade to the new version with new features and bug fixes or to stay with a version you know works for you a while longer.

There can be [breaking changes](elasticsearch://release-notes/breaking-changes.md) in some new versions of {{es}} that break what used to work in older versions. Before upgrading, you’ll want to check if the new version introduces any changes that might affect your applications. A breaking change might be a function that was previously deprecated and that has been removed in the latest version, for example. If you have an application that depends on the removed function, the application will need to be updated to continue working with the new version of {{es}}.

To learn more about upgrading to newer versions of the {{stack}} on our hosted service, check [Upgrade Versions](../../upgrade/deployment-or-cluster.md).


## Upgrades or restart for critical issues [ec-version-policy-critical]

We reserve the right to force upgrade or restart a cluster immediately and without notice in advance if there is a critical security or stability issue. Such upgrades happen only within minor versions.

A forced upgrade or restart might become necessary in a situation that:

* Bypasses Shield, where knowing only the cluster endpoint is sufficient to gain access to data.
* Disrupts our ability to effectively manage a cluster in disaster scenarios
* Impairs stability to the point where we cannot guarantee cluster node or data integrity
* Impairs or risks impairing our infrastructure


## Release candidates and cutting-edge releases [ec-release-builds]

Interested in kicking the tires of {{es}} releases at the cutting edge? We sometimes make release candidate builds and other cutting-edge releases available in {{ecloud}} for you to try out.

::::{warning}
Remember that cutting-edge releases are used to test new function fully. These releases might still have issues and might be less stable than the GA version. There’s also no guaranteed upgrade path to the GA version when it becomes available.
::::


If you’re interested in trying out one of these cutting-edge releases, we don’t recommended upgrading an existing deployment directly. Instead, use a copy of your existing data with a test deployment, first.

Cutting-edge releases do not remain available forever. Once the GA version of {{es}} is released, your deployment needs to be removed after a grace period. We cannot guarantee that you will be able to upgrade to the GA version when it becomes available.


## Version Policy and Product End of Life [ec-version-policy-eol]

For {{ecloud}}, we follow the [Elastic Version Maintenance and Support Policy](https://www.elastic.co/support/eol), which defines the support and maintenance policy of the {{stack}}.
