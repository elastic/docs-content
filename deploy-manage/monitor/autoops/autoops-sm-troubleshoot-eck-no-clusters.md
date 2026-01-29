---
applies_to:
  deployment:
    eck:
navigation_title: Connected clusters not appearing with ECK
products:
  - id: cloud-kubernetes
---

# Troubleshoot connected clusters not appearing with ECK installation

If you chose ECK as your installation method in the wizard to connect your {{es}} clusters to AutoOps, but you can't view any connected clusters in your account, go through this guide to diagnose and fix common issues.

## Verify `AutoOpsAgentPolicy` status

Check if the `AutoOpsAgentPolicy` resource was successfully created and the ECK operator is processing it correctly.

:::::{stepper}

::::{step} Check if the policy was created
Run the following command.
```shell
kubectl get autoopsagentpolicy <policy_name>
```
If the policy doesn't appear, there was an issue with its creation.
::::

::::{step} Confirm the issue by checking logs
Run the following command to show logs.
```shell
kubectl logs -f -n <ECK_operator_namespace> -l control-plane=elastic-operator
```
If the log contains any errors mentioning `AutoOpsAgentPolicy` or the policy's name, this confirms that the policy's creation and processing is causing the issue. 
::::

::::{step} Re-add the YAML manifest to your configuration file
Repeat the steps to [install the agent](../autoops/cc-connect-self-managed-to-autoops.md#install-agent) with ECK as your installation method. This should resolve any issues with the policy.
::::

:::::

## Verify that {{agent}} was deployed

Check if `AutoOpsAgentPolicy` successfully deployed {{agent}} for your {{es}} clusters. 

:::::{stepper}

::::{step} List agent deployments
Run the following command.
```shell
kubectl get deployments -l autoops.k8s.elastic.co/policy-name=<policy_name>
```
If no deployments appear, there might be an issue with the `resourceSelector` label applied to your {{es}} clusters. If deployments appear but pods are not running, there might be an issue with a specific pod.
::::

::::{step} Check cluster labels and agent pods 
If no deployments appeared in the previous step, run the following command to check your cluster labels.   
```shell
kubectl get elasticsearch <policy_name> --show-labels
```
Make sure that the label you applied in the [Launch AutoOps](../autoops/cc-connect-self-managed-to-autoops.md#launch-autoops) step of the wizard appears correctly in the list.

If deployments appeared in the previous step, run the following command to check pod status.
```shell
kubectl get pods -l autoops.k8s.elastic.co/policy-name=<policy_name>
```

If the status indicates that a pod is crashing or in a pending state, run the following command to inspect its events:
```shell
kubectl describe pod <agent_pod_name>
```
::::

:::::

## Validate connection secrets

Make sure there are no errors in your secret keys.

:::::{stepper}

::::{step} Verify secret content
Run the following command.
```shell
kubectl get secret <secret_name> -o yaml
```
Make sure the secret has the following required keys:
* `autoops-token`
* `autoops-otel-url`
* `cloud-connected-mode-api-key`
::::

::::{step} Confirm secret reference
Run the following command to confirm that `AutoOpsAgentPolicy` is actually referencing the correct configuration.
```shell
kubectl get autoopsagentpolicy <policy_name> -o jsonpath='{.spec.autoOpsRef.secretName}'
```
The command should return the correct `.spec.autoOpsRef.secretName`. 
::::

:::::

## Check for authorization errors

When you go through the installation wizard, the ECK operator attempts to create an API key for {{agent}} within {{es}}. If there is an issue with this creation, authorization errors will appear in the operator logs.
:::::{stepper}

::::{step} Pull operator logs
Run the following command.
```shell
kubectl logs -f -n <ECK_operator_namespace> -l control-plane=elastic-operator
```
::::

::::{step} Inspect logs
If any errors in the logs mention "authorization" or "unauthorized connection", go through the installation wizard again so that the operator can reattempt creating a user or API key.
::::

## Ensure that {{agent}} is allowed to send data to AutoOps

:::{include} ../_snippets/autoops-allowlist-port-and-urls.md
:::

## Check cluster health

Ensure that the {{es}} clusters you are trying to connect to AutoOps are healthy. {{agent}} may fail to connect clusters in a Red state.