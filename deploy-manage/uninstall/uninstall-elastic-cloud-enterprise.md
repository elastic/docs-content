---
mapped_urls:
  -  https://www.elastic.co/guide/en/cloud-enterprise/current/ece-uninstall.html
applies_to:
  deployment:
    ece: 
---

# Uninstall {{ece}} [ece-uninstall]

This guide provides instructions for uninstalling {{ece}} from a specific host within an {{ece}} platform. This process removes the {{ece}} software from the host but does not uninstall the entire {{ece}} platform.

You might need to remove {{ece}} for one of the following reasons:

* The installation process does not complete successfully and you can't troubleshoot the issue.
* You are de-provisioning a host and want to remove the installed {{ece}} software.

::::{important}
If the {{ece}} host you are uninstalling has the allocator role and is running instances from orchestrated deployments, all containers will be deleted, causing the instances to appear unhealthy on the Deployments page. To avoid disruptions, it is recommended to [vacate the host](/deploy-manage/maintenance/ece/move-nodes-instances-from-allocators.md) before uninstalling {{ece}}.
::::

You can remove {{ece}} by removing all containers on the host:

* If using Docker:

  ```sh
  docker rm -f frc-runners-runner frc-allocators-allocator $(docker ps -a -q); sudo rm -rf /mnt/data/elastic/ && docker ps -a
  ```

* If using Podman:

  ```sh
  sudo podman rm -f frc-runners-runner frc-allocators-allocator $(sudo podman ps -a -q); sudo rm -rf /mnt/data/elastic && sudo podman ps -a
  ```

If you plan to reinstall {{ece}} on the host, make sure you [delete the host](../maintenance/ece/delete-ece-hosts.md) from the Cloud UI first. Reinstallation can fail if the host is still associated with your old {{ece}} installation.

::::{warning} 
During installation, the system generates secrets that are placed into the `/mnt/data/elastic/bootstrap-state/bootstrap-secrets.json` secrets file, unless you passed in a different path with the `--host-storage-path` parameter. Keep the information in the `bootstrap-secrets.json` file secure by removing it from its default location and placing it into a secure storage location.
::::

