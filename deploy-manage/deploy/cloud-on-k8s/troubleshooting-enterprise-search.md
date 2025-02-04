---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-enterprise-search-troubleshoot.html
---

# Troubleshooting [k8s-enterprise-search-troubleshoot]

## Capture a JVM heap dump [k8s-enterprise-search-jvm-heap-dump]

For advanced troubleshooting you might need to capture a JVM heap dump. By default, the Enterprise Search Docker image is not configured to run with a data volume by the ECK operator. However, you can write a heap dump to the `tmp` directory that Enterprise Search uses. Note that your heap dump will be lost if you do not extract it before the container restarts.

```sh
kubectl exec $POD_NAME -- bash -c \
  'jmap -dump:format=b,file=tmp/heap.hprof $(jps| grep Main | cut -f 1 -d " ")'

# The Enterprise Search Docker images don't have tar installed so we cannot use kubectl cp
kubectl exec $POD_NAME -- cat /usr/share/enterprise-search/tmp/heap.hprof | gzip -c > heap.hprof.gz

# Remove the heap dump from the running container to free up space
kubectl exec $POD_NAME -- rm /usr/share/enterprise-search/tmp/heap.hprof
```


