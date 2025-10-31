Unversioned products don't follow a fixed versioning scheme and are released a lot more often than versioned products. All users are using the same version of this product.

* When a change is released in `ga`, it **doesn’t need any specific tagging**.
* When a change is introduced as preview or beta, use `preview` or `beta` as value for the corresponding key within the `applies_to`:

    ```
    ---
    applies_to:
      serverless: preview
    ---
    ```
* When a change introduces a deprecation, use deprecated as value for the corresponding key within the `applies_to`:

    ```
    ---
    applies_to:
      deployment:
        ess: deprecated
    ---
    ```

* When a change removes a feature, **remove the content**. 
  
    **Exception:** If the content also applies to another context (for example a feature is removed in both Kibana 9.x and Serverless), then it must be kept for any user reading the page that may be using a version of Kibana prior to the removal. 
    
    For example:

    ```
    ---
    applies_to:
      stack: deprecated 9.1, removed 9.4
      serverless: removed
    ---
    ```