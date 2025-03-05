---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-directory-layout.html
applies_to:
  stack: all
---

# Installation layout [apm-directory-layout]

View the installation layout and default paths for both Fleet-managed APM Server and the APM Server binary.


## Fleet-managed [_fleet_managed]

{{agent}} files are installed in the following locations. You cannot override these installation paths because they are required for upgrades.

:::::::{tab-set}

::::::{tab-item} macOS
`/Library/Elastic/Agent/*`
:   {{agent}} program files

`/Library/Elastic/Agent/elastic-agent.yml`
:   Main {{agent}} configuration

`/Library/Elastic/Agent/fleet.enc`
:   Main {{agent}} {{fleet}} encrypted configuration

`/Library/Elastic/Agent/data/elastic-agent-*/logs/elastic-agent.ndjson`
:   Log files for {{agent}} and {{beats}} shippers <sup class="footnote" id="_footnote_lognumbering">[<a id="_footnoteref_1" class="footnote" href="#_footnotedef_1" title="View footnote.">1</a>]</sup>

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
:   Log files for {{agent}} and {{beats}} shippers <sup class="footnoteref">[<a class="footnote" href="#_footnotedef_1" title="View footnote.">1</a>]</sup>

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
:   Log files for {{agent}} and {{beats}} shippers <sup class="footnoteref">[<a class="footnote" href="#_footnotedef_1" title="View footnote.">1</a>]</sup>

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
:   Log files for {{agent}} and {{beats}} shippers <sup class="footnoteref">[<a class="footnote" href="#_footnotedef_1" title="View footnote.">1</a>]</sup>

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
:   Log files for {{agent}} and {{beats}} shippers <sup class="footnoteref">[<a class="footnote" href="#_footnotedef_1" title="View footnote.">1</a>]</sup>

`/usr/bin/elastic-agent`
:   Shell wrapper installed into PATH
::::::

:::::::

## APM Server binary [_apm_server_binary]

APM Server uses the following default paths unless you explicitly change them.

:::::::{tab-set}

::::::{tab-item} ZIP, tar.gz, or TGZ
| Type | Description | Location |
| --- | --- | --- |
| home | Home of the APM Server installation. | `{extract.path}` |
| bin | The location for the binary files. | `{extract.path}` |
| config | The location for configuration files. | `{extract.path}` |
| data | The location for persistent data files. | `{extract.path}/data` |
| logs | The location for the logs created by APM Server. | `{extract.path}/logs` |

For the ZIP, tar.gz, or TGZ distributions, these paths are based on the location of the extracted binary file. This means that if you start APM Server with the following simple command, all paths are set correctly:

```sh
./apm-server
```
::::::

::::::{tab-item} Docker
| Type | Description | Location |
| --- | --- | --- |
| home | Home of the APM Server installation. | `/usr/share/apm-server` |
| bin | The location for the binary files. | `/usr/share/apm-server` |
| config | The location for configuration files. | `/usr/share/apm-server` |
| data | The location for persistent data files. | `/usr/share/apm-server/data` |
| logs | The location for the logs created by APM Server. | `/usr/share/apm-server/logs` |
::::::

::::::{tab-item} DEB & RPM
| Type | Description | Location |
| --- | --- | --- |
| home | Home of the APM Server installation. | `/usr/share/apm-server` |
| bin | The location for the binary files. | `/usr/share/apm-server/bin` |
| config | The location for configuration files. | `/etc/apm-server` |
| data | The location for persistent data files. | `/var/lib/apm-server` |
| logs | The location for the logs created by APM Server. | `/var/log/apm-server` |

For the deb and rpm distributions, these paths are set in the init script or in the systemd unit file.  Make sure that you start the APM Server service by using the preferred operating system method (init scripts or `systemctl`). Otherwise the paths might be set incorrectly.
::::::

:::::::
