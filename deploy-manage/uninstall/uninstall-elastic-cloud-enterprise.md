---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-uninstall.html
---

# Uninstall Elastic Cloud Enterprise [ece-uninstall]

You might need to remove Elastic Cloud Enterprise for one of the following reasons:

* If the installation process does not complete successfully and you cannot troubleshoot the issue.
* If you are de-provisioning a host and want to remove the installed Elastic Cloud Enterprise software.

You remove Elastic Cloud Enterprise by removing all containers on the host:

* If using Docker

::::{admonition} 
```sh
docker rm -f frc-runners-runner frc-allocators-allocator $(docker ps -a -q); sudo rm -rf /mnt/data/elastic/ && docker ps -a
```

::::


* If using Podman

::::{admonition} 
```sh
sudo podman rm -f frc-runners-runner frc-allocators-allocator $(sudo podman ps -a -q); sudo rm -rf /mnt/data/elastic && sudo podman ps -a
```

::::


If you plan to reinstall Elastic Cloud Enterprise on the host, make sure you [delete the host](../maintenance/ece/delete-ece-hosts.md) from the Cloud UI first. Reinstallation can fail if the host is still associated with your old Elastic Cloud Enterprise installation.

::::{warning} 
During installation, the system generates secrets that are placed into the `/mnt/data/elastic/bootstrap-state/bootstrap-secrets.json` secrets file, unless you passed in a different path with the --host-storage-path parameter. Keep the information in the `bootstrap-secrets.json` file secure by removing it from its default location and placing it into a secure storage location.
::::


