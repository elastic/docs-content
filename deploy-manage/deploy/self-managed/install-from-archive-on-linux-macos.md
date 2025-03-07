---
navigation_title: "Install from archive on Linux or macOS"
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/targz.html
---



# Install from archive on Linux or macOS [targz]


Kibana is provided for Linux and Darwin as a `.tar.gz` package. These packages are the easiest formats to use when trying out Kibana.

This package contains both free and subscription features. [Start a 30-day trial](../../license/manage-your-license-in-self-managed-cluster.md) to try out all of the features.

The latest stable version of Kibana can be found on the [Download Kibana](https://elastic.co/downloads/kibana) page. Other versions can be found on the [Past Releases page](https://elastic.co/downloads/past-releases).

::::{note}
macOS is supported for development purposes only and is not covered under the support SLA for [production-supported operating systems](https://www.elastic.co/support/matrix#kibana).

::::


## Download and install the Linux 64-bit package [install-linux64]

Version 9.0.0-beta1 of Kibana has not yet been released.


## Download and install the Darwin package [install-darwin64]

::::{admonition} macOS Gatekeeper warnings
:class: important

Apple’s rollout of stricter notarization requirements affected the notarization of the 9.0.0-beta1 {{kib}} artifacts. If macOS displays a dialog when you first run {{kib}} that interrupts it, you will need to take an action to allow it to run.

To prevent Gatekeeper checks on the {{kib}} files, run the following command on the downloaded `.tar.gz` archive or the directory to which was extracted:

```sh
xattr -d -r com.apple.quarantine <archive-or-directory>
```

Alternatively, you can add a security override if a Gatekeeper popup appears by following the instructions in the *How to open an app that hasn’t been notarized or is from an unidentified developer* section of [Safely open apps on your Mac](https://support.apple.com/en-us/HT202491).

::::


Version 9.0.0-beta1 of Kibana has not yet been released.


## Start {{es}} and generate an enrollment token for {{kib}} [targz-enroll]


When you start {{es}} for the first time, the following security configuration occurs automatically:

* [Certificates and keys](installing-elasticsearch.md#stack-security-certificates) for TLS are generated for the transport and HTTP layers.
* The TLS configuration settings are written to `elasticsearch.yml`.
* A password is generated for the `elastic` user.
* An enrollment token is generated for {{kib}}.

You can then start {{kib}} and enter the enrollment token to securely connect {{kib}} with {{es}}. The enrollment token is valid for 30 minutes.


## Run {{kib}} from the command line [targz-running]

Kibana can be started from the command line as follows:

```sh
./bin/kibana
```

By default, Kibana runs in the foreground, prints its logs to the standard output (`stdout`), and can be stopped by pressing **Ctrl-C**.

If this is the first time you’re starting {{kib}}, this command generates a unique link in your terminal to enroll your {{kib}} instance with {{es}}.

1. In your terminal, click the generated link to open {{kib}} in your browser.
2. In your browser, paste the enrollment token that was generated in the terminal when you started {{es}}, and then click the button to connect your {{kib}} instance with {{es}}.
3. Log in to {{kib}} as the `elastic` user with the password that was generated when you started {{es}}.

::::{note}
If you need to reset the password for the `elastic` user or other built-in users, run the [`elasticsearch-reset-password`](elasticsearch://reference/elasticsearch/command-line-tools/reset-password.md) tool. To generate new enrollment tokens for {{kib}} or {{es}} nodes, run the [`elasticsearch-create-enrollment-token`](elasticsearch://reference/elasticsearch/command-line-tools/create-enrollment-token.md) tool. These tools are available in the {{es}} `bin` directory.

::::



## Configure {{kib}} via the config file [targz-configuring]

Kibana loads its configuration from the `$KIBANA_HOME/config/kibana.yml` file by default.  The format of this config file is explained in [Configuring Kibana](configure.md).


## Directory layout of `.tar.gz` archives [targz-layout]

The `.tar.gz` packages are entirely self-contained. All files and directories are, by default, contained within `$KIBANA_HOME` — the directory created when unpacking the archive.

This is very convenient because you don’t have to create any directories to start using Kibana, and uninstalling Kibana is as easy as removing the `$KIBANA_HOME` directory.  However, it is advisable to change the default locations of the config and data directories so that you do not delete important data later on.

| Type | Description | Default Location | Setting |
| --- | --- | --- | --- |
| home | Kibana home directory or `$KIBANA_HOME` | Directory created by unpacking the archive |  |
| bin | Binary scripts including `kibana` to start the Kibana server    and `kibana-plugin` to install plugins | `$KIBANA_HOME\bin` |  |
| config | Configuration files including `kibana.yml` | `$KIBANA_HOME\config` | `[KBN_PATH_CONF](configure.md)` |
| data | The location of the data files written to disk by Kibana and its plugins | `$KIBANA_HOME\data` |  |
| plugins | Plugin files location. Each plugin will be contained in a subdirectory. | `$KIBANA_HOME\plugins` |  |
