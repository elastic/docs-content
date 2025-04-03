The default host and port settings configure Kibana to run on localhost:5601. To change this behavior and allow remote users to connect, you need to set up {{kib}} to run on a routable, external IP address. You can do this by editing the settings in [`kibana.yml`](/deploy-manage/deploy/self-managed/configure-kibana.md): 

1.  Retrieve the external IP address of your host. You’ll need this value later.
2.  Open `kibana.yml` in a text editor.
 
3.  Uncomment the line `#server.host: localhost` and replace the default address with the value that you retrieved in step one. For example:

    ```yaml
    server.host: 10.128.0.28
    ```

4.  Save your changes and close the editor.
