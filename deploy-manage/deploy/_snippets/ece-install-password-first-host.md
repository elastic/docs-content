:::{tip}
:applies_to: ece: ga 4.3+
To protect the bootstrap secrets that additional hosts read when they join, configure an install password. Add `--install-password 'PASSWORD'` to the installation command, or set the `INSTALL_PASSWORD` environment variable before you run the script. Every additional host must use the same password. Refer to [](/deploy-manage/security/secure-your-elastic-cloud-enterprise-installation/configure-ece-install-password.md).
:::
