{{es}} can be started and stopped as follows:

```sh
sudo systemctl start elasticsearch.service
sudo systemctl stop elasticsearch.service
```

These commands provide no feedback as to whether {{es}} was started successfully or not. Instead, this information will be written in the log files located in `/var/log/elasticsearch/`.

If you have password-protected your {{es}} keystore, you will need to provide `systemd` with the keystore password using a local file and systemd environment variables. This local file should be protected while it exists and may be safely deleted once {{es}} is up and running.

```sh
echo "keystore_password" > /path/to/my_pwd_file.tmp
chmod 600 /path/to/my_pwd_file.tmp
sudo systemctl set-environment ES_KEYSTORE_PASSPHRASE_FILE=/path/to/my_pwd_file.tmp
sudo systemctl start elasticsearch.service
```