* When a change is released in `ga`, users need to know which version the feature became available in:

    ```
    ---
    applies_to:
      stack: ga 9.3
    ---
    ```

* When a change is introduced as preview or beta, use `preview` or `beta` as value for the corresponding key within the `applies_to`:

    ```
    ---
    applies_to:
      stack: beta 9.1
    ---
    ```

* When a change introduces a deprecation, use `deprecated` as value for the corresponding key within the `applies_to`:

    ```
    ---
    applies_to:
      deployment:
        ece: deprecated 4.2
    ---
    ```

* When a change removes a feature, any user reading the page that may be using a version of Kibana prior to the removal must be aware that the feature is still available to them. For that reason, we do not remove the content, and instead mark the feature as removed:

    ```
    ---
    applies_to:
      stack: deprecated 9.1, removed 9.4
    ---
    ```