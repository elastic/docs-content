---
navigation_title: Sandbox limitations
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Troubleshoot sandbox limitations in Painless

Follow these guidelines to avoid Painless sandbox restriction errors in your script.

## Painless sandbox restrictions causing compilation errors

Painless implements sandbox limitations that differ from standard Java syntax and behavior. These restrictions are designed to optimize performance and prevent logical errors, which can lead to unexpected compilation errors when developers use common Java patterns. One limitation is that empty foreach loops are not allowed.

### Sample error

```json
{
  "error": {
    "root_cause": [
      {
        "type": "script_exception",
        "reason": "compile error",
        "script_stack": [
          """... keyboard": 85];

        for (item in products.ent ...""",
          "                             ^---- HERE"
        ],
        "script": """
        Map products = ["laptop": 1200, "mouse": 25, "keyboard": 85];

        for (item in products.entrySet())
        {

            
        }

        return false;
    """,
        "lang": "painless",
        "position": {
          "offset": 80,
          "start": 55,
          "end": 105
        }
      }
    ],
    "type": "script_exception",
    "reason": "compile error",
    "script_stack": [
      """... keyboard": 85];

        for (item in products.ent ...""",
      "                             ^---- HERE"
    ],
    "script": """
        Map products = ["laptop": 1200, "mouse": 25, "keyboard": 85];

        for (item in products.entrySet())
        {

            
        }

        return false;
    """,
    "lang": "painless",
    "position": {
      "offset": 80,
      "start": 55,
      "end": 105
    },
    "caused_by": {
      "type": "illegal_argument_exception",
      "reason": "extraneous foreach loop"
    }
  },
  "status": 400
}
```

### Problematic code

```json
{
    "script": {
      "lang": "painless",
      "source": """
        Map products = ["laptop": 1200, "mouse": 25, "keyboard": 85];

       for (item in products.entrySet())
       {

            
        }

        return false;
      """
    }
}
```

### Root cause

* **Empty loop blocks:** Painless does not allow empty foreach loops as an intentional feature to enhance usability and performance.  
* **Performance optimization:** Since scripts run once per document and there may be millions of documents, empty loops are considered wasteful.


The error occurs because Painless expects meaningful code inside loop blocks and treats empty loops as potential bugs or risks.

### Solution: Add code inside loop blocks

Always include actual code inside foreach loops. For example:

```json
POST _scripts/painless/_execute
{
  "script": {
    "lang": "painless",
    "source": """
      Map products = ["laptop": 1200, "mouse": 25, "keyboard": 85];
      String inventory = "";

      for (item in products.entrySet())
      {
        inventory += item.getKey() + " costs $" + item.getValue() + ". ";
      }

      return inventory;
    """
  }
}
```

### Notes

* **Empty loops:** Painless intentionally prohibits empty foreach loops for performance reasons.  
* **Syntax differences:** Painless syntax differs from Java in several ways to optimize execution and prevent logical errors.


