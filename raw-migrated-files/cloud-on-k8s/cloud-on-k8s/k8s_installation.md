# Installation [k8s_installation]

## FIPS compliant installation using Helm [k8s_fips_compliant_installation_using_helm]

Set `image.fips=true` to install a FIPS-enabled version of the ECK Operator. Refer to [Install ECK using the Helm chart](../../../deploy-manage/deploy/cloud-on-k8s/install-using-helm-chart.md) for full Helm installation instructions.

```sh
helm install elastic-operator elastic/eck-operator \
  -n elastic-system --create-namespace \
  --set=image.fips=true
```


## FIPS compliant installation using manifests [k8s_fips_compliant_installation_using_manifests]

The `StatefulSet` definition within the yaml installation manifest will need to be patched prior to installation to append `-fips` to the `spec.template.spec.containers[*].image` to install a FIPS-enabled version of the ECK Operator. Refer to [Install ECK using the YAML manifests](../../../deploy-manage/deploy/cloud-on-k8s/install-using-yaml-manifest-quickstart.md) for full manifest installation instructions.

::::{note} 
`${ECK_VERSION}` in the following command needs to be replaced with the version of the Operator that is to be installed.
::::


```sh
curl -s https://download.elastic.co/downloads/eck/${ECK_VERSION}/operator.yaml | sed -r 's#(image:.*eck-operator)(:.*)#\1-fips\2#' | kubectl apply -f -
```

If the Operator has already been installed using the manifests, the installation can be patched instead:

```sh
kubectl patch sts elastic-operator -n elastic-system -p '{"spec":{"template":{"spec":{"containers":[{"name":"manager", "image":"docker.elastic.co/eck/eck-operator-fips:${ECK_VERSION}"}]}}}}'
```


