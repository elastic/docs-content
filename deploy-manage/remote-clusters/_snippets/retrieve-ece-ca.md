Before configuring the local deployment, retrieve the CA certificate of the remote ECE proxy. To find this certificate:

1. In the remote ECE environment, go to **Platform > Settings > TLS certificates**.
2. Select **Show certificate chain** under **Proxy**.
3. Click **Copy root certificate** and paste it into a new file. The root certificate is the last certificate shown in the chain.

    :::{image} /deploy-manage/images/cloud-remote-clusters-proxy-certificate.png
    :alt: Certificate to copy from the chain
    :::

4. Save the file as `.crt`.

You can now proceed to configure the local deployment. The CA file you saved will be used in one of the following steps.

