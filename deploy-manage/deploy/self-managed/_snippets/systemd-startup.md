To configure {{es}} to start automatically when the system boots up, run the following commands:

```sh
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable elasticsearch.service
```