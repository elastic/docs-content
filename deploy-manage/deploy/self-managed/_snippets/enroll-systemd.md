1. Run the `status` command to get details about the {{kib}} service.

    ```sh
    sudo systemctl status kibana
    ```


    In the `status` command output, a URL is shown with:

    * A host address to access {{kib}}
    * A six digit verification code

    For example:

    ```sh
    Kibana has not been configured.
    Go to http://<host>:5601/?code=<code> to get started.
    ```

    Make a note of the verification code.

2. Go to the host address.

    It can take a minute or two for {{kib}} to start up, so refresh the page if you don’t see a prompt right away.

3. When {{kib}} starts, you’re prompted to provide an enrollment token. Paste in the {{kib}} enrollment token that you generated earlier.
4. Click **Configure Elastic**.
5. If you’re prompted to provide a verification code, copy and paste in the six digit code that was returned by the `status` command. Then, wait for the setup to complete.
6. When you see the **Welcome to Elastic** page, provide the `elastic` as the username and provide the password that you copied from the install command output when you set up your first {{es}} node.
7. Click **Log in**.