Reissuing the transport certificates for your self-managed nodes is recommended in the following cases:

- Your current certificates do not include the required X.509 SAN entry of type `otherName`, which is needed for {{ecloud}} trust restrictions to work correctly.
- You want your node certificates to follow the same subject name pattern used in {{ecloud}}, which simplifies trust management by allowing you to select clusters instead of listing individual node names.

You can use the [{{es}} `certutil` tool](elasticsearch://reference/elasticsearch/command-line-tools/certutil.md) to generate new certificates that meet both requirements:

1. Create a file called `instances.yaml` describing all the nodes in your self-managed cluster. The `dns` and `ip` fields are optional, but the `cn` field is required. When provided through this file, `certutil` automatically adds the corresponding `otherName` SAN entry used by {{es}} for trust restrictions:

    ```yaml
    instances:
      - name: "node1"
        dns: ["<NODE1_FQDN>"]
        ip: ["192.0.2.1"]
        cn: ["node1.node.1234567abcd.cluster.myscope.account"]
      - name: "node2"
        dns: ["<NODE2_FQDN>"]
        ip: ["192.0.2.2"]
        cn: ["node2.node.1234567abcd.cluster.myscope.account"]
    ```

    The value specified under cn should follow the {{ecloud}} naming pattern:

    ```
    <node_id>.node.<cluster_id>.cluster.<scope_id>.account
    ```

2. Generate the new nodes certificates, using your existing self-managed transport CA:

    ```sh
    ./bin/elasticsearch-certutil cert --ca elastic-stack-ca.p12 -in instances.yaml
    ```

    This command generates a certificate and private key for each node listed in `instances.yaml`.

3. Distribute the certificates to each node:

    Copy the generated certificate and key files to their corresponding nodes and update your {{es}} TLS configuration to use them. Then restart each node to apply the changes.

After the new certificates are in place with the desired naming pattern, you can [configure trust on your {{ecloud}} deployment](#configure-trust-deployment) to align with the updated names.