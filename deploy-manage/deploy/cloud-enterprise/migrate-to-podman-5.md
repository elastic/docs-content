---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-podman-5-migration.html
applies_to:
  deployment:
    ece: all
---
# Migrating to Podman 5

This guide describes the supported ways to upgrade or migrate your {{ece}} (ECE) hosts to Podman 5. There are two primary methods:

* **In-place upgrade**: Update Podman directly on existing ECE hosts without replacing them. In-place upgrades to Podman 5 are only supported from existing Podman-based hosts.

* **Grow-and-shrink upgrade**: [Add new hosts](./install-ece-on-additional-hosts.md) running the desired Podman version to your ECE installation, then [remove the old ones](/deploy-manage/uninstall/uninstall-elastic-cloud-enterprise.md). This method is safer and preferred, as it avoids potential risks associated with upgrading the container engine or the operating system in place.

ECE only supports Podman 5 in version `5.2.2`, regardless of your upgrade method. Later versions such as `5.2.3` and above are not supported. Refer always to the official [Support matrix](https://www.elastic.co/support/matrix#elastic-cloud-enterprise) for details on supported versions.

:::{important}
Podman versions `5.2.2-11` and `5.2.2-13` are affected by a known [memory leak issue](https://github.com/containers/podman/issues/25473). To avoid this issue, use a later build such as `5.2.2-16` or newer. 
:::

The following table summarizes the supported upgrade paths to Podman 5 in ECE.

| **From ↓** ...       **To →**           | Podman 5.2.2-latest | Podman 5.2.3 |
|-----------------------------------------|-----------------|--------------|
| **<vanilla Linux installation> (grow)** | ✓               | X            |
| **Docker (grow-and-shrink)**            | ✓               | X            |
| **Podman 4.9.4 (grow-and-shrink)**      | ✓               | X            |
| **Podman 4.9.4 (in-place)**             | ✓               | X            |
| **Podman 5.2.2 (grow-and-shrink)**      | ✓               | X            |
| **Podman 5.2.2 (in-place)**             | ✓               | X            |

As shown in the table above, [migrations from Docker](./migrate-ece-to-podman-hosts.md) are only supported using the grow-and-shrink method.
