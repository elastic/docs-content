---
navigation_title: Windows
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/windows.html
products:
  - id: kibana
---

# Install {{kib}} on Windows [windows]

{{kib}} can be installed on Windows using the `.zip` package.

:::{include} _snippets/trial.md
:::

:::{include} _snippets/kib-releases.md
:::

## Step 1: Download and install the `.zip` package [install-windows]

::::{tab-set}

:::{tab-item} Latest
Download the .zip windows archive for {{kib}} {{version.stack}} from [https://artifacts.elastic.co/downloads/kibana/kibana-{{version.stack}}-windows-x86_64.zip](https://artifacts.elastic.co/downloads/kibana/kibana-{{version.stack}}-windows-x86_64.zip)

Unzip it with your favorite unzip tool. This will create a folder with the following name:

```text subs=true
kibana-{{version.stack}}-windows-x86_64
```
We will refer to this folder as `$KIBANA_HOME`.

In a terminal window, CD to the `$KIBANA_HOME` directory, for instance:

```sh subs=true
CD c:\kibana-{{version.stack}}-windows-x86_64
```
:::

:::{tab-item} Specific version
Download the `.zip` archive for the {{kib}} version that you want from the [Past Releases](https://www.elastic.co/downloads/past-releases) page. 
If you're unsure about which version to install, refer to [{{es}} version](/deploy-manage/deploy/self-managed/install-kibana.md#elasticsearch-version) for more information about version compatibility.

Unzip it with your favorite unzip tool. This will create a folder called `kibana-<SPECIFIC.VERSION.NUMBER>-windows-x86_64`, where `<SPECIFIC.VERSION.NUMBER>` is the version you downloaded. We will refer to this folder as `$KIBANA_HOME`. 

In a terminal window, CD to the `$KIBANA_HOME` directory, for instance:

```sh subs=true
CD c:\kibana-<SPECIFIC.VERSION.NUMBER>}-windows-x86_64
```
Replace `<SPECIFIC.VERSION.NUMBER>` with the {{kib}} version number you installed. 
:::
::::

## Step 2: Start {{es}} and generate an enrollment token for {{kib}} [windows-enroll]

[Start {{es}}](/deploy-manage/maintenance/start-stop-services/start-stop-elasticsearch.md).

:::{include} _snippets/auto-security-config.md
:::

:::{include} _snippets/new-enrollment-token.md
:::

## Step 3 (Optional): Make {{kib}} externally accessible

:::{include} _snippets/kibana-ip.md
:::

## Step 4: Run {{kib}} from the command line [windows-running]

{{kib}} can be started from the command line as follows:

```sh
.\bin\kibana.bat
```

By default, {{kib}} runs in the foreground, prints its logs to `STDOUT`, and can be stopped by pressing `Ctrl`+`C`.

:::{include} _snippets/enroll-steps.md
:::

## Step 4: Configure {{kib}} using the config file [windows-configuring]

{{kib}} loads its configuration from the `$KIBANA_HOME/config/kibana.yml` file by default.  The format of this config file is explained in [](configure-kibana.md).

## Directory layout of `.zip` archive [windows-layout]

The `.zip` package is entirely self-contained. All files and directories are, by default, contained within `$KIBANA_HOME` — the directory created when unpacking the archive.

This is very convenient because you don’t have to create any directories to start using {{kib}}, and uninstalling {{kib}} is as easy as removing the `$KIBANA_HOME` directory.  However, it is advisable to change the default locations of the config and data directories so that you do not delete important data later on.

| Type | Description | Default Location | Setting |
| --- | --- | --- | --- |
| home | {{kib}} home directory or `$KIBANA_HOME` | Directory created by unpacking the archive |  |
| bin | Binary scripts including `kibana` to start the {{kib}} server    and `kibana-plugin` to install plugins | `$KIBANA_HOME\bin` |  |
| config | Configuration files including `kibana.yml` | `$KIBANA_HOME\config` | `[KBN_PATH_CONF](configure-kibana.md)` |
|  | data | The location of the data files written to disk by {{kib}} and its plugins | `$KIBANA_HOME\data` |
|  | plugins | Plugin files location. Each plugin will be contained in a subdirectory. | `$KIBANA_HOME\plugins` |

## Next steps

:::{include} _snippets/install-kib-next-steps.md
:::