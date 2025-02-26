---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/secret-files-guide.html
---

# Secret files guide [secret-files-guide]

This guide provides step-by-step examples with best practices on how to deploy secret files directly on a host or through the Kubernetes secrets engine.

## Secrets on filesystem [secret-filesystem]

Secret files can be provisioned as plain text files directly on filesystems and referenced or passed through {{agent}}.

We recommend these steps to improve security.

### File permissions [_file_permissions]

File permissions should not allow for global read permissions.

On MacOS and Linux, you can set file ownership and file permissions with the `chown` and `chmod` commands, respectively. {{fleet-server}} runs as the `root` user on MacOS and Linux, so given a file named `mySecret`, you can alter it with:

```sh
sudo chown root:root mySecret # set the user:group to root
sudo chmod 0600 mySecret      # set only the read/write permission flags for the user, clear group and global permissions.
```

On Windows, you can use `icacls` to alter the ACL list associated with the file:

```powershell
Write-Output -NoNewline SECRET > mySecret          # Create the file mySecret with the contents SECRET
icacls .\mySecret /inheritance:d                   # Remove inherited permissions from file
icacls .\mySecret /remove:g BUILTIN\Administrators # Remove Administrators group permissions
icacls .\mySecret /remove:g $env:UserName          # Remove current user's permissions
```


### Temporary filesystem [_temporary_filesystem]

You can use a temporary filesystem (in RAM) to hold secret files in order to improve security. These types of filesystems are normally not included in backups and are cleared if the host is reset. If used, the filesystem and secret files need to be reprovisioned with every reset.

On Linux you can use `mount` with the `tmpfs` filesystem to create a temporary filesystem in RAM:

```sh
mount -o size=1G -t tmpfs none /mnt/fleet-server-secrets
```

On MacOS you can use a combination of `diskutil` and `hdiutil` to create a RAM disk:

```sh
diskutil erasevolume HFS+ 'RAM Disk' `hdiutil attach -nobrowse -nomount ram://2097152`
```

Windows systems do not offer built-in options to create a RAM disk, but several third party programs are available.


### Example [_example]

Here is a step by step guide for provisioning a service token on a Linux system:

```sh
sudo mkdir -p /mnt/fleet-server-secrets
sudo mount -o size=1G -t tmpfs none /mnt/fleet-server-secrets
echo -n MY-SERVICE-TOKEN > /mnt/fleet-server-secrets/service-token
sudo chown root:root /mnt/fleet-server-secrets/service-token
sudo chmod 0600 /mnt/fleet-server-secrets/service-token
```

::::{note}
The `-n` flag is used with `echo` to prevent a newline character from being appended at the end of the secret. Be sure that the secret file does not contain the trailing newline character.
::::




## Secrets in containers [_secrets_in_containers]

When you are using secret files directly in containers without using Kubernetes or another secrets management solution, you can pass the files into containers by mounting the file or directory. Provision the file in the same manner as it is in [Secrets on filesystem](#secret-filesystem) and mount it in read-only mode. For example, when using Docker.

If you are using {{agent}} image:

```sh
docker run \
	-v /path/to/creds:/creds:ro \
        -e FLEET_SERVER_CERT_KEY_PASSPHRASE=/creds/passphrase \
        -e FLEET_SERVER_SERVICE_TOKEN_PATH=/creds/service-token \
        --rm docker.elastic.co/elastic-agent/elastic-agent
```


## Secrets in Kubernetes [_secrets_in_kubernetes]

Kubernetes has a [secrets management engine](https://kubernetes.io/docs/concepts/configuration/secret/) that can be used to provision secret files to pods.

For example, you can create the passphrase secret with:

```sh
kubectl create secret generic fleet-server-key-passphrase \
  --from-literal=value=PASSPHRASE
```

And create the service token secret with:

```sh
kubectl create secret generic fleet-server-service-token \
  --from-literal=value=SERVICE-TOKEN
```

Then include it in the pod specification, for example, when you are running {{fleet-server}} under {{agent}}:

```yaml
spec:
  volumes:
  - name: key-passphrase
    secret:
      secretName: fleet-server-key-passphrase
  - name: service-token
    secret:
      secretName: fleet-server-service-token
  containers:
  - name: fleet-server
    image: docker.elastic.co/elastic-agent/elastic-agent
    volumeMounts:
    - name: key-passphrase
      mountPath: /var/secrets/passphrase
    - name: service-token
      mountPath: /var/secrets/service-token
    env:
    - name: FLEET_SERVER_CERT_KEY_PASSPHRASE
      value: /var/secrets/passphrase/value
    - name: FLEET_SERVER_SERVICE_TOKEN_PATH
      value: /var/secrets/service-token/value
```

### {{agent}} Kubernetes secrets provider [_agent_kubernetes_secrets_provider]

When you are running {{fleet-server}} under {{agent}} in {{k8s}}, you can use {{agent}}'s [Kubernetes Secrets Provider](/reference/ingestion-tools/fleet/kubernetes_secrets-provider.md) to insert a {{k8s}} secret directly into {{fleet-server}}'s configuration. Note that due to how {{fleet-server}} is bootstrapped only the APM secrets (API key or secret token) can be specified with this provider.



