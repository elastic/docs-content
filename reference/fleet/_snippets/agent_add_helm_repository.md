Before installing, add the Elastic Helm repository to your local Helm configuration and verify the available versions of the `elastic-agent` chart. If the repository is already configured, run `helm repo update` to ensure you have the latest package information.

1. Set up Helm repository:

    ```sh
    helm repo add elastic https://helm.elastic.co/
    helm repo update
    ```

2. Verify chart versions:

    ```sh
    helm search repo elastic-agent --versions
    ```

    The previous command returns something similar to:

    ```sh
    NAME                 	CHART VERSION	APP VERSION	DESCRIPTION
    elastic/elastic-agent	9.0.0        	9.0.0      	Elastic-Agent Helm Chart
    elastic/elastic-agent	8.18.0       	8.18.0     	Elastic-Agent Helm Chart
    ```
