---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/install-agent-msi.html
---

# Install Elastic Agent from an MSI package [install-agent-msi]

MSI is the file format and command line utility for the [Windows Installer](https://en.wikipedia.org/wiki/Windows_Installer). Windows Installer (previously known as Microsoft Installer) is an interface for Microsoft Windows that’s used to install and manage software on Windows systems. This section covers installing Elastic Agent through the MSI package repository.

The MSI package installer must be run by an administrator account. The installer won’t start without Windows admin permissions.


## Install {{agent}} [_install_agent]

1. Download the latest Elastic Agent MSI binary from the [{{agent}} download page](https://www.elastic.co/downloads/elastic-agent).
2. Run the installer. The command varies slightly depending on whether you’re using the default Windows command prompt or PowerShell.

    ::::{admonition}
    * Using the default command prompt:

        ```shell
        elastic-agent-<VERSION>-windows-x86_64.msi INSTALLARGS="--url=<URL> --enrollment-token=<TOKEN>"
        ```

    * Using PowerShell:

        ```shell
        ./elastic-agent-<VERSION>-windows-x86_64.msi --% INSTALLARGS="--url=<URL> --enrollment-token=<TOKEN>"
        ```


    ::::


    Where:

    * `VERSION` is the {{stack}} version you’re installing, indicated in the MSI package name. For example, `8.13.2`.
    * `URL` is the {{fleet-server}} URL used to enroll the {{agent}} into {{fleet}}. You can find this on the {{fleet}} **Settings** tab in {{kib}}.
    * `TOKEN` is the authentication token used to enroll the {{agent}} into {{fleet}}. You can find this on the {{fleet}} **Enrollment tokens** tab.

    When you run the command, the value set for `INSTALLARGS` will be passed to the [`elastic-agent install`](/reference/ingestion-tools/fleet/agent-command-reference.md#elastic-agent-install-command) command verbatim.

3. If you need to troubleshoot, you can install using `msiexec` with the `-L*V "log.txt"` option to create installation logs:

    ```shell
    msiexec -i elastic-agent-<VERSION>-windows-x86_64.msi INSTALLARGS="--url=<URL> --enrollment-token=<TOKEN>"  -L*V "log.txt"
    ```



## Installation notes [_installation_notes]

Installing using an MSI package has the following behaviors:

* If `INSTALLARGS` are not provided, the MSI will copy the files to a temporary folder and finish.
* If `INSTALLARGS` are provided, the MSI will copy the files to a temporary folder and then run the [`elastic-agent install`](/reference/ingestion-tools/fleet/agent-command-reference.md#elastic-agent-install-command) command with the provided parameters. If the install flow is successful, the temporary folder is deleted.
* If `INSTALLARGS` are provided but the `elastic-agent install` command fails, the top-level folder is NOT deleted, in order to allow for further troubleshooting.
* If the `elastic-agent install` command fails for any reason, the MSI will rollback all changes.
* If the {{agent}} enrollment fails, the install will fail as well. To avoid this behavior you can add the [`--delay-enroll`](/reference/ingestion-tools/fleet/agent-command-reference.md#elastic-agent-install-command) option to the install command.


## Upgrading [_upgrading]

The {{agent}} version can be upgraded via {{fleet}}, but the registered MSI version will display the initially installed version (this shortcoming will be addressed in future releases). Attempts to upgrade outside of {{fleet}} via the MSI will require an uninstall and reinstall procedure to upgrade. Also note that this MSI implementation relies on the tar {{agent}} binary to upgrade the installation. Therefore if the {{agent}} is installed in an air-gapped environment, you must ensure that the tar image is available before an upgrade request is issued.


## Installing in a custom location [_installing_in_a_custom_location]

Starting in version 8.13, it’s also possible to override the default installation folder by running the MSI from the command line, as shown:

```shell
elastic-agent-<VERSION>-windows-x86_64.msi INSTALLARGS="--url=<URL> --enrollment-token=<TOKEN>" INSTALLDIR="<path of custom folder>"
```

