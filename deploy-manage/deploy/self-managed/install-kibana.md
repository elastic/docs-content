---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/setup.html
  - https://www.elastic.co/guide/en/kibana/current/install.html
applies_to:
  deployment:
    self:
products:
  - id: kibana
---

# Install {{kib}}

{{kib}} provides the user interface for all Elastic solutions. It’s a powerful tool for visualizing and analyzing your data, and for managing and monitoring the {{stack}}. Although {{kib}} is not required to use {{es}}, it's required for most use cases.

This section includes information on how to set up {{kib}} and get it running, including:

* Downloading and installing {{kib}}
* Enrolling {{kib}} with an {{es}} cluster
* Configuring {{kib}}

To quickly set up {{es}} and {{kib}} in Docker for local development or testing, jump to [](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md).

## Supported platforms [supported-platforms]

Packages of {{kib}} are provided for and tested against Linux, Darwin, and Windows. Because {{kib}} runs on Node.js, we include the necessary Node.js binaries for these platforms. Running {{kib}} against a separately maintained version of Node.js is not supported.

To support certain older Linux platforms (most notably CentOS7/RHEL7), {{kib}} for Linux ships with a custom build of Node.js with glibc 2.17 support. For details, see [Custom builds of Node.js](kibana://extend/upgrading-nodejs.md#custom-nodejs-builds).

## {{kib}} install packages [install]

{{kib}} is provided in the following package formats:

| Format | Description | Instructions |
| --- | --- | --- |
| `tar.gz` | The `tar.gz` packages are provided for installation on Linux and Darwin and are the easiest choice for getting started with {{kib}}. | [Install from archive on Linux or macOS](/deploy-manage/deploy/self-managed/install-kibana-from-archive-on-linux-macos.md)|
| `zip` | The `zip` package is the only supported package for Windows.| [Install on Windows](/deploy-manage/deploy/self-managed/install-kibana-on-windows.md)|
| `deb` | The `deb` package is suitable for Debian, Ubuntu, and other Debian-based systems.  Debian packages may be downloaded from the Elastic website or from our Debian repository. | [Install with Debian package](/deploy-manage/deploy/self-managed/install-kibana-with-debian-package.md) |
| `rpm` | The `rpm` package is suitable for installation on Red Hat, SLES, OpenSuSE and other RPM-based systems.  RPMs may be downloaded from the Elastic website or from our RPM repository. | [Install with RPM](/deploy-manage/deploy/self-managed/install-kibana-with-rpm.md) |
| `docker` | Images are available for running {{kib}} as a Docker container. They may be downloaded from the Elastic Docker Registry. | [Running {{kib}} on Docker](/deploy-manage/deploy/self-managed/install-kibana-with-docker.md) |

## {{es}} version [elasticsearch-version]

:::{include} /deploy-manage/deploy/_snippets/stack-version-compatibility.md
:::

Running different major version releases of {{kib}} and {{es}} (e.g. {{kib}} 9.x and {{es}} 8.x) is not supported, nor is running a minor version of {{kib}} that is newer than the version of {{es}} (e.g. {{kib}} 8.14 and {{es}} 8.13).

Running a minor version of {{es}} that is higher than {{kib}} will generally work in order to facilitate an upgrade process where {{es}} is upgraded first (e.g. {{kib}} 8.14 and {{es}} 8.15). In this configuration, a warning will be logged on {{kib}} server startup, so it’s only meant to be temporary until {{kib}} is upgraded to the same version as {{es}}.

Running different patch version releases of {{kib}} and {{es}} (e.g. {{kib}} 9.0.0 and {{es}} 9.0.1) is generally supported, though we encourage users to run the same versions of {{kib}} and {{es}} down to the patch version.


## Installation order

:::{include} /deploy-manage/deploy/_snippets/installation-order.md
:::

## Default ports

:::{include} _snippets/ports.md
:::

## Third-party dependencies

:::{include} /deploy-manage/deploy/self-managed/_snippets/third-party-dependencies.md
:::
