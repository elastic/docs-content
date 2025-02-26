---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/upgrade-standalone.html
---

# Upgrade standalone Elastic Agents [upgrade-standalone]

To upgrade a standalone agent running on an edge node:

1. Make sure the `elastic-agent` service is running.
2. From the directory where {{agent}} is installed, run the `upgrade` command to upgrade to a new version. Not sure where the agent is installed? Refer to [Installation layout](/reference/ingestion-tools/fleet/installation-layout.md).

    For example, on macOS, to upgrade the agent from version 8.8.0 to 8.8.1, you would run:

    ```shell
    cd /Library/Elastic/Agent/
    sudo elastic-agent upgrade 8.8.1
    ```


This command upgrades the binary. Your agent policy should continue to work, but you might need to upgrade it to use new features and capabilities.

For more command-line options, see the help for the [`upgrade`](/reference/ingestion-tools/fleet/agent-command-reference.md#elastic-agent-upgrade-command) command.

## Upgrading standalone {{agent}} in an air-gapped environmment [upgrade-standalone-air-gapped]

The basic upgrade scenario should work for most use cases. However, in an air-gapped environment {{agent}} is not able to access the {{artifact-registry}} at `artifacts.elastic.co` directly.

As an alterative, you can do one of the following:

* [Configure a proxy server](/reference/ingestion-tools/fleet/fleet-agent-proxy-support.md) for standalone {{agent}} to access the {{artifact-registry}}.
* [Host your own artifact registry](/reference/ingestion-tools/fleet/air-gapped.md#host-artifact-registry) for standalone {{agent}} to access binary downloads.

As well, starting from version 8.9.0, during the upgrade process {{agent}} needs to download a PGP/GPG key. Refer to [Configure {{agents}} to download a PGP/GPG key from {{fleet-server}}](/reference/ingestion-tools/fleet/air-gapped.md#air-gapped-pgp-fleet) for the steps to configure the key download location in an air-gapped environment.

Refer to [Air-gapped environments](/reference/ingestion-tools/fleet/air-gapped.md) for more details.


## Verifying {{agent}} package signatures [upgrade-standalone-verify-package]

Standalone {{agent}} verifies each package that it downloads using publically available SHA hash and .asc PGP signature files. The SHA file is used to verify that the package has not been modified, and the .asc file is used to verify that the package was released by Elastic. For this purpose, the Elastic public GPG key is embedded in {{agent}} itself.

At times, the Elastic private GPG key may need to be rotated, either due to the key expiry or due to the private key having been exposed. In this case, standalone {{agent}} upgrades can fail because the embedded public key no longer works.

In the event of a private GPG key rotation, you can use the following options with the [`upgrade`](/reference/ingestion-tools/fleet/agent-command-reference.md#elastic-agent-upgrade-command) command to either skip the verification process (not recommended) or force {{agent}} to use a new public key for verification:

`--skip-verify`
:   Skip the package verification process. This option is not recommended as it is insecure.

    Example:

    ```yaml
    ./elastic-agent upgrade 8.8.0 --skip-verify
    ```


`--pgp-path <string>`
:   Use a locally stored copy of the PGP key to verify the upgrade package.

    Example:

    ```yaml
    ./elastic-agent upgrade 8.8.0 --pgp-path /home/elastic-agent/GPG-KEY-elasticsearch
    ```


`--pgp-uri <string>`
:   Use the specified online PGP key to verify the upgrade package.

    Example:

    ```yaml
    ./elastic-agent upgrade 8.7.0-SNAPSHOT --pgp-uri "https://artifacts.elastic.co/GPG-KEY-elasticsearch"
    ```


Under the basic upgrade scenario standalone {{agent}} will automatically fetch the most current public key, however in an air-gapped environment or in the event that the {{artifact-registry}} is otherwise inaccessible, these commands can be used instead.


