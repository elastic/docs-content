::::{admonition} Startup timeouts with older systemd versions
:class: tip

By default {{es}} sets the `TimeoutStartSec` parameter to `systemd` to `900s`. If you are running at least version 238 of `systemd`, then {{es}} can automatically extend the startup timeout, and will do so repeatedly until startup is complete even if it takes longer than 900s.

Versions of `systemd` prior to 238 do not support the timeout extension mechanism and will terminate the {{es}} process if it has not fully started up within the configured timeout. If this happens, {{es}} will report in its logs that it was shut down normally a short time after it started:

```text
[2022-01-31T01:22:31,077][INFO ][o.e.n.Node               ] [instance-0000000123] starting ...
...
[2022-01-31T01:37:15,077][INFO ][o.e.n.Node               ] [instance-0000000123] stopping ...
```

However the `systemd` logs will report that the startup timed out:

```text
Jan 31 01:22:30 debian systemd[1]: Starting {{es}}...
Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Start operation timed out. Terminating.
Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Main process exited, code=killed, status=15/TERM
Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Failed with result 'timeout'.
Jan 31 01:37:15 debian systemd[1]: Failed to start {{es}}.
```

To avoid this, upgrade your `systemd` to at least version 238. You can also temporarily work around the problem by extending the `TimeoutStartSec` parameter.

::::