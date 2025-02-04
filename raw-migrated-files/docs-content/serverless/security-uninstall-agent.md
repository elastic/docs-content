# Uninstall {{agent}} [security-uninstall-agent]

To uninstall {{agent}} from a host, run the `uninstall` command from the directory where it’s running. Refer to the [{{fleet}} and {{agent}} documentation](https://www.elastic.co/guide/en/fleet/current/uninstall-elastic-agent.html) for more information.

If [Agent tamper protection](../../../solutions/security/configure-elastic-defend/prevent-elastic-agent-uninstallation.md) is enabled on the Agent policy for the host, you’ll need to include the uninstall token in the command, using the `--uninstall-token` flag. You can [find the uninstall token](../../../solutions/security/configure-elastic-defend/prevent-elastic-agent-uninstallation.md#fleet-uninstall-tokens) on the Agent policy or at **{{fleet}}** → **Uninstall tokens**.

For example:

:::::::{tab-set}

::::::{tab-item} macOS
```shell
sudo elastic-agent uninstall --uninstall-token 12345678901234567890123456789012
```
::::::

::::::{tab-item} Linux
```shell
sudo elastic-agent uninstall --uninstall-token 12345678901234567890123456789012
```
::::::

::::::{tab-item} Windows
```shell
C:\"Program Files"\Elastic\Agent\elastic-agent.exe uninstall --uninstall-token 12345678901234567890123456789012
```
::::::

:::::::

## Provide multiple uninstall tokens [multiple-uninstall-tokens]

If you have multiple tamper-protected {{agent}} policies, you may want to provide multiple uninstall tokens in a single command. There are two ways to do this:

* The `--uninstall-token` command can receive multiple uninstall tokens separated by a comma, without spaces.

    ```shell
    sudo elastic-agent uninstall -f --uninstall-token 7b3d364db8e0deb1cda696ae85e42644,a7336b71e243e7c92d9504b04a774266
    ```

* `--uninstall-token`'s argument can also be a path to a text file with one uninstall token per line.

    ::::{note}
    You must use the full file path, otherwise the file may not be found.
    ::::


    ```shell
    sudo elastic-agent uninstall -f --uninstall-token /tmp/tokens.txt
    ```

    In this example, `tokens.txt` would contain:

    ```txt
    7b3d364db8e0deb1cda696ae85e42644
    a7336b71e243e7c92d9504b04a774266
    ```



## Uninstall {{elastic-endpoint}} [uninstall-endpoint]

Use these commands to uninstall {{elastic-endpoint}} from a host **ONLY** if [uninstalling an {{agent}}](https://www.elastic.co/guide/en/fleet/current/uninstall-elastic-agent.html) is unsuccessful.

:::::::{tab-set}

::::::{tab-item} macOS
```shell
cd /tmp
cp /Library/Elastic/Endpoint/elastic-endpoint elastic-endpoint
sudo ./elastic-endpoint uninstall
rm elastic-endpoint
```
::::::

::::::{tab-item} Linux
```shell
cd /tmp
cp /opt/Elastic/Endpoint/elastic-endpoint elastic-endpoint
sudo ./elastic-endpoint uninstall
rm elastic-endpoint
```
::::::

::::::{tab-item} Windows
```shell
cd %TEMP%
copy "c:\Program Files\Elastic\Endpoint\elastic-endpoint.exe" elastic-endpoint.exe
.\elastic-endpoint.exe uninstall
del .\elastic-endpoint.exe
```
::::::

:::::::
