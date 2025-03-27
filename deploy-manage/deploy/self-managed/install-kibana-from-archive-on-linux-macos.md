---
navigation_title: "Install from archive on Linux or macOS"
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/targz.html
navigation_title: "Linux and MacOS"
applies_to:
  deployment:
    self:
---

# Install {{kib}} from archive on Linux or macOS [targz]


{{kib}} is provided for Linux and Darwin as a `.tar.gz` package. These packages are the easiest formats to use when trying out Kibana.

:::{include} _snippets/trial.md
:::

:::{include} _snippets/kib-releases.md
:::

::::{note}
macOS is supported for development purposes only and is not covered under the support SLA for [production-supported operating systems](https://www.elastic.co/support/matrix#kibana).
::::

## Step 1: Download and install the archive

### Linux [install-linux64]

The Linux archive for {{kib}} {{stack-version}} can be downloaded and installed as follows:

```sh subs=true
curl -O https://artifacts.elastic.co/downloads/kibana/kibana-{{stack-version}}-linux-x86_64.tar.gz
curl https://artifacts.elastic.co/downloads/kibana/kibana-{{stack-version}}-linux-x86_64.tar.gz.sha512 | shasum -a 512 -c - <1>
tar -xzf kibana-{{stack-version}}-linux-x86_64.tar.gz
cd kibana-{{stack-version}}/ <2>
```

1. Compares the SHA of the downloaded `.tar.gz` archive and the published checksum, which should output `kibana-<version>-linux-x86_64.tar.gz: OK`.
2. This directory is known as `$KIBANA_HOME`.

## MacOS [install-darwin64]

The Darwin archive for {{kib}} {{stack-version}} can be downloaded and installed as follows:

```sh subs=true
curl -O https://artifacts.elastic.co/downloads/kibana/kibana-{{stack-version}}-darwin-x86_64.tar.gz
curl https://artifacts.elastic.co/downloads/kibana/kibana-{{stack-version}}-darwin-x86_64.tar.gz.sha512 | shasum -a 512 -c - <1>
tar -xzf kibana-{{stack-version}}-darwin-x86_64.tar.gz
cd kibana-{{stack-version}}/ <2>
```

1. Compares the SHA of the downloaded `.tar.gz` archive and the published checksum, which should output `kibana-<version>-darwin-x86_64.tar.gz: OK`.
2. This directory is known as `$KIBANA_HOME`.


::::{admonition} macOS Gatekeeper warnings
:class: important

Apple’s rollout of stricter notarization requirements affected the notarization of the {{stack-version}} {{kib}} artifacts. If macOS displays a dialog when you first run {{kib}} that interrupts it, you will need to take an action to allow it to run.

To prevent Gatekeeper checks on the {{kib}} files, run the following command on the downloaded `.tar.gz` archive or the directory to which was extracted:

```sh subs=true
xattr -d -r com.apple.quarantine <archive-or-directory>
```

Alternatively, you can add a security override if a Gatekeeper popup appears by following the instructions in the *How to open an app that hasn’t been notarized or is from an unidentified developer* section of [Safely open apps on your Mac](https://support.apple.com/en-us/HT202491).

::::

## Step 2: Start {{es}} and generate an enrollment token for {{kib}} [targz-enroll]

[Start {{es}}](/deploy-manage/maintenance/start-stop-services/start-stop-elasticsearch.md).

:::{include} _snippets/auto-security-config.md
:::

:::{include} _snippets/new-enrollment-token.md
:::

## Step 3: Run {{kib}} from the command line [targz-running]

{{kib}} can be started from the command line as follows:

```sh
./bin/kibana
```
By default, {{kib}} runs in the foreground, prints its logs to the standard output (`stdout`), and can be stopped by pressing `Ctrl`+`C`.

:::{include} _snippets/enroll-steps.md
:::

## Step 4: Configure {{kib}} using the config file [targz-configuring]

{{kib}} loads its configuration from the `$KIBANA_HOME/config/kibana.yml` file by default. The format of this config file is explained in [](configure-kibana.md).


## Directory layout of `.tar.gz` archives [targz-layout]

The `.tar.gz` packages are entirely self-contained. All files and directories are, by default, contained within `$KIBANA_HOME` — the directory created when unpacking the archive.

This is very convenient because you don’t have to create any directories to start using Kibana, and uninstalling {{kib}} is as easy as removing the `$KIBANA_HOME` directory.  However, it is advisable to change the default locations of the config and data directories so that you do not delete important data later on.

| Type | Description | Default Location | Setting |
| --- | --- | --- | --- |
| home | {{kib}} home directory or `$KIBANA_HOME` | Directory created by unpacking the archive |  |
| bin | Binary scripts including `kibana` to start the {{kib}} server    and `kibana-plugin` to install plugins | `$KIBANA_HOME\bin` |  |
| config | Configuration files including `kibana.yml` | `$KIBANA_HOME\config` | `[KBN_PATH_CONF](configure-kibana.md)` |
| data | The location of the data files written to disk by {{kib}} and its plugins | `$KIBANA_HOME\data` |  |
| plugins | Plugin files location. Each plugin will be contained in a subdirectory. | `$KIBANA_HOME\plugins` |  |

## Next steps

:::{include} _snippets/install-kib-next-steps.md
:::