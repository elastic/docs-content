---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-manage-system-passwords.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
---

# Manage system passwords[ece-manage-system-passwords]

At the end of the {{ece}} installation process on the first host, you are provided with the URL and user credentials for the administration console users `admin` and `readonly`. You use this information to log into the Cloud UI. Both users can access all parts of the Cloud UI, but only the `admin` user can make changes. We recommend that you keep this information secure.


## Retrieve user passwords [ece-retrieve-passwords]

If you need to retrieve the system passwords at a later point, you can issue one of the following commands from the first host you installed on (requires that you have [jq](https://stedolan.github.io/jq/download/) installed).

If you specified a different host storage path during installation, change `/mnt/data/elastic` to the path your installation is using. These commands require that the secrets file exists on the host where you run the command. (Don’t have a secrets file? You can also [reset the passwords](#ece-reset-passwords).)

To retrieve the password for the `admin` user:

```sh
jq -r '.adminconsole_root_password' /mnt/data/elastic/bootstrap-state/bootstrap-secrets.json
```

To retrieve the password for the `readonly` user:

```sh
jq -r '.adminconsole_readonly_password' /mnt/data/elastic/bootstrap-state/bootstrap-secrets.json
```

You  access the Cloud UI on port 12400 or port 12443 at IP address of the first host you installed on ([https://192.168.50.10:12443](https://192.168.50.10:12443), for example).


## Reset user passwords [ece-reset-passwords]

You might need to reset the Cloud UI passwords for one of the following reasons:

* To change the passwords for the `admin` and `readonly` users after installing {{ece}} or periodically as part of your standard operating procedures.
* To reset passwords if you think they might have become compromised.

The passwords for these users are stored in `/mnt/data/elastic/bootstrap-state/bootstrap-secrets.json` along with other secrets (unless you specified a different host storage path).

To reset the password for the user `admim` on the administration console based on the secrets in `/mnt/data/elastic/bootstrap-state/bootstrap-secrets.json`:

```sh
bash elastic-cloud-enterprise.sh reset-adminconsole-password --user admin
```

To reset the password for the `admin` user if no secrets file exists:

```sh
bash elastic-cloud-enterprise.sh reset-adminconsole-password
```

For additional usage examples, check [`elastic-cloud-enterprise.sh reset-adminconsole-password` Reference](cloud://reference/cloud-enterprise/ece-installation-script-reset.md).

