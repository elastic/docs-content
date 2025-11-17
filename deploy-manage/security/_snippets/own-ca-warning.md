:::{warning}
Transport connections between {{es}} nodes are security-critical and you must protect them carefully. Malicious actors who can observe or interfere with node-to-node transport traffic can read or modify cluster data. A malicious actor who can establish a transport connection might be able to invoke system-internal APIs, including APIs that read or modify cluster data.

If you choose to issue node transport certificates using an external CA, then carefully review [](/deploy-manage/security/external-ca-transport.md) to ensure that the certificates that you provide meet the security requirements for transport connections.
:::