---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/profiling-no-kernel-version-check.html
applies_to:
  stack: ga
products:
  - id: observability
---

# Override kernel version check [profiling-no-kernel-version-check]

The `-no-kernel-version-check` flag, or the `no-kernel-version-check` key in the Universal Profiling Agent configuration file, controls the kernel version compatibility check during the Universal Profiling Agent’s startup process. The kernel version compatibility check enforces the minimum kernel version supported,  and prevents the profiling agent from running on certain kernel versions with known issues. When the `no-kernel-version-check` is set to `true`, the compatibility check is bypassed, allowing Universal Profiling Agent execution to proceed regardless of the kernel version. By default, this option is set to `false`, and the kernel compatibility version check is performed as usual.

::::{warning}
Take extra caution when using this configuration option, especially when running the Universal Profiling Agent on older kernels with backported eBPF functionalities. Setting this option to `true` on kernels with unfixed eBPF bugs can crash your system.
::::



## Host agent configuration example [profiling-no-kernel-example]

The following example shows how to configure the `-no-kernel-version-check` in the Universal Profiling agent CLI:

```bash
sudo pf-host-agent/pf-host-agent -no-kernel-version-check=true
```

It is also possible to use the environment variable `PRODFILER_NO_KERNEL_VERSION_CHECK=true` to set this configuration.

