---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-install-using-podman-cloud.html
---

# Fresh installation of ECE using Podman hosts cloud [ece-install-using-podman-cloud]

This section provides guidelines and recommendations to install ECE using a Podman-based environment. The recommended approach consists of two (2) high-level steps.

**Step 1**: Install ECE.

**Step 2**: Add additional Podman hosts

::::{note} 
When copy-pasting commands, verify that characters like quotes (“) are encoded correctly in the console where you copy the command to.
::::


::::{note} 
Steps that run commands starting with `sudo` can be run as any sudoers user. Otherwise, the corresponding user is mentioned as part of the step description.
::::


::::{note} 
Avoid customizing the host Docker path `/mnt/data/docker` when using SELinux. Otherwise the ECE installer script needs to be adjusted.
::::


1. Install ECE

    Use the ECE installer script together with the `--podman` flag.

    Refer to the official [Install ECE online](install-ece-onprem.md) documentation to adapt the command line parameters to your environment.

    [JVM heap sizes](ece-jvm.md) describes recommended JVM options.

    ::::{important} 
    Important while running `./elastic-cloud-enterprise.sh`

    * Execute the installer script as user `elastic`.
    * Ensure to use an installer script that supports podman.
    * Make sure you use `--podman`.
    * Use `--cloud-enterprise-version VERSION_NAME` to specify the correct version.
    * If you are using SELinux, make sure you also use `--selinux`.

    ::::

2. Add additional Podman hosts

    Refer to the official [Install Elastic Cloud Enterprise on an additional host](install-ece-on-additional-hosts.md) and [Install ECE online](install-ece-onprem.md) documentation to adapt the command line parameters to your environment including fetching the role token.

    [JVM heap sizes](ece-jvm.md) describes recommended JVM options.

    ::::{important} 
    Important while running `./elastic-cloud-enterprise.sh`

    * Execute the installer script as user `elastic`.
    * Ensure to use an installer script that supports podman.
    * Make sure you use `--podman`.
    * If you are using SELinux, make sure you also use `--selinux`.
    * To fetch a role token following the [Generate Roles Tokens](generate-roles-tokens.md) guidelines, you need to send a JSON token to the admin console. Double check the correct format of the roles. Roles are a list of individual strings in quotes, **NOT a single string**.

        **Example**

        ```json
        { "persistent": true, "roles": [ "allocator","coordinator","director","proxy" ] }
        ```

    * The ECE version of the additional host must be the same as the version used in step 2. Use `--cloud-enterprise-version VERSION_NAME` to specify the correct version.
    * Make sure to apply the roles to the additional host. The value for the `--roles` flag is a single string.

        **Example**

        ```sh
        --roles "allocator,coordinator,director,proxy"
        ```


    ::::


    To add a new allocator, use `--roles "allocator"`. To add a new coordinator, director, proxy, and allocator, use `--roles "allocator,coordinator,director,proxy"`


