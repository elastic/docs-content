---
navigation_title: Install password
description: Configure an ECE install password to protect the bootstrap secrets that additional hosts read when they join your installation.
applies_to:
  deployment:
    ece: ga 4.3+
products:
  - id: cloud-enterprise
---

# Configure an install password for ECE [ece-configure-install-password]

When you install {{ece}} on an additional host, the host reads a set of bootstrap secrets from the installation to join it. By default, any host that can reach the installation over the network can read these secrets. To protect them, you can set an install password. While a password is set, a host can only join when it is installed with the same password.

An install password is optional. {{ece}} doesn't generate or configure one automatically, even for a new installation. You can set it during the initial installation or add it to an existing installation later.

The install password doesn't replace the [roles token](/deploy-manage/deploy/cloud-enterprise/generate-roles-tokens.md), which a host still needs to join. It protects the bootstrap secrets only, so keep restricting network access to the installation to trusted hosts.

## Before you begin

If you upgrade an existing installation, set the install password only after every host runs {{ece}} 4.3 or later. On a host that still runs an earlier version, the services forwarder loses access to the bootstrap secrets when it restarts. If that happens, remove the password as described in the [`set-install-password` command reference](cloud://reference/cloud-enterprise/ece-installation-script-set-install-password.md).

## Configure a password for a new installation

To start a new installation with an install password, add `--install-password 'PASSWORD'` to the installation command on the first host, or set the password in the `INSTALL_PASSWORD` environment variable before you run the script. The environment variable keeps the password out of the installer command line.

Use this option with the other parameters required by your [installation procedure](/deploy-manage/deploy/cloud-enterprise/install-ece-procedures.md). Keep the password in a secure location so that you can use it when you add hosts.

## Configure or manage a password for an existing installation

To set, generate, rotate, or remove the install password of an existing installation, use the `set-install-password` command. For the required privileges, command options, and examples, refer to the [`set-install-password` command reference](cloud://reference/cloud-enterprise/ece-installation-script-set-install-password.md).

## Add hosts to a password-protected installation

After you set a password, install every additional host with the same password, using `--install-password 'PASSWORD'` or the `INSTALL_PASSWORD` environment variable. Without the correct password, the new host cannot read the secrets it needs to join and the installation fails.

Hosts that are already part of the installation don't need the install password.

For the complete procedure, refer to [](/deploy-manage/deploy/cloud-enterprise/install-ece-on-additional-hosts.md).
