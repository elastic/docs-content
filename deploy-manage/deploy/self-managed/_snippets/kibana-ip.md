The default host and port settings configure Kibana to run on localhost:5601. To change this behavior and allow remote users to connect, you need to set up {{kib}} to run on a routable, external IP address. You can do this by editing the settings in [`kibana.yml`](/deploy-manage/deploy/self-managed/configure-kibana.md): 

1.  Open `kibana.yml` in a text editor.
 
2.  Uncomment the line `#server.host: localhost` and replace the default address with `0.0.0.0`. The `0.0.0.0` setting enables {{kib}} to listen for connections on all available network interfaces. In a production environment, you might want to [use a different value](kibana://reference/configuration-reference/general-settings.md#server-host), such as a static IP address.

    ```yaml
    server.host: 0.0.0.0
    ```

3.  Save your changes and close the editor.
