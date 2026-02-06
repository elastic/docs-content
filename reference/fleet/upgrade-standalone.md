---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/upgrade-standalone.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Upgrade standalone Elastic Agents [upgrade-standalone]

To upgrade a standalone agent running on an edge node:

1. Make sure the `elastic-agent` service is running.
2. From the directory where {{agent}} is installed, run the `upgrade` command to upgrade to a new version. Not sure where the agent is installed? Refer to [Installation layout](/reference/fleet/installation-layout.md).

    For example, to upgrade the agent from version 9.1.0 to 9.1.1, you would run:

    :::::{tab-set}

    ::::{tab-item} macOS

    ```shell
    sudo elastic-agent upgrade 9.1.1
    ```

    ::::

    ::::{tab-item} Linux

    ```shell
    sudo elastic-agent upgrade 9.1.1
    ```

    ::::

    ::::{tab-item} Windows

    As an Administrator, run:

    ```shell
    .\elastic-agent.exe upgrade 9.1.1
    ```

    ::::

    ::::{tab-item} DEB

    ```shell
    sudo elastic-agent upgrade 9.1.1
    ```

    ::::

    ::::{tab-item} RPM

    ```shell
    sudo elastic-agent upgrade 9.1.1
    ```

    ::::

    :::::


This command upgrades the binary. Your agent policy should continue to work, but you might need to upgrade it to use new features and capabilities.

For more command-line options, see the help for the [`upgrade`](/reference/fleet/agent-command-reference.md#elastic-agent-upgrade-command) command.

## Upgrading standalone {{agent}} in an air-gapped environment [upgrade-standalone-air-gapped]

The basic upgrade scenario should work for most use cases. However, in an air-gapped environment {{agent}} is not able to access the {{artifact-registry}} at `artifacts.elastic.co` directly.

As an alterative, you can do one of the following:

* [Configure a proxy server](/reference/fleet/fleet-agent-proxy-support.md) for standalone {{agent}} to access the {{artifact-registry}}.
* [Host your own artifact registry](/reference/fleet/air-gapped.md#host-artifact-registry) for standalone {{agent}} to access binary downloads.

As well, starting from version 8.9.0, during the upgrade process {{agent}} needs to download a PGP/GPG key. Refer to [Configure {{agents}} to download a PGP/GPG key from {{fleet-server}}](/reference/fleet/air-gapped.md#air-gapped-pgp-fleet) for the steps to configure the key download location in an air-gapped environment.

Refer to [Air-gapped environments](/reference/fleet/air-gapped.md) for more details.


## Verifying {{agent}} package signatures [upgrade-standalone-verify-package]

Standalone {{agent}} verifies each package that it downloads using publicly available SHA hash and .asc PGP signature files. The SHA file is used to verify that the package has not been modified, and the .asc file is used to verify that the package was released by Elastic. For this purpose, the Elastic public GPG key is embedded in {{agent}} itself.

At times, the Elastic private GPG key may need to be rotated, either due to the key expiry or due to the private key having been exposed. In this case, standalone {{agent}} upgrades can fail because the embedded public key no longer works.

In the event of a private GPG key rotation, you can use the following options with the [`upgrade`](/reference/fleet/agent-command-reference.md#elastic-agent-upgrade-command) command to either skip the verification process (not recommended) or force {{agent}} to use a new public key for verification:

`--skip-verify`
:   Skip the package verification process. This option is not recommended as it is insecure.

    Example:

    ```yaml
    ./elastic-agent upgrade 9.1.0 --skip-verify
    ```


`--pgp-path <string>`
:   Use a locally stored copy of the PGP key to verify the upgrade package.

    Example:

    ```yaml
    ./elastic-agent upgrade 9.1.0 --pgp-path /home/elastic-agent/GPG-KEY-elasticsearch
    ```


`--pgp-uri <string>`
:   Use the specified online PGP key to verify the upgrade package.

    Example:

    ```yaml
    ./elastic-agent upgrade 8.7.0-SNAPSHOT --pgp-uri "https://artifacts.elastic.co/GPG-KEY-elasticsearch"
    ```


Under the basic upgrade scenario standalone {{agent}} will automatically fetch the most current public key, however in an air-gapped environment or in the event that the {{artifact-registry}} is otherwise inaccessible, these commands can be used instead.


## Roll back an Elastic Agent upgrade for standalone agents [rollback-upgrade-standalone]
```yaml {applies_to}
stack: ga 9.3.0+
serverless: ga
```

We have you covered in the unusual case that you need to rollback an upgrade for a standalone agent. 

Earlier {{agent}} versions could detect issues and automatically roll back to the previous installed version within ten minutes of an upgrade if needed.
This feature is still available and on by default. 

::::{admonition} Elastic subscription
The manual rollback feature for {{agent}} is available only for some [Elastic subscription levels]({{subscriptions}}).
::::

**Manual rollback.**
The manual rollback feature expands the time window for rollbacks, giving you the ability to roll back to the previous version within seven days.

To roll back a recent upgrade to the previously installed version (if it is still available on disk): 

:::::{tab-set}
::::{tab-item} macOS

```shell
sudo elastic-agent upgrade --rollback
```
::::

::::{tab-item} Linux
```shell
sudo elastic-agent upgrade --rollback
```
::::

::::{tab-item} Windows
As an Administrator, run:
```shell
.\elastic-agent.exe upgrade --rollback
```
::::

::::{tab-item} DEB
The manual rollback feature is not available for system-managed packages such as DEB and RPM. 
::::

::::{tab-item} RPM
The manual rollback feature is not available for system-managed packages such as DEB and RPM. 
::::
:::::


### Limitations for manual rollback (standalone agents) [rollback-upgrade-standalone-limitations]

These limitations apply for the manual rollback feature: 

* Rollback is limited to the version running _before_ the upgrade. Both the previously and currently running versions must be 9.3.0 or later for this functionality to be available.
* Data required for the rollback is stored on disk for seven days, which can impact available disk space.
* Rollback must be performed within seven days of the upgrade. Rollback data is automatically cleaned up after seven days and becomes unavailable.
* Manual rollback is not available for system-managed packages such as DEB and RPM.
* Some data might be re-ingested after rollback. 

#### Possible errors [rollback-upgrade-standalone-errors]

If no version is available on disk to rollback to, you get an error.
This situation can happen if:

- the version you upgraded from is earlier than 9.3.0, as the feature was not implemented in earlier versions. 

- the rollback window has ended (typically more than seven days). When the rollback window ends, the files from the previous version are removed to free up disk space. 
