---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-migrate-to-selinux-in-enforcing-mode.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Migrate ECE on Podman hosts to SELinux enforce [ece-migrate-to-selinux-in-enforcing-mode]

This section provides guidelines and recommendations for migrating an existing platform on a Podman-based environment to use SELinux in `enforcing` mode.

[SELinux](https://www.redhat.com/en/topics/linux/what-is-selinux) (Security-Enhanced Linux) is a security module that enforces mandatory access controls, helping to protect systems from unauthorized access and privilege escalation. Running in enforcing mode ensures that security policies are strictly applied, which can improve security and compliance in hardened environments.

The migration process consists of four high-level steps. Steps 2-4 need to be repeated for each host in your environment.

**Step 1** Migrate existing ECE installation to version >=3.7.2

**Step 2** Put host into maintenance mode

**Step 3** Switch to SELinux in `enforcing` mode

**Step 4** Remove maintenance mode

::::{important} 
We do not recommend to upgrade ECE and switch to SELinux in `enforcing` mode at the same time.
::::


::::{important} 
Execute the following steps on each ECE host, one after the other. Do not execute those steps on multiple hosts at the same time.
::::


Perform the following steps on each host of your {{ECE}} installation:

1. Ensure that SELinux is `disabled` on the host.

    ```bash
    $ sudo getenforce
    Disabled
    ```

2. Verify the SELinux labels on `/mnt/data/docker`.

    At this state, ECE is not running with SELinux enabled. We do not see any SELinux labels yet.

    ```bash
    $ sudo ls -alishZ /mnt/data/docker/
    total 848K
          132    0 drwx--x--x  10 elastic elastic ?  203 Nov 14 12:14 .
          128    0 drwxr-xr-x   4 elastic elastic ?   35 Nov  8 10:05 ..
          133 796K -rw-r--r--   1 root    root    ? 792K Nov 14 12:14 db.sql
    ```

3. Put the host into maintenance mode.
4. Set SELinux to `Permissive` mode ([Resource](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/using_selinux/changing-selinux-states-and-modes_using-selinux#changing-to-permissive-mode_changing-selinux-states-and-modes)) and reboot the host.

    ```bash
    $ sudo sed -i 's/SELINUX=.*/SELINUX=permissive/g'  /etc/selinux/config
    $ sudo reboot
    ```

5. Verify that SELinux is running in `permissive` mode.

    ```bash
    $ getenforce
    Permissive
    ```

6. Fix the SELinux file labels across the system. Run the following command and reboot the host ([Resource](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/using_selinux/changing-selinux-states-and-modes_using-selinux#enabling-selinux-on-systems-that-previously-had-it-disabled_changing-selinux-states-and-modes)).

    ```bash
    $ sudo fixfiles -F onboot
    System will relabel on next boot

    sudo reboot
    ```

7. Verify that SELinux labels are visible.

    ```bash
    $ sudo ls -alishZ /mnt/data/docker/
    total 848K
          132    0 drwx--x--x.  10 elastic elastic system_u:object_r:unlabeled_t:s0  203 Nov 14 12:26 .
          128    0 drwxr-xr-x.   4 elastic elastic system_u:object_r:unlabeled_t:s0   35 Nov  8 10:05 ..
          133 796K -rw-r--r--.   1 root    root    system_u:object_r:unlabeled_t:s0 792K Nov 14 12:26 db.sq
    ```

8. Run the `configure-selinux-settings` command of the ECE installer as user `elastic`.

    ::::{note} 
    Ensure that the flag `--podman` is used.
    ::::


    ```bash
    $ bash <(curl -fsSL https://download.elastic.co/cloud/elastic-cloud-enterprise.sh) configure-selinux-settings --podman
    ```

9. Verify that SELinux labels are visible. The labels change from `object_r:unlabeled_t` to `container_var_lib_t`.

    ```bash
    $ sudo ls -alishZ /mnt/data/docker/
    total 848K
          132    0 drwx--x--x.  10 elastic elastic system_u:object_r:container_var_lib_t:s0  203 Nov 14 12:31 .
          128    0 drwxr-xr-x.   4 elastic elastic system_u:object_r:mnt_t:s0                 35 Nov  8 10:05 ..
          133 796K -rw-r--r--.   1 root    root    system_u:object_r:container_var_lib_t:s0 792K Nov 14 12:31 db.sql
    ```

10. Use SELinux in `enforcing` mode ([Resource](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/using_selinux/changing-selinux-states-and-modes_using-selinux#changing-to-enforcing-mode_changing-selinux-states-and-modes)) and reboot the host.

    ```bash
    $ sudo sed -i 's/SELINUX=.*/SELINUX=enforcing/g'  /etc/selinux/config
    $ sudo reboot
    ```

11. Verify that SELinux is running in `enforcing` mode.

    ```bash
    $ getenforce
    Enforcing
    ```

12. Verify that all containers are healthy.
13. Remove the maintenance mode of the host.

