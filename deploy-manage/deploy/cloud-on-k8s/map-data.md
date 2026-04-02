---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-maps-data.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Map data [k8s-maps-data]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


The Elastic Maps Server Docker image contains only a few zoom levels of data. To get the map data up to the highest zoom level, Elastic Maps Server needs a basemap file mounted into its container.

## Basemap download [k8s-maps-basemap-download]

You have to download the basemap ahead of time on a machine that is not air-gapped and populate a volume that can be mounted into the Elastic Maps Server Pods. Check also the [Elastic Maps Server documentation.](/explore-analyze/visualize/maps/maps-connect-to-ems.md#elastic-maps-server)

The procedure on how to get a Kubernetes volume populated with that data is outside the scope of this document, as it depends on your specific Kubernetes setup and choice of volume provisioner. This is a possible approach that works for most setups:

1. Download the basemap zip archive using the link shown in the Elastic Maps Server UI or extracted from the `/status` endpoint.
2. Create a PersistentVolumeClaim of sufficient size (> 90G for the maximal resolution) and a temporary Pod to mount the corresponding volume.

    ```yaml
    ---
    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: ems-basemap
    spec:
      storageClassName: "standard"
      accessModes:
        - ReadWriteOnce
      resources:
        requests:
          storage: 250G
    ---
    kind: Pod
    apiVersion: v1
    metadata:
      name: ems-data-setup
    spec:
      terminationGracePeriodSeconds: 0
      volumes:
        - name: ems-storage
          persistentVolumeClaim:
           claimName: ems-basemap
      containers:
        - name: ems-setup
          image: ubuntu
          command: [bash, -c, "apt-get update && apt-get install unzip && while true; do sleep 10; done"]
          volumeMounts:
            - mountPath: "/usr/share/planet"
              name: ems-storage
    ```

3. Use `kubectl` to copy the basemap data into the volume

    ```sh
    kubectl cp planet.zip ems-data-setup:/usr/share/planet/planet.zip
    ```

4. Unzip the archive on the temporary Pod

    ```sh
    kubectl exec ems-data-setup -- unzip /usr/share/data/planet.zip -d /usr/share/planet
    ```

5. Delete the temporary Pod and remount the volume into the Elastic Maps Server Pods as described in [Pod configuration](#k8s-maps-pod-configuration).

    ```sh
    kubectl delete pod ems-data-setup
    ```



## Pod configuration [k8s-maps-pod-configuration]

You can [customize the Elastic Maps Server Pod](customize-pods.md) using a Pod template.

The following example demonstrates how to create a Elastic Maps Server deployment which mounts a data volume with the complete basemap.

```yaml subs=true
apiVersion: maps.k8s.elastic.co/v1alpha1
kind: ElasticMapsServer
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  count: 1
  podTemplate:
    spec:
      containers:
      - name: maps
        volumeMounts:
        - name: map-data
          readOnly: true
          mountPath: /usr/src/app/data
      volumes:
        - name: map-data
          persistentVolumeClaim:
            claimName: ems-basemap
```

The name of the container in the Pod template must be `maps`.


