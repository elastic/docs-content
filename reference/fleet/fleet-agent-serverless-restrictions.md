---
navigation_title: Restrictions for {{serverless-full}}
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-agent-serverless-restrictions.html
applies_to:
  serverless: all
products:
  - id: fleet
  - id: elastic-agent
---

# {{fleet}} and {{agent}} restrictions for {{serverless-full}} [fleet-agent-serverless-restrictions]

## {{agent}} [elastic-agent-serverless-restrictions]

If you are using {{agent}} with [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md), note these differences from use with {{ech}} and self-managed {{es}}:

* A maximum of 10,000 {{fleet}}-managed {{agents}} can be connected to an {{serverless-full}} project. This limit does not apply to standalone agents.
* The maximum supported number of {{agent}} policies is 500.
* The minimum supported version of {{agent}} supported for use with {{serverless-full}} is 8.11.0.

### Outputs

On {{serverless-short}}, you can configure new {{es}} outputs to use a proxy, with the restriction that the output URL is fixed. Any new {{es}} outputs must use the default {{es}} host URL.

### Upgrade

{{agents}} are not automatically upgraded with the upgrade of the {{serverless-short}} project. You can upgrade standalone or {{fleet}}-managed {{agent}}s at your convenience.

For more information, see [](upgrade-elastic-agent.md) and [](upgrade-standalone.md).


## {{fleet}} [fleet-serverless-restrictions]

The path to get to the {{fleet}} application in {{kib}} differs across projects:

* In {{ech}} deployments, navigate to **Management** → **Fleet**.
* In {{serverless-short}} {{observability}} projects, navigate to **Project settings** → **Fleet**.
* In {{serverless-short}} Security projects, navigate to **Assets** → **Fleet**.


## {{fleet-server}} [fleet-server-serverless-restrictions]

Note the following restrictions with using {{fleet-server}} on {{serverless-short}}:

* On-premises {{fleet-server}} is not currently available for use in a {{serverless-short}} environment. We recommend using the hosted {{fleet-server}} that is included and configured automatically in {{serverless-short}} {{observability}} and Security projects.
* On {{serverless-short}}, you can configure {{fleet-server}} to use a proxy, with the restriction that the {{fleet-server}} host URL is fixed. Any new {{fleet-server}} hosts must use the default {{fleet-server}} host URL.
