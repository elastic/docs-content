---
navigation_title: "Install on Windows"
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/windows.html
---



# Install on Windows [windows]


Kibana can be installed on Windows using the `.zip` package.

This package contains both free and subscription features. [Start a 30-day trial](../../license/manage-your-license-in-self-managed-cluster.md) to try out all of the features.

The latest stable version of Kibana can be found on the [Download Kibana](https://elastic.co/downloads/kibana) page. Other versions can be found on the [Past Releases page](https://elastic.co/downloads/past-releases).

## Download and install the `.zip` package [install-windows]

Version 9.0.0-beta1 of Kibana has not yet been released.


## Start {{es}} and generate an enrollment token for {{kib}} [windows-enroll]


When you start {{es}} for the first time, the following security configuration occurs automatically:

* [Certificates and keys](installing-elasticsearch.md#stack-security-certificates) for TLS are generated for the transport and HTTP layers.
* The TLS configuration settings are written to `elasticsearch.yml`.
* A password is generated for the `elastic` user.
* An enrollment token is generated for {{kib}}.

You can then start {{kib}} and enter the enrollment token to securely connect {{kib}} with {{es}}. The enrollment token is valid for 30 minutes.


## Run {{kib}} from the command line [windows-running]

Kibana can be started from the command line as follows:

```sh
.\bin\kibana.bat
```

By default, Kibana runs in the foreground, prints its logs to `STDOUT`, and can be stopped by pressing **Ctrl-C**.

If this is the first time you’re starting {{kib}}, this command generates a unique link in your terminal to enroll your {{kib}} instance with {{es}}.

1. In your terminal, click the generated link to open {{kib}} in your browser.
2. In your browser, paste the enrollment token that was generated in the terminal when you started {{es}}, and then click the button to connect your {{kib}} instance with {{es}}.
3. Log in to {{kib}} as the `elastic` user with the password that was generated when you started {{es}}.

::::{note}
If you need to reset the password for the `elastic` user or other built-in users, run the [`elasticsearch-reset-password`](https://www.elastic.co/guide/en/elasticsearch/reference/current/reset-password.html) tool. To generate new enrollment tokens for {{kib}} or {{es}} nodes, run the [`elasticsearch-create-enrollment-token`](https://www.elastic.co/guide/en/elasticsearch/reference/current/create-enrollment-token.html) tool. These tools are available in the {{es}} `bin` directory.

::::



## Configure {{kib}} via the config file [windows-configuring]

Kibana loads its configuration from the `$KIBANA_HOME/config/kibana.yml` file by default.  The format of this config file is explained in [Configuring Kibana](configure.md).


## Directory layout of `.zip` archive [windows-layout]

The `.zip` package is entirely self-contained. All files and directories are, by default, contained within `$KIBANA_HOME` — the directory created when unpacking the archive.

This is very convenient because you don’t have to create any directories to start using Kibana, and uninstalling Kibana is as easy as removing the `$KIBANA_HOME` directory.  However, it is advisable to change the default locations of the config and data directories so that you do not delete important data later on.

| Type | Description | Default Location | Setting |
| --- | --- | --- | --- |
| home | Kibana home directory or `$KIBANA_HOME` | Directory created by unpacking the archive |  |
| bin | Binary scripts including `kibana` to start the Kibana server    and `kibana-plugin` to install plugins | `$KIBANA_HOME\bin` |  |
| config | Configuration files including `kibana.yml` | `$KIBANA_HOME\config` | `[KBN_PATH_CONF](configure.md)` |
|  | data | `The location of the data files written to disk by Kibana and its plugins` | `$KIBANA_HOME\data` |
|  | plugins | `Plugin files location. Each plugin will be contained in a subdirectory.` | `$KIBANA_HOME\plugins` |
