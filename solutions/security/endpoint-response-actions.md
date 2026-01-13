---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/response-actions.html
  - https://www.elastic.co/guide/en/serverless/current/security-response-actions.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Endpoint response actions

The response console allows you to perform response actions on an endpoint using a terminal-like interface. You can enter action commands and get near-instant feedback on them. Actions are also recorded in the endpoint’s [response actions history](/solutions/security/endpoint-response-actions.md#actions-log) for reference.

Response actions are supported on all endpoint platforms (Linux, macOS, and Windows).

::::{admonition} Requirements
* Response actions and the response console UI require the appropriate [subscription](https://www.elastic.co/pricing) in {{stack}} or [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md) in {{serverless-short}}.
* Endpoints must have {{agent}} version 8.4 or higher installed with the {{elastic-defend}} integration to receive response actions.
* Some response actions require:
  * In {{stack}}, specific [privileges](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md), indicated below.
  * In {{serverless-short}}, either a [predefined Security user role](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles) or a [custom role](/deploy-manage/users-roles/cloud-organization/user-roles.md) with a specific feature privilege, indicated below.

  These are required to perform actions both in the response console and in other areas of the {{security-app}} (such as isolating a host from a detection alert).
* Users must have the appropriate user role or privileges for at least one response action to access the response console.
::::


:::{image} /solutions/images/security-response-console.png
:alt: Response console UI
:width: 90%
:screenshot:
:::

Launch the response console from any of the following places in {{elastic-sec}}:

* **Endpoints** page → **Actions** menu (**…**) → **Respond**
* Endpoint details flyout → **Take action** → **Respond**
* Alert details flyout → **Take action** → **Respond**
* Host details page → **Respond**
* {applies_to}`stack: ga 9.1` {applies_to}`serverless: ga` Event details flyout → **Take action** → **Respond** 

To perform an action on the endpoint, enter a [response action command](/solutions/security/endpoint-response-actions.md#response-action-commands) in the input area at the bottom of the console, then press **Return**. Output from the action is displayed in the console.

If a host is unavailable, pending actions will execute once the host comes online. Pending actions expire after two weeks and can be tracked in the response actions history.

::::{note}
Some response actions may take a few seconds to complete. Once you enter a command, you can immediately enter another command while the previous action is running.
::::


Activity in the response console is persistent, so you can navigate away from the page and any pending actions you’ve submitted will continue to run. To confirm that an action completed, return to the response console to view the console output or check the [response actions history](/solutions/security/endpoint-response-actions.md#actions-log).

::::{important}
Once you submit a response action, you can’t cancel it, even if the action is pending for an offline host.
::::


## Response action commands [response-action-commands]

The following response action commands are available in the response console.


### `isolate` [_isolate]

[Isolate the host](/solutions/security/endpoint-response-actions/isolate-host.md), blocking communication with other hosts on the network.

Predefined role (in {{serverless-short}}): **Tier 3 analyst**, **SOC manager**, or **Endpoint operations analyst**

Required privilege (in {{stack}}) or custom role privilege (in {{serverless-short}}): **Host Isolation**

Example: `isolate --comment "Isolate host related to detection alerts"`


### `release` [_release]

Release an isolated host, allowing it to communicate with the network again.

Predefined role (in {{serverless-short}}): **Tier 3 analyst**, **SOC manager**, or **Endpoint operations analyst**

Required privilege (in {{stack}}) or custom role privilege (in {{serverless-short}}): **Host Isolation**

Example: `release --comment "Release host, everything looks OK"`


### `status` [_status]

Show information about the host’s status, including: {{agent}} status and version, the {{elastic-defend}} integration’s policy status, and when the host was last active.


### `processes` [processes]

Show a list of all processes running on the host. This action may take a minute or so to complete.

Predefined role (in {{serverless-short}}): **Tier 3 analyst**, **SOC manager**, or **Endpoint operations analyst**

Required privilege (in {{stack}}) or custom role privilege (in {{serverless-short}}): **Process Operations**

::::{tip}
Use this command to get current PID or entity ID values, which are required for other response actions such as `kill-process` and `suspend-process`.

Entity IDs may be more reliable than PIDs, because entity IDs are unique values on the host, while PID values can be reused by the operating system.
::::


::::{note}
Running this command on third-party-protected hosts might return the process list in a different format. Refer to [](/solutions/security/endpoint-response-actions/third-party-response-actions.md) for more information.
::::


### `kill-process` [kill-process]

Terminate a process. You must include one of the following parameters to identify the process to terminate:

* `--pid` : A process ID (PID) representing the process to terminate.
* `--entityId` : An entity ID representing the process to terminate.

Predefined role (in {{serverless-short}}): **Tier 3 analyst**, **SOC manager**, or **Endpoint operations analyst**

Required privilege (in {{stack}}) or custom role privilege (in {{serverless-short}}): **Process Operations**

Example: `kill-process --pid 123 --comment "Terminate suspicious process"`

::::{note}
For SentinelOne-enrolled hosts, you must use the parameter `--processName` to identify the process to terminate. `--pid` and `--entityId` are not supported.

Example: `kill-process --processName cat --comment "Terminate suspicious process"`
::::


### `suspend-process` [_suspend_process]

Suspend a process. You must include one of the following parameters to identify the process to suspend:

* `--pid` : A process ID (PID) representing the process to suspend.
* `--entityId` : An entity ID representing the process to suspend.

Predefined role (in {{serverless-short}}): **Tier 3 analyst**, **SOC manager**, or **Endpoint operations analyst**

Required privilege (in {{stack}}) or custom role privilege (in {{serverless-short}}): **Process Operations**

Example: `suspend-process --pid 123 --comment "Suspend suspicious process"`


### `get-file` [get-file]

Retrieve a file from a host. Files are downloaded in a password-protected `.zip` archive to prevent the file from running. Use password `elastic` to open the `.zip` in a safe environment.

::::{note}
Files retrieved from third-party-protected hosts require a different password. Refer to [](/solutions/security/endpoint-response-actions/third-party-response-actions.md) for your system’s password.
::::


You must include the following parameter to specify the file’s location on the host:

* `--path` : The file’s full path (including the file name).

Predefined role (in {{serverless-short}}): **Tier 3 analyst**, **SOC manager**, or **Endpoint operations analyst**

Required privilege (in {{stack}}) or custom role privilege (in {{serverless-short}}): **File Operations**

Example: `get-file --path "/full/path/to/file.txt" --comment "Possible malware"`

::::{note}
:applies_to: {"stack": "removed 9.3", "serverless": "removed"}
The maximum file size that `get-file` can retrieve is `104857600` bytes, or 100 MB.
::::

::::{tip}
You can use the [Osquery manager integration](/solutions/security/investigate/osquery.md) to query a host’s operating system and gain insight into its files and directories, then use `get-file` to retrieve specific files.
::::


::::{note}
When {{elastic-defend}} prevents file activity due to [malware prevention](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#malware-protection), the file is quarantined on the host and a malware prevention alert is created. To retrieve this file with `get-file`, copy the path from the alert’s **Quarantined file path** field (`file.Ext.quarantine_path`), which appears under **Highlighted fields** in the alert details flyout. Then paste the value into the `--path` parameter.
::::


### `execute` [_execute]

Run a shell command on the host. The command’s output and any errors appear in the response console, up to 2000 characters. The complete output (stdout and stderr) are also saved to a downloadable `.zip` archive (password: `elastic`). Use these parameters:

* `--command` : (Required) A shell command to run on the host. The command must be supported by `bash` for Linux and macOS hosts, and `cmd.exe` for Windows.

    ::::{note}
    * Multiple consecutive dashes in the value must be escaped; single dashes do not need to be escaped. For example, to represent a directory named `/opt/directory--name`, use the following: `/opt/directory\-\-name`.
    * You can use quotation marks without escaping. For example:<br> `execute --command "cd "C:\Program Files\directory""`
    ::::

* `--timeout` : (Optional) How long the host should wait for the command to complete. Use `h` for hours, `m` for minutes, `s` for seconds (for example, `2s` is two seconds). If no timeout is specified, it defaults to four hours.

Predefined role (in {{serverless-short}}): **SOC manager** or **Endpoint operations analyst**

Required privilege (in {{stack}}) or custom role privilege (in {{serverless-short}}): **Execute Operations**

Example: `execute --command "ls -al" --timeout 2s --comment "Get list of all files"`

::::{warning}
This response action runs commands on the host using the same user account running the {{elastic-defend}} integration, which normally has full control over the system. Be careful with any commands that could cause irrevocable changes.
::::


### `upload` [_upload]

Upload a file to the host. The file is saved to the location on the host where {{elastic-endpoint}} is installed. After you run the command, the full path is returned in the console for reference. Use these parameters:

* `--file` : (Required) The file to send to the host. As soon as you type this parameter, a popup appears — select it to navigate to the file, or drag and drop the file onto the popup.
* `--overwrite` : (Optional) Overwrite the file on the host if it already exists.

Predefined role (in {{serverless-short}}): **Tier 3 analyst**, **SOC manager**, or **Endpoint operations analyst**

Required privilege (in {{stack}}) or custom role privilege (in {{serverless-short}}): **File Operations**

Example: `upload --file --comment "Upload remediation script"`

::::{tip}
You can follow this with the `execute` response action to upload and run scripts for mitigation or other purposes.
::::


::::{note}
The default file size maximum is 25 MB, configurable in [`kibana.yml`](/deploy-manage/stack-settings.md) with the `xpack.securitySolution.maxUploadResponseActionFileBytes` setting. You must enter the value in bytes. 

({applies_to}`stack: removed 9.4` the maximum value of `xpack.securitySolution.maxUploadResponseActionFileBytes` is `104857600` bytes, or 100 MB).
::::


### `scan` [_scan]

Scan a specific file or directory on the host for malware. This uses the [malware protection settings](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#malware-protection) (such as **Detect** or **Prevent** options, or enabling the blocklist) as configured in the host’s associated {{elastic-defend}} integration policy. Use these parameters:

* `--path` : (Required) The absolute path to a file or directory to be scanned.

Predefined role (in {{serverless-short}}): **Tier 3 Analyst**, **SOC Manager**, or **Endpoint Operations Analyst**

Required privilege (in {{stack}}) or custom role privilege (in {{serverless-short}}): **Scan Operations**

Example: `scan --path "/Users/username/Downloads" --comment "Scan Downloads folder for malware"`

::::{note}
Scanning can take longer for directories containing a lot of files.
::::


### `runscript` [runscript]

Run a script on a host. 

#### CrowdStrike

For CrowdStrike, you must include one of the following parameters to identify the script you want to run:

* `--Raw`: The full script content provided directly as a string.
* `--CloudFile`: The name of the script stored in a cloud storage location.

   {applies_to}`stack: ga 9.1` {applies_to}`serverless: ga` When using this parameter, select from a list of saved custom scripts.

* `--HostPath`: The absolute or relative file path of the script located on the host machine.

You can also use these optional parameters:

* `--CommandLine`: Additional command-line arguments passed to the script to customize its execution.
* `--Timeout`: The maximum duration, in seconds, that the script can run before it’s forcibly stopped. If no timeout is specified, it defaults to 60 seconds.

Predefined role (in {{serverless-short}}): **SOC manager** or **Endpoint operations analyst**

Required privilege (in {{stack}}) or custom role privilege (in {{serverless-short}}): **Execute Operations**

Examples:

`runscript --CloudFile="CloudScript1.ps1" --CommandLine="-Verbose true" --Timeout=180`

` runscript --Raw=```Get-ChildItem.``` `

`runscript --HostPath="C:\temp\LocalScript.ps1" --CommandLine="-Verbose true"`


#### Microsoft Defender for Endpoint
```yaml {applies_to}
stack: ga 9.1
serverless: ga
```

For Microsoft Defender for Endpoint, you must include the following parameter to identify the script you want to run:

* `--ScriptName`: The name of the script stored in a cloud storage location. Select from a list of saved custom scripts.

You can also use this optional parameter:

* `--Args`: Additional command-line arguments passed to the script to customize its execution.
  :::{note}
  The response console does not support double-dash (`--`) syntax within the `--Args` parameter.
  :::

Predefined role (in {{serverless-short}}): **SOC manager** or **Endpoint operations analyst**

Required privilege (in {{stack}}) or custom role privilege (in {{serverless-short}}): **Execute Operations**

Example: `runscript --ScriptName="Script2.sh" --Args="-Verbose true"`

#### SentinelOne
```yaml {applies_to}
stack: ga 9.2
serverless: ga
```
For SentinelOne, you must include the following parameter to identify the script you want to run:

* `--script`: The name of the script to run. Select from a list of saved custom scripts.

You can also use this optional parameter:

* `--inputParams`: Additional command-line arguments passed to the script to customize its execution.

Predefined role (in {{serverless-short}}): **SOC manager** or **Endpoint operations analyst**

Required privilege (in {{stack}}) or custom role privilege (in {{serverless-short}}): **Execute Operations**

Example: `runscript --script="copy.sh" --inputParams="~/logs/log.txt /tmp/log.backup.txt"`

### `cancel` [cancel]
```yaml {applies_to}
stack: ga 9.2
serverless: ga
```

::::{note}
This response action is supported only for [Microsoft Defender for Endpoint–enrolled hosts](/solutions/security/endpoint-response-actions/third-party-response-actions.md#defender-response-actions).
::::

Cancel an ongoing action on the host. This allows you to force-cancel actions that are stuck in a pending state, unblocking further use of the response console.

You must include the following parameter to identify the action to cancel:

* `--action`: The response action to cancel. Select from a list of pending actions.

Required role or privilege: `cancel` doesn't have its own required role or privilege. To use it, you must have the same role or privilege that's required for the action you're canceling. For example, canceling a `runscript` action requires the **Execute Operations** privilege.

Example: `cancel --action="copy.sh" --comment="Canceled because it is stuck"`

## Supporting commands and parameters [supporting-commands-parameters]


### `--comment` [_comment]

Add to a command to include a comment explaining or describing the action. Comments are included in the response actions history.


### `--help` [_help]

Add to a command to get help for that command.

Example: `isolate --help`


### `clear` [_clear]

Clear all output from the response console.


### `help` [_help_2]

List supported commands in the console output area.

::::{tip}
You can also get a list of commands in the [Help panel](/solutions/security/endpoint-response-actions.md#help-panel), which stays on the screen independently of the output area.
::::


## Help panel [help-panel]

Click {icon}`question` **Help** in the upper-right to open the **Help** panel, which lists available response action commands and parameters as a reference.

::::{note}
This panel displays only the response actions that you have the user role or privileges to perform.
::::


:::{image} /solutions/images/security-response-console-help-panel.png
:alt: Help panel
:width: 65%
:screenshot:
:::

You can use this panel to build commands with less typing. Click the add icon (![Add icon](/solutions/images/security-add-command-icon.png "title =20x20")) to add a command to the input area, enter any additional parameters or a comment, then press **Return** to run the command.

If the endpoint is running an older version of {{agent}}, some response actions may not be supported, as indicated by an informational icon and tooltip. [Upgrade {{agent}}](/reference/fleet/upgrade-elastic-agent.md) on the endpoint to be able to use the latest response actions.

:::{image} /solutions/images/security-response-console-unsupported-command.png
:alt: Unsupported response action with tooltip
:width: 65%
:screenshot:
:::


## Response actions history [actions-log]

Click **Response actions history** to display a log of the response actions performed on the endpoint, such as isolating a host or terminating a process. You can filter the information displayed in this view. Refer to [](/solutions/security/endpoint-response-actions/response-actions-history.md) for more details.

:::{image} /solutions/images/security-response-actions-history-console.png
:alt: Response actions history with a few past actions
:width: 85%
:screenshot:
:::
