`applies_to` keys accept comma-separated values to specify lifecycle states for multiple product versions. For example:

* A feature is added in 9.1 as tech preview and becomes GA in 9.4: 

    ```yml
    applies_to:
      stack: preview 9.1, ga 9.4
    ```


* A feature is deprecated in ECE 4.0 and is removed in 4.8. At the same time, it has already been removed in {{ech}}:

    ```yml
    applies_to:
      deployment:
        ece: deprecated 4.0, removed 4.8
        ess: removed
    ```