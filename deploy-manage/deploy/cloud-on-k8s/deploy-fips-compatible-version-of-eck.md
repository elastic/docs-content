---
navigation_title: FIPS compatibility
applies_to:
  deployment:
    eck: all
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-fips.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s_installation.html
---

# Deploy a FIPS compatible version of ECK [k8s-fips]

The Federal Information Processing Standard (FIPS) Publication 140-2, (FIPS PUB 140-2), titled "Security Requirements for Cryptographic Modules" is a U.S. government computer security standard used to approve cryptographic modules. Since version 2.6 ECK offers a FIPS-enabled image that is a drop-in replacement for the standard image.

For the ECK operator, adherence to FIPS 140-2 is ensured by:

* Using FIPS approved / NIST recommended cryptographic algorithms.
* Compiling the operator using the [BoringCrypto](https://github.com/golang/go/blob/dev.boringcrypto/README.boringcrypto.md) library for various cryptographic primitives.

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

