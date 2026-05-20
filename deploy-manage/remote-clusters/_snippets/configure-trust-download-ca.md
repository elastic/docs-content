1. Download the transport CA certificate associated with your deployment. This CA is required by the self-managed cluster to establish trust with the deployment.

    1. Open your deployment management page in the {{ecloud}} UI and go to **Security**.
    2. Under **CA certificates**, select the download icon to save the CA into a local file.

2. Obtain the CA certificate of the self-managed cluster (the CA used to sign all transport certificates of your cluster). The CA needs to be in PEM format and should not contain the private key. If you only have the CA with the key in p12 format, then you can create the necessary file with the following command:

    ```sh
    openssl pkcs12 -in elastic-stack-ca.p12 -out newfile.crt.pem -clcerts -nokeys
    ```

    :::{tip}
    The transport CA used by your self-managed cluster is part of its existing [transport TLS/SSL configuration](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#security-transport-tls-ssl-key-trusted-certificate-settings).
    :::
