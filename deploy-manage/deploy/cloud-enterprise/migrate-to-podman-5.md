---
applies_to:
  deployment:
    ece: all
---
# Migrating to Podman 5

Following are the supported upgrade paths for Podman 5 in {{ece}}.

| **From ↓** ...       **To →**           | Podman 5.2.2-9 | Podman 5.2.2-11 | Podman 5.2.2-13 | Podman 5.2.3 |
|-----------------------------------------|----------------|-----------------|-----------------|--------------|
| **<vanilla Linux installation> (grow)** | ✓ ^*^          | ✓ ^*^           | ✓               | X            |
| **Docker (grow-and-shrink)**            | ✓ ^*^          | ✓ ^*^           | ✓               | X            |
| **Podman 4.9.4 (grow-and-shrink)**      | ✓ ^*^          | ✓ ^*^           | ✓               | X            |
| **Podman 4.9.4 (in-place)**             | ✓              | X               | X               | X            |
| **Podman 5.2.2-9 (in-place)**           | -              | X               | X               | X            |




^*^ *Supported but not recommended given that a newer version (Podman `5.2.2-13`) is available.*

Podman `5.2.2-13` is only supported when conducting a **fresh {{ece}} installation** or performing a **grow-and-shrink update** from Docker or Podman 4.

For **in-place updates**, it is recommended to use Podman `5.2.2-9`, since upgrades to versions `5.2.2-11` and `5.2.2-13` are affected by a known [memory leak issue](https://github.com/containers/podman/issues/25473).
When performing an in-place update, make sure to configure the Podman version to be locked at version `5.2.2-9.*`, by following the instructions below.

```sh
## Install versionlock
sudo dnf install 'dnf-command(versionlock)'

## Lock major version
sudo dnf versionlock add --raw 'podman-5.2.2-9.*'
sudo dnf versionlock add --raw 'podman-remote-5.2.2-9.*'

## Verify that podman-5.2.2-9.* and podman-remote-5.2.2-9.* appear in the output
sudo dnf versionlock list
```

Podman versions `5.2.3` and higher are not supported.