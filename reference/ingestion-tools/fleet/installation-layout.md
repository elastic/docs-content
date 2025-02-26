---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/installation-layout.html
---

# Installation layout [installation-layout]

{{agent}} files are installed in the following locations.

:::::::{tab-set}

::::::{tab-item} macOS
`/Library/Elastic/Agent/*`
:   {{agent}} program files

`/Library/Elastic/Agent/elastic-agent.yml`
:   Main {{agent}} configuration

`/Library/Elastic/Agent/fleet.enc`
:   Main {{agent}} {{fleet}} encrypted configuration

`/Library/Elastic/Agent/data/elastic-agent-*/logs/elastic-agent.ndjson`
:   Log files for {{agent}} and {{beats}} shippers ^1^

`/usr/bin/elastic-agent`
:   Shell wrapper installed into PATH

You can install {{agent}} in a custom base path other than `/Library`.  When installing {{agent}} with the `./elastic-agent install` command, use the `--base-path` CLI option to specify the custom base path.
::::::

::::::{tab-item} Linux
`/opt/Elastic/Agent/*`
:   {{agent}} program files

`/opt/Elastic/Agent/elastic-agent.yml`
:   Main {{agent}} configuration

`/opt/Elastic/Agent/fleet.enc`
:   Main {{agent}} {{fleet}} encrypted configuration

`/opt/Elastic/Agent/data/elastic-agent-*/logs/elastic-agent.ndjson`
:   Log files for {{agent}} and {{beats}} shippers ^1^

`/usr/bin/elastic-agent`
:   Shell wrapper installed into PATH

You can install {{agent}} in a custom base path other than `/opt`.  When installing {{agent}} with the `./elastic-agent install` command, use the `--base-path` CLI option to specify the custom base path.
::::::

::::::{tab-item} Windows
`C:\Program Files\Elastic\Agent*`
:   {{agent}} program files

`C:\Program Files\Elastic\Agent\elastic-agent.yml`
:   Main {{agent}} configuration

`C:\Program Files\Elastic\Agent\fleet.enc`
:   Main {{agent}} {{fleet}} encrypted configuration

`C:\Program Files\Elastic\Agent\data\elastic-agent-*\logs\elastic-agent.ndjson`
:   Log files for {{agent}} and {{beats}} shippers ^1^

You can install {{agent}} in a custom base path other than `C:\Program Files`.  When installing {{agent}} with the `.\elastic-agent.exe install` command, use the `--base-path` CLI option to specify the custom base path.
::::::

::::::{tab-item} DEB
`/usr/share/elastic-agent/*`
:   {{agent}} program files

`/etc/elastic-agent/elastic-agent.yml`
:   Main {{agent}} configuration

`/etc/elastic-agent/fleet.enc`
:   Main {{agent}} {{fleet}} encrypted configuration

`/var/lib/elastic-agent/data/elastic-agent-*/logs/elastic-agent.ndjson`
:   Log files for {{agent}} and {{beats}} shippers ^1^

`/usr/bin/elastic-agent`
:   Shell wrapper installed into PATH
::::::

::::::{tab-item} RPM
`/usr/share/elastic-agent/*`
:   {{agent}} program files

`/etc/elastic-agent/elastic-agent.yml`
:   Main {{agent}} configuration

`/etc/elastic-agent/fleet.enc`
:   Main {{agent}} {{fleet}} encrypted configuration

`/var/lib/elastic-agent/data/elastic-agent-*/logs/elastic-agent.ndjson`
:   Log files for {{agent}} and {{beats}} shippers ^1^

`/usr/bin/elastic-agent`
:   Shell wrapper installed into PATH
::::::

:::::::

^1^ Logs file names end with a date `(YYYYMMDD)` and optional number: `elastic-agent-YYYYMMDD.ndjson`, `elastic-agent-YYYYMMDD-1.ndjson`, and so on as new files are created during rotation.
