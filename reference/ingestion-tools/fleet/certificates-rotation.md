---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/certificates-rotation.html
---

# Rotate SSL/TLS CA certificates [certificates-rotation]

In some scenarioes you may want to rotate your configured certificate authorities (CAs), for instance if your chosen CAs are due to expire. Refer to the following steps to rotate certificates between connected components:

* [Rotating a {{fleet-server}} CA](#certificates-rotation-agent-fs)
* [Rotating an {{es}} CA for connections from {{fleet-server}}](#certificates-rotation-fs-es)
* [Rotating an {{es}} CA for connections from {{agent}}](#certificates-rotation-agent-es)


## Rotating a {{fleet-server}} CA [certificates-rotation-agent-fs]

{{agent}} communicates with {{fleet-server}} to receive policies and to check for updates. There are two methods to rotate a CA certificate on {{fleet-server}} for connections from {{agent}}. The first method requires {{agent}} to re-enroll with {{fleet-server}} one or more times. The second method avoids re-enrollment and requires overwriting the existing CA file with a new certificate.

**Option 1: To renew an expiring CA certificate on {{fleet-server}} with {{agent}} re-enrollments**

Using this method, the {{agent}} with an old or expiring CA configured will be re-enrolled with {{fleet-server}} using a new CA.

1. Update the {{agent}} with the new {{fleet-server}} CA:

    The {{agent}} should already have a CA configured. Use the [`elastic-agent enroll`](/reference/ingestion-tools/fleet/agent-command-reference.md#elastic-agent-enroll-command) command to re-enroll the agent with an updated, comma separated set of CAs to use.

    ```shell
    elastic-agent enroll \
      --url=<Fleet-Server-URL> \
      --enrollment-token=<enrollment-token> \
      ... \
      --certificate-authorities <original_CA, new_CA>
    ```

    A new agent enrollment will cause a new agent to appear in {{fleet}}. This may be considered disruptive, however the old agent entry will transition to an offline state. A new agent enrollment is required in order for the {{fleet-server}} configuration to be modified to accept multiple certificate authorities.

    At this point, all TLS connections are still relying on the original CA that was provided (`original_CA`) in order to authenticate {{fleet-server}} certificates.

2. Rotate the certificates on {{fleet-server}}:

    This procedure will reissue new certificates based on the new CA. Re-enroll {{fleet-server}} with all the new certificates:

    ```shell
    elastic-agent enroll ...
      --url=<Fleet-Server-URL> \
      --enrollment-token=<enrollment-token> \
      ... \
      --fleet-server-cert <new_cert> --certificate-authorities <new_CA>
    ```

    This will cause the TLS connections to the {{agents}} to reset and will load the relevant new CA and certificates to the {{fleet-server}} configuration.

3. The {{agents}} will automatically establish new TLS connections as part of their normal operation:

    The new CA (`new_CA`) on the agent installed in Step 1 will be used to authenticate the certificates used by {{fleet-server}}.

    Note that if the original CA (`original CA`) was compromised, then it may need to be removed from the agent’s CA list. To achieve this you need to enroll the agent again:

    ```shell
    elastic-agent enroll ...
      --url=<Fleet-Server-URL> \
      --enrollment-token=<enrollment-token> \
      ... \
      --certificate-authorities <new_CA>
    ```


**Option 2: To renew an expiring CA certificate on {{es}} without {{agent}} re-enrollments**

Option 1 results in multiple {{agent}} enrollments. Another option to avoid multiple enrollments is to overwrite the CA files with the new CA or certificate. This method uses a single file with multiple CAs that can be replaced.

To use this option it is assumed that:

* {{agent}}s have already been enrolled using a file that contains the Certificate Authority:

    ```shell
    elastic-agent enroll ...
      --url=<Fleet-Server-URL> \
      --enrollment-token=<enrollment-token> \
      ... \
      --certificate-authorities=<CA.pem>
    ```

* The {{agent}} running {{fleet-server}} has already been enrolled with the following secure connection options, where each option points to files that contain the certificates and keys:

    ```shell
    elastic-agent enroll ...
      --url=<Fleet-Server-URL> \
      --enrollment-token=<enrollment-token> \
      ... \
      --certificate-authorities=<CA.pem> \
      --fleet-server-cert=<fleet-cert.pem> \
      --fleet-server-cert-key=<key.pem>
    ```


To update the {{agent}} and {{fleet-server}} configurations:

1. Update the configuration with the new CA by changing the content of `CA.pem` to include the new CA.

    ```shell
    cat new_ca.pem >> CA.pem
    ```

2. Restart the {{agents}}. Note that this is not a re-enrollment. Restarting will force the {{agents}} to reload the CAs.

    ```shell
    elastic-agent restart
    ```

3. For the {{agent}} that is running {{fleet-server}}, overwrite the original `certificate`, `certificate-key`, and the `certificate-authority` with the new ones to use.

    ```shell
    cat new-cert.pem > cert.pem
    cat new-key.pem > key.pem
    cat new_ca.pem > CA.pem
    ```

4. Restart the {{agent}} that is running {{fleet-server}}.

    ```shell
    elastic-agent restart
    ```

5. If the original certificate needs to be removed from the {{agents}}, overwrite the `CA.pem` with the new CA only:

    ```shell
    cat new_ca.pem > CA.pem
    ```

6. Finally, restart the {{agents}} again.

    ```shell
    elastic-agent restart
    ```



## Rotating an {{es}} CA for connections from {{fleet-server}} [certificates-rotation-fs-es]

{{fleet-server}} communicates with {{es}} to send status information to {{fleet}} about {{agent}}s and to retrieve updated policies to ship out to all {{agent}}s enrolled in a given policy. If you have {{fleet-server}}  [deployed on-premise](/reference/ingestion-tools/fleet/deployment-models.md), you may wish to rotate your configured CA certificate, for instance if the certificate is due to expire.

To rotate a CA certificate on {{es}} for connections from {{fleet-server}}:

1. Update the {{fleet-server}} with the new {{fleet-server}} CA:

    The {{agent}} running {{fleet-server}} should already have a CA configured. Use the [`elastic-agent enroll`](/reference/ingestion-tools/fleet/agent-command-reference.md#elastic-agent-enroll-command) command to re-enroll the agent running {{fleet-server}} with an updated, comma separated set of CAs to use.

    ```shell
    elastic-agent enroll \
      --fleet-server-es=<Elasticsearch-URL> \
      --fleet-server-service-token=<service-token> \
      ... \
      --fleet-server-es-ca <original_ES_CA, new_ES_CA>
    ```

    A new agent enrollment will cause two {{fleet-server}} agents to appear in {{fleet}}. This may be considered disruptive, however the old agent entry will transition to offline. A new agent enrollment is required in order for the {{fleet-server}} configuration to be modified to accept multiple certificate authorities.

    At this point, all TLS connections are still relying on the original CA that was provided (`original_ES_CA`) in order to authenticate {{es}} certificates. Re-enrolling the {{fleet-server}} will cause the agents going through that {{fleet-server}} to also reset their TLS, but the connections will be re-established as required.

2. Rotate the certificates on {{es}}.

    {{es}} will use new certificates based on the new {{es}} CA. Since the {{fleet-server}} has the original and the new {{es}} CAs in a chain, it will accept original and new certificates from {{es}}.

    Note that if the original {{es}} CA (`original_ES CA`) was compromised, then it may need to be removed from the {{fleet-server}}'s CA list. To achieve this you need to enroll the {{fleet-server}} agent again (if re-enrollment is a concern then use a file to hold the certificates and certificate-authority):

    ```shell
    elastic-agent enroll \
      --fleet-server-es=<Elasticsearch-URL> \
      --fleet-server-service-token=<service-token> \
      ... \
      --fleet-server-es-ca <new_ES_CA>
    ```



## Rotating an {{es}} CA for connections from {{agent}} [certificates-rotation-agent-es]

Using configuration information from a policy delivered by {{fleet-server}}, {{agent}} collects data and sends it to {{es}}.

To rotate a CA certificate on {{es}} for connections from {{agent}}:

1. In {{fleet}} open the **Settings** tab.
2. In the **Outputs** section, click the edit button for the {{es}} output that requires a certificate rotation.
3. In the **Elasticsearch CA trusted fingerprint** field, add the new trusted fingerprint to use. This is the SHA-256 fingerprint (hash) of the certificate authority used to self-sign {{es}} certificates. This fingerprint will be used to verify self-signed certificates presented by {{es}}.

    If this certificate is present in the chain during the handshake, it will be added to the `certificate_authorities` list and the handshake will continue normally.

    :::{image} images/certificate-rotation-agent-es.png
    :alt: Screen capture of the Edit Output UI: Elasticsearch CA trusted fingerprint
    :class: screenshot
    :::
