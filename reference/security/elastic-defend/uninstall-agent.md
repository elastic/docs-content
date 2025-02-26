---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/uninstall-agent.html
---

# Uninstall Elastic Agent [uninstall-agent]

To uninstall {{agent}} from a host, run the `uninstall` command from the directory where it’s running. Refer to the [{{fleet}} and {{agent}} documentation](/reference/ingestion-tools/fleet/uninstall-elastic-agent.md) for more information.

If [Agent tamper protection](/reference/security/elastic-defend/agent-tamper-protection.md) is enabled on the Agent policy for the host, you’ll need to include the uninstall token in the command, using the `--uninstall-token` flag. You can [find the uninstall token](/reference/security/elastic-defend/agent-tamper-protection.md#fleet-uninstall-tokens) on the Agent policy. Alternatively, find **{{fleet}}** in the navigation menu or by using the [global search field](/get-started/the-stack.md#kibana-navigation-search), and select **Uninstall tokens**.

For example, to uninstall {{agent}} on a macOS or Linux host:

```shell
sudo elastic-agent uninstall --uninstall-token 12345678901234567890123456789012
```


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

Use these commands to uninstall {{elastic-endpoint}} from a host **ONLY** if [uninstalling an {{agent}}](/reference/ingestion-tools/fleet/uninstall-elastic-agent.md) is unsuccessful.

Windows

```shell
cd %TEMP%
copy "c:\Program Files\Elastic\Endpoint\elastic-endpoint.exe" elastic-endpoint.exe
.\elastic-endpoint.exe uninstall
del .\elastic-endpoint.exe
```

macOS

```shell
cd /tmp
cp /Library/Elastic/Endpoint/elastic-endpoint elastic-endpoint
sudo ./elastic-endpoint uninstall
rm elastic-endpoint
```

Linux

```shell
cd /tmp
cp /opt/Elastic/Endpoint/elastic-endpoint elastic-endpoint
sudo ./elastic-endpoint uninstall
rm elastic-endpoint
```
