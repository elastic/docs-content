# Upgrade

⚠️ **This page is a work in progress.** ⚠️

Upgrading to the latest version provides you access to Elastic latest features, enhancements, performance improvements, and bug fixes, many of which enable you to save your organization money, respond faster to potential threats, and improve the tools you use to investigate and analyze your data. As new versions are released, older versions reach their end of life at a regular cadence, so it’s important to ensure that your deployment is fully maintained and supported. For more information, refer to Elastic’s [Product End of Life Dates](https://www.elastic.co/support/eol).

:::{note}
Upgrading from a release candidate build, such as 9.0.0-rc1 or 9.0.0-rc2, is not supported. Pre-releases should only be used for testing in a temporary environment.
:::

## Plan your upgrade [plan-upgrade]

There are a number of things you need to plan for before performing the actual upgrade, so create a test plan. Consider the following recommendations: 

* Plan for an appropriate amount of time to complete the upgrade. Depending on your configuration and the size of your cluster, the process can take up to a few weeks or more to complete.
* Consider opening a [support case](https://support.elastic.co/) with Elastic to alert our Elastic Support team of your system change. If you need additional assistance, [Elastic Consulting Services](https://www.elastic.co/consulting) provides the technical expertise and step-by-step approach for upgrading your Elastic deployment.
* Schedule a system maintenance window within your organization.

**Check system requirements** 

Ensure the version you’re upgrading to for {{es}}, {{kib}}, and any ingest components supports your current operating system. Refer to the [Product and Operating System support matrix](https://www.elastic.co/support/matrix#matrix_os). 

**OpenJDK compatibility and FIPS compliance**

By default, {{es}} is built using Java and includes a bundled version of [OpenJDK](https://openjdk.java.net/) within each distribution. While we strongly recommend using the bundled Java Virtual Machine (JVM) in all installations of {{es}}, if you choose to use your own JVM, ensure it’s compatible by reviewing the [Product and JVM support matrix](https://www.elastic.co/support/matrix#matrix_jvm). {{es}} 9.0 requires Java 21 and supports Java 24. 

If you’re running {{es}} in FIPS 140-2 mode, {{es}} 9.0 has been tested with [Bouncy Castle's](https://www.bouncycastle.org/java.html) FIPS implementation and is the recommended Java security provider when running {{es}}. 

**Conduct a component inventory**

It is very important to map all the components that are being used on the {{stack}}. When you upgrade your deployment, you also may need to upgrade all the other components. You should record if each component is used, and if it is, also record the current version. While not comprehensive, here’s a list of components you should check: 

* {{es}}
* {{es}} Hadoop
* {{es}} plugins
* {{es}} clients
* {{kib}}
* {{ls}}
* {{ls}} plugins
* {{beats}}
* {{beats}} modules
* {{apm-agent}}
* APM server
* {{agent}}
* {{fleet}}
* Security
* Browsers
* External services (Kafka, etc.)

:::{tip}
When you do your inventory, you can [enable audit logging](/deploy-manage/security/logging-configuration/enabling-audit-logs.md) to evaluate resources accessing your deployment.
:::

**Test your development environment**

We highly recommend testing and upgrading in your development environment before your production environment. Therefore, it is crucial to ensure that both your development and production environments have the same settings. Consider checking the following components beforehand:

* Enrichment information
* Plugins
* Mapping
* Index lifecycle management (ILM)
* Snapshot lifecycle management (SLM)
* Index templates
* {{ml-cap}} jobs
* Inbound sample data
* Live data
* Performance
* Outbound integrations
* Dashboards
* Alerts
* Authentication

## Choose your upgrade path [choose-upgrade-path]

The procedures you follow to upgrade depend on your infrastructure and deployment method. You’ve installed Elastic components using either Elastic-managed infrastructure or self-managed infrastructure. 

### Elastic-managed infrastructure 

Elastic-managed infrastructure includes {{ecloud}} – the umbrella term for {{ech}} (ECH) and {{serverless-full}}. {{serverless-full}} (“Serverless”) is a fully managed cloud offering with three products: {{es-serverless}}, {{obs-serverless}}, and {{sec-serverless}}. All serverless products are built on top of the Search AI Lake. Customers on serverless receive the latest features automatically when updates are published and do not need to choose an upgrade path.  

{{ech}} is Elastic’s cloud offering for managing {{stack}} deployments, built on top of {{es}}. A single click in the {{ecloud}} console can upgrade a deployment to a newer version.

### Self-managed infrastructure

Self-managed infrastructure – either on-prem or on public cloud, includes: 
* {{stack}} 
* {{ece}} (ECE)
* {{eck}} (ECK)

For ECE and ECK, you must ensure the operator is running a compatible version with the {{stack}} version you’re upgrading to. If not, you need to upgrade that before you can upgrade your cluster. 

If you’re running the {{stack}} on your own self-managed infrastructure, you must upgrade each component individually. 

% Refer to the diagram below for a visualization of the different deployment methods. 


