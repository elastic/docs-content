---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-users-permissions.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Users and permissions prerequisites [ece-users-permissions]

The following users and permissions are required:

* To prepare your environment: A user with `sudo` permissions, such as the *ubuntu* user provided on Ubuntu.
* To install ECE: A user with a UID and GID greater than or equal to 1000 who is part of the `docker` group. You must not install ECE as the `root` user.

You can find out information about a user with the `id` command:

```
id
uid=1000(elastic) gid=1000(elastic) groups=1000(elastic),
4(adm),20(dialout),24(cdrom),25(floppy),
27(sudo),29(audio),30(dip),44(video),
46(plugdev),102(netdev),112(libvirtd),1001(docker)
```
In this example, the user `elastic` with a UID and GID of 1000 belongs to both the `sudo` and the `docker` groups.

::::{note} 
For ECE installation with Podman, the user does not need to be added to the `docker` group. Instead, the user must be added to the `podman` group.
::::


