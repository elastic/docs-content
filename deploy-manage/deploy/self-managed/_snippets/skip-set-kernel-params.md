::::{note}
On systemd-based distributions, the installation scripts will attempt to set kernel parameters (e.g., `vm.max_map_count`). You can skip this by masking the `systemd-sysctl.service` unit.
::::