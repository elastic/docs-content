---
navigation_title: Get started
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/profiling-get-started.html
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: observability
---



# Get started with Universal Profiling [profiling-get-started]


This page shows you how to configure and use Universal Profiling on an {{ecloud}} deployment. To set up a self-hosted deployment of {{stack}}, refer to [Run Universal Profiling on self-hosted Elastic stack ](./run-universal-profiling-on-self-hosted-elastic-stack.md).

This page covers:

* Prerequisites to setting up Universal Profiling on {{ecloud}}
* Setting up Universal Profiling in your {{ecloud}} deployment
* Installing the Universal Profiling Agent
* Installing the Universal Profiling Agent integration

We would appreciate feedback on your experience with this product and any other profiling pain points you may have. See the [send feedback](/troubleshoot/observability/troubleshoot-your-universal-profiling-agent-deployment.md#profiling-send-feedback) section of the troubleshooting documentation for more information.


## Prerequisites [profiling-prereqs]

Before setting up Universal Profiling, make sure you meet the following requirements:

* An {{stack}} deployment on [{{ecloud}}](http://cloud.elastic.co). To set up a self-hosted deployment of {{stack}}, refer to [Run Universal Profiling on self-hosted Elastic stack ](./run-universal-profiling-on-self-hosted-elastic-stack.md).
* The workloads you’re profiling must be running on Linux machines with x86_64 or ARM64 CPUs.
* The minimum supported kernel version is either 4.19 for x86_64 or 5.5 for ARM64 machines.
* The Integrations Server must be enabled on your {{ecloud}} deployment.
* Credentials (username and password) for the `superuser` Elasticsearch role (typically, the `elastic` user).


### Interpreters [profiling-prereqs-interpreters]

Universal Profiling is a system-wide profiling solution with additional support for PHP, Python, Java (or any JVM language), Go, Rust, C/C++, Node.js/V8, Ruby, .Net, and Perl.

The minimum supported versions of each interpreter are:

* JVM/JDK: 7
* Python: 3.6
* V8: 8.1.0
* Perl: 5.28
* PHP: 7.3
* Ruby: 2.5
* .Net: 6


### Deployment configuration example [profiling-prereqs-config-example]

The following deployment configuration example was tested to support profiling data from a fleet of up to 500 hosts, each with 8 or 16 CPU cores, for a total of roughly 6000 cores:

| Component | Size per zone (memory) | Zones |
| --- | --- | --- |
| {{es}} | 64 GB | 2 |
| Kibana | 8 GB | 1 |
| Integrations Server | 8 GB | 1 |

Even if you’re profiling a smaller fleet, we recommend configuring at least two zones for Elasticsearch and 4 GB of memory each for the Integrations Server and Kibana.


## Set up Universal Profiling on an {{ecloud}} deployment [profiling-set-up-on-cloud]

To set up Universal Profiling on your {{ecloud}} deployment, you need to [configure data ingestion](#profiling-configure-data-ingestion) first.


### Configure data ingestion [profiling-configure-data-ingestion]

After enabling Universal Profiling on your deployment for the first time, select any subheading under **Universal Profiling** in the navigation menu to open the following page:

:::{image} /solutions/images/observability-profiling-setup-popup.png
:alt: profiling setup popup
:screenshot:
:::

Click **Set up Universal Profiling** to configure data ingestion.

::::{note}
To configure data ingestion, you need elevated privileges, typically the `elastic` user.
::::


If you’re upgrading from a previous version with Universal Profiling enabled, see the [upgrade guide](upgrade-universal-profiling.md).


### Programmatic configuration [profiling-configure-data-ingestion-programmatic]
```{applies_to}
stack: ga 9.2
```

If you prefer to configure data ingestion programmatically, you can use a Kibana API call. This call can be made either through the "Dev Tools" console in Kibana or with any standalone HTTP client (such as `curl` or `wget`). In both cases, the API call must be executed using the `elastic` user credentials to ensure the necessary permissions.

A successful API call will return a `202 Accepted` response with an empty body.

To configure data ingestion from the console, go to **Dev Tools** in the navigation menu and run the following command:

```console
POST kbn:/api/profiling/setup/es_resources
{}
```

To configure data ingestion programmatically using a standalone HTTP client (e.g., `curl`), run the following command:

```console
curl -u elastic:<PASSWORD> -H "kbn-xsrf: true" -H "Content-Type: application/json" \
    --data "{}" "https://<kibana-host>:<kibana-port>/api/profiling/setup/es_resources"
```


## Install the Universal Profiling Agent [profiling-install-profiling-agent]

You have the following options when installing the Universal Profiling Agent:

1. [Install the Universal Profiling Agent using the {{agent}}](#profiling-install-agent-elastic-agent)
2. [Install the Universal Profiling Agent in standalone mode](#profiling-install-agent-standalone)


### Install the Universal Profiling Agent using the {{agent}} [profiling-install-agent-elastic-agent]

To install the Universal Profiling Agent using the {{agent}} and the Universal Profiling Agent integration, complete the following steps:

1. Copy the `secret token` and `Universal Profiling Collector url` from the Elastic Agent Integration

    :::{image} /solutions/images/observability-profiling-elastic-agent.png
    :alt: profiling elastic agent
    :screenshot:
    :::

2. Click `Manage Universal Profiling Agent in Fleet` to complete the integration.
3. On the Integrations page, click **Add Universal Profiling Agent**.
4. In **Universal Profiling Agent → Settings**, add the information you copied from the **Add profiling data** page:

    1. Add the Universal Profiling collector URL to the **Universal Profiling collector endpoint** field.
    2. Add the secret token to the **Authorization** field.

        :::{image} /solutions/images/observability-profililing-elastic-agent-creds.png
        :alt: profililing elastic agent creds
        :screenshot:
        :::

5. Click **Save and continue**.

#### Deploy {{agent}} using `Kubernetes` with the Universal Profiling Agent integration

To deploy {{agent}} with the Universal Profiling Agent integration using Kubernetes,
make sure that the following options are set in the manifest.

```console
hostPID: true
securityContext:
  readOnlyRootFilesystem: true
  privileged: true
  runAsUser: 0
  runAsGroup: 0
  capabilities:
    add:
      - SYS_ADMIN
```

## Install the Universal Profiling Agent in standalone mode [profiling-install-agent-standalone]

The Universal Profiling Agent profiles your fleet. You need to install and configure it on every machine that you want to profile. The Universal Profiling Agent needs  `root` / `CAP_SYS_ADMIN` privileges to run.

After clicking **Set up Universal Profiling** in the previous step, you’ll see the instructions for installing the Universal Profiling Agent. You can also find these instructions by clicking the **Add data** button in the top-right corner of the page.

The following is an example of the provided instructions for {{k8s}}:

:::{image} /solutions/images/observability-profiling-k8s-hostagent.png
:alt: profiling k8s hostagent
:screenshot:
:::


### Universal Profiling Agent configuration notes [profiling-agent-config-notes]

Consider the following when configuring your Universal Profiling Agent:

* The instructions in Kibana work well for testing environments. For production environments, we recommend setting an immutable version.
* Before {{stack}} version 8.9 the Universal Profiling Agent versioning scheme was **not aligned with the {{stack}} version scheme**.
* You can find a list of container image versions in the [Elastic container library repository](https://container-library.elastic.co/r/observability/profiling-agent).
* For {{k8s}} deployments, the Helm chart version is already used to configure the same container image, unless overwritten with the `version` parameter in the Helm values file.
* For {{stack}} version 8.8, use `v3` host agents. For version 8.7, use `v2`. `v3` host agents are incompatible with 8.7 {{stack}} versions.
