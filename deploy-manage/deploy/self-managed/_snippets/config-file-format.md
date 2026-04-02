The `elasticsearch.yml` configuration format is [YAML](https://yaml.org/). Here is an example of changing the path of the data and logs directories in {{es}}:

```yaml
path:
    data: /var/lib/elasticsearch
    logs: /var/log/elasticsearch
```

Settings can also be flattened as follows:

```yaml
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch
```

In YAML, you can format non-scalar values as sequences:

```yaml
discovery.seed_hosts:
   - 192.168.1.10:9300
   - 192.168.1.11
   - seeds.mydomain.com
```

Though less common, you can also format non-scalar values as arrays:

```yaml
discovery.seed_hosts: ["192.168.1.10:9300", "192.168.1.11", "seeds.mydomain.com"]
```