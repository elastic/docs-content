---
applies_to:
  deployment:
    self:
navigation_title: Connect your local development cluster
products:
  - id: cloud-kubernetes
  - id: cloud-enterprise
---

# Connect your local development cluster to AutoOps

If you have an {{es}} cluster set up for local development or testing, you can connect it to AutoOps using Docker.

## Prerequisites

Ensure your system meets the following requirements before proceeding:

* You have set up [{{es}} for local development](/deploy-manage/deploy/self-managed/local-development-installation-quickstart.md).
* You have installed [Docker Desktop](https://www.docker.com/products/docker-desktop).
* You have an {{ecloud}} account with the [Organization owner role](/deploy-manage/monitor/autoops/cc-manage-users.md#assign-roles).

## Connect your local development cluster to AutoOps

Complete the following steps to connect your local development cluster to AutoOps.

1. Run the following command in your terminal to open the `/etc/hosts` file in a text editor with administrator privileges:

  ```sh
  vim /etc/hosts
  ```
2. On a new line in the `/etc/hosts` file, add an entry to map the {{es}} cluster URL to the IP address representing the local development cluster.

    The entry should be formatted as `127.0.0.1 {{hostname}}`.
3. Save the changes.
4. In your terminal, run the following command to reload the hostname service:
    * For Linux: 
    ```sh
    /bin/systemctl restart systemd-hostnamed
    ```
    * For macOS: 
    ```sh
    sudo dscacheutil -flushcache
    ```
5. Follow the instructions to [Connect to AutoOps](/deploy-manage/monitor/autoops/cc-connect-self-managed-to-autoops.md#connect-to-autoops) with the following differences:
    * In the [Select installation method](/deploy-manage/monitor/autoops/cc-connect-self-managed-to-autoops.md#select-installation-method) step, select **Docker**.
    * In the [Configure agent](/deploy-manage/monitor/autoops/cc-connect-self-managed-to-autoops.md#configure-agent) step, when prompted to enter your **{{es}} endpoint URL**, enter the name of your local development cluster or enter the following:
        ```sh
        http://localhost:9200
        ```
    * In the [Install agent](/deploy-manage/monitor/autoops/cc-connect-self-managed-to-autoops.md#install-agent) step, paste the command into the text editor and replace `docker run -d \` with:
        ```sh
        docker run -d --network host \
        ```
        
        This replacement is also required if your cluster is running on macOS.
      
After completing all the steps, you can [Access AutoOps](/deploy-manage/monitor/autoops/cc-connect-self-managed-to-autoops.md#access-autoops).




