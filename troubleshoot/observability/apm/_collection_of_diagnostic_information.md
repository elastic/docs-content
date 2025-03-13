---
mapped_pages:
  - https://www.elastic.co/guide/en/apm/agent/php/current/_collection_of_diagnostic_information.html
applies_to:
  stack: all
  serverless:
    observability: all
---

# Collection of diagnostic information [_collection_of_diagnostic_information]

For a more detailed analysis of issues, it is necessary to collect diagnostic information. The agent allows for the automatic collection of such information - all data will be saved to the file specified in the configuration.

There are two possible ways to enable this feature:

1. By php.ini - To enable this feature, you need to modify the php.ini file (or 99-elastic.ini) and provide the path to the file where the data will be saved, f.ex:

    ```ini
    elastic_apm.debug_diagnostic_file=/tmp/php_diags_%p_%t.txt
    ```

2. By environment variable. You can also enable information collection using the environment variable `ELASTIC_APM_DEBUG_DIAGNOSTIC_FILE`. It must be exported or directly specified when running php process. Example of calling php-cli script:

    ```ini
    ELASTIC_APM_DEBUG_DIAGNOSTIC_FILE=/tmp/php_diags_%p_%t.txt php test.php
    ```


Remember, the provided file path must be writable by the PHP process.

If there are multiple PHP processes in your system, we allow you to specify directives in the diagnostic file name. This way, the files will remain unique and won’t be overwritten.

* `%p` - In this place, the agent will substitute the process identifier.
* `%t` - In this place, the agent will substitute the UNIX timestamp.

::::{important} 
After setting the path, remember to **fully restart the process** for which you are collecting diagnostic information. This may vary depending on the context, such as PHP, PHP-FPM, Apache, or PHP-CGI. Diagnostic information will be recorded after the first HTTP request is made or at the beginning of script execution for PHP-CLI.<br> <br> Please also be aware that the information contained in the output file may include sensitive data, such as passwords, security tokens or environment variables from your system. Make sure to review the data and mask sensitive information before sharing the file publicly.<br> <br> After collecting diagnostic information, remember to disable this feature and restore the previous configuration in php.ini or the environment variable.
::::


What information will be collected:

* Process identifier and parent process identifier
* User identifier of the worker process
* List of loaded PHP extensions
* Result from the phpinfo() function
* Process memory information and memory maps (`/proc/{{id}}/maps` and `/proc/{{id}}/smaps_rollup`)
* Process status information (`/proc/{{id}}/status`)

