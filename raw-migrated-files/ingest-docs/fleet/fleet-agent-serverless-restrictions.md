---
navigation_title: "Restrictions for {{serverless-full}}"
---

# {{fleet}} and {{agent}} restrictions for {{serverless-full}} [fleet-agent-serverless-restrictions]



## {{agent}} [elastic-agent-serverless-restrictions]

If you are using {{agent}} with [{{serverless-full}}](https://docs.elastic.co/serverless), note these differences from use with {{ech}} and self-managed {{es}}:

* The number of {{agents}} that may be connected to an {{serverless-full}} project is limited to 10 thousand.
* The minimum supported version of {{agent}} supported for use with {{serverless-full}} is 8.11.0.

$$$outputs-serverless-restrictions$$$
**Outputs**

* On {{serverless-short}}, you can configure new {{es}} outputs to use a proxy, with the restriction that the output URL is fixed. Any new {{es}} outputs must use the default {{es}} host URL.


## {{fleet}} [fleet-serverless-restrictions]

The path to get to the {{fleet}} application in {{kib}} differs across projects:

* In {{ech}} deployments, navigate to **Management > Fleet**.
* In {{serverless-short}} {{observability}} projects, navigate to **Project settings > Fleet**.
* In {{serverless-short}} Security projects, navigate to **Assets > Fleet**.


## {{fleet-server}} [fleet-server-serverless-restrictions]

Note the following restrictions with using {{fleet-server}} on {{serverless-short}}:

* On-premises {{fleet-server}} is not currently available for use in a {{serverless-short}} environment. We recommend using the hosted {{fleet-server}} that is included and configured automatically in {{serverless-short}} {{observability}} and Security projects.
* On {{serverless-short}}, you can configure {{fleet-server}} to use a proxy, with the restriction that the {{fleet-server}} host URL is fixed. Any new {{fleet-server}} hosts must use the default {{fleet-server}} host URL.
