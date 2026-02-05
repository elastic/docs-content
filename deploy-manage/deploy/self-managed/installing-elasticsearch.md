---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/setup.html
  - https://www.elastic.co/guide/en/elastic-stack/current/installing-elastic-stack.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/configuring-stack-security.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
---

# Deploy an {{es}} cluster

% will be fixed

$$$stack-security-certificates$$$

This section includes information on how to set up {{es}} and get it running, including:

* [Configuring your system to support {{es}}](/deploy-manage/deploy/self-managed/important-system-configuration.md), and the [bootstrap checks](/deploy-manage/deploy/self-managed/bootstrap-checks.md) that are run at startup to verify these configurations
* Downloading, installing, and starting {{es}} using each [supported installation method](#installation-methods)

To quickly set up {{es}} and {{kib}} in Docker for local development or testing, jump to [](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md).

## Installation methods

If you want to install and manage {{es}} yourself, you can:

* Run {{es}} using a [Linux, MacOS, or Windows install package](#elasticsearch-install-packages).
* Run {{es}} in a [Docker container](#elasticsearch-docker-images).

::::{tip}
To try out {{stack}} on your own machine, we recommend using Docker and running both {{es}} and {{kib}}. For more information, see [](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md). This setup is not suitable for production use.
::::

::::{admonition} Use dedicated hosts
$$$dedicated-host$$$
:::{include} _snippets/dedicated-hosts.md
:::
::::

### {{es}} install packages [elasticsearch-install-packages]

{{es}} is provided in the following package formats.

Each linked guide provides the following details:

* Download and installation instructions
* Information on enrolling a newly installed node in an existing cluster
* Instructions on starting {{es}} manually and, if applicable, as a service or daemon
* Instructions on connecting clients to your new cluster
* Archive or package contents information
* Security certificate and key information

Special considerations such as firewalls and proxy servers are not covered.

Before you start, make sure that you [configure your system](/deploy-manage/deploy/self-managed/important-system-configuration.md).

| Format | Description | Instructions |
| --- | --- | --- |
| Linux and MacOS `tar.gz` archives | The `tar.gz` archives are available for installation on any Linux distribution and MacOS. | [Install {{es}} from archive on Linux or MacOS](/deploy-manage/deploy/self-managed/install-elasticsearch-from-archive-on-linux-macos.md) |
| Windows `.zip` archive | The `zip` archive is suitable for installation on Windows. | [Install {{es}} with `.zip` on Windows](/deploy-manage/deploy/self-managed/install-elasticsearch-with-zip-on-windows.md) |
| `deb` | The `deb` package is suitable for Debian, Ubuntu, and other Debian-based systems. Debian packages can be downloaded from the {{es}} website or from our Debian repository. | [Install {{es}} with Debian Package](/deploy-manage/deploy/self-managed/install-elasticsearch-with-debian-package.md) |
| `rpm` | The `rpm` package is suitable for installation on Red Hat, Centos, SLES, OpenSuSE and other RPM-based systems. RPM packages can be downloaded from the {{es}} website or from our RPM repository. | [Install {{es}} with RPM](/deploy-manage/deploy/self-managed/install-elasticsearch-with-rpm.md) |

### {{es}} container images [elasticsearch-docker-images]

You can also run {{es}} inside a docker container image. Docker container images may be downloaded from the Elastic Docker Registry.

You can [use Docker Compose](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-compose.md) to deploy multiple nodes at once.

[Install {{es}} with Docker](/deploy-manage/deploy/self-managed/install-elasticsearch-with-docker.md)

## Version compatibility

:::{include} /deploy-manage/deploy/_snippets/stack-version-compatibility.md
:::

## Installation order

:::{include} /deploy-manage/deploy/_snippets/installation-order.md
:::

## Required ports

:::{include} _snippets/ports.md
:::

## Supported operating systems and JVMs [supported-platforms]

The matrix of officially supported operating systems and JVMs is available in the [Elastic Support Matrix](https://elastic.co/support/matrix). {{es}} is tested on the listed platforms, but it is possible that it will work on other platforms too.

### Java (JVM) Version [jvm-version]

{{es}} is built using Java, and includes a bundled version of [OpenJDK](https://openjdk.java.net) within each distribution. We strongly recommend using the bundled JVM in all installations of {{es}}.

The bundled JVM is treated the same as any other dependency of {{es}} in terms of support and maintenance. This means that Elastic takes responsibility for keeping it up to date, and reacts to security issues and bug reports as needed to address vulnerabilities and other bugs in {{es}}. Elastic’s support of the bundled JVM is subject to Elastic’s [support policy](https://www.elastic.co/support_policy) and [end-of-life schedule](https://www.elastic.co/support/eol) and is independent of the support policy and end-of-life schedule offered by the original supplier of the JVM. Elastic does not support using the bundled JVM for purposes other than running {{es}}.

::::{tip}
{{es}} uses only a subset of the features offered by the JVM. Bugs and security issues in the bundled JVM often relate to features that {{es}} does not use. Such issues do not apply to {{es}}. Elastic analyzes reports of security vulnerabilities in all its dependencies, including in the bundled JVM, and will issue an [Elastic Security Advisory](https://github.com/elastic/.github/blob/main/SECURITY.md) if such an advisory is needed.
::::


If you decide to run {{es}} using a version of Java that is different from the bundled one, prefer to use the latest release of a [LTS version of Java](https://www.oracle.com/technetwork/java/eol-135779.html) which is [listed in the support matrix](https://elastic.co/support/matrix). Although such a configuration is supported, if you encounter a security issue or other bug in your chosen JVM then Elastic may not be able to help unless the issue is also present in the bundled JVM. Instead, you must seek assistance directly from the supplier of your chosen JVM. You must also take responsibility for reacting to security and bug announcements from the supplier of your chosen JVM. {{es}} may not perform optimally if using a JVM other than the bundled one. {{es}} is closely coupled to certain OpenJDK-specific features, so it may not work correctly with JVMs that are not OpenJDK. {{es}} will refuse to start if you attempt to use a known-bad JVM version.

To use your own version of Java, set the `ES_JAVA_HOME` environment variable to the path to your own JVM installation. The bundled JVM is located within the `jdk` subdirectory of the {{es}} home directory. You may remove this directory if using your own JVM.

:::{warning}
Don’t use third-party Java agents that attach to the JVM. Such agents can be harmful to {{es}} stability and performance. In some cases they may cause nodes to freeze, crash, or fail to start up, or to lose or corrupt your data.
:::

## Third-party dependencies [dependencies-versions]

:::{include} /deploy-manage/deploy/self-managed/_snippets/third-party-dependencies.md
:::
