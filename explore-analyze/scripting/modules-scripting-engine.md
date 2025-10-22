---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-engine.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Implementing custom scripting language in Elasticsearch [modules-scripting-engine]

A `ScriptEngine` is a backend for implementing a scripting language in {{es}}.

## How it works

Custom script engines integrate with {{es}} scripting framework through the `ScriptEngine` interface. To register the `ScriptEngine`, your plugin should implement the `ScriptPlugin` interface and override the `getScriptEngine(Settings settings)` method during plugin initialization. 

## When to implement

Consider implementing a custom script engine when you need to use advanced internals of scripting, such as scripts that require term frequencies while scoring, or when implementing specialized scripting languages with custom syntax beyond standard Painless capabilities.

## Example implementation

The plugin [documentation](elasticsearch://extend/index.md) has more information on how to write a plugin so {{es}} will properly load it. For the complete ScriptEngine interface reference, refer to the [official implementation](https://github.com/elastic/elasticsearch/blob/main/server/src/main/java/org/elasticsearch/script/ScriptEngine.java).

### What this script does

This code creates a custom script engine that allows you to use `expert_scripts` as the language name and `pure_df` as the script source in your {{es}} queries. The script calculates document scores using term frequency data instead of {{es}} standard scoring algorithm.

The following example shows the essential parts of implementing a custom `ScriptEngine`: 

```java
private static class MyExpertScriptEngine implements ScriptEngine {
    
    // 1. Define your custom language name
    @Override
    public String getType() {
        return "expert_scripts";  // This becomes your "lang" value
    }

    // 2. Define your script source and compilation
    @Override
    public <T> T compile(String scriptName, String scriptSource, 
                         ScriptContext<T> context, Map<String, String> params) {
        // This recognizes "pure_df" as your script source
        if ("pure_df".equals(scriptSource)) {
            ScoreScript.Factory factory = new PureDfFactory();
            return context.factoryClazz.cast(factory);
        }
        throw new IllegalArgumentException("Unknown script: " + scriptSource);
    }
    
    // ... (additional required methods)
}

// 3. Where the actual score calculation happens
private static class ScoreScriptImpl extends ScoreScript {
    @Override
    public double execute(ExplanationHolder explanation) {
        // This is where you define your custom scoring logic
        // In this example: return term frequency as the score
        try {
            return postings.freq();  // Custom score calculation
        } catch (IOException e) {
            return 0.0d;
        }
    }
}

```

### Key points

* **Language Definition**: The `getType()` method returns `expert_scripts`, which becomes the value you use for the `lang` parameter in your scripts.  
* **Script Recognition:** The `compile()` method identifies `pure_df` as a valid script source, which becomes the value you use for the `source` parameter.  
* **Custom Scoring:** The `execute()` method replaces {{es}} standard scoring with your custom logic. In this case, using term frequency as the document score. 

**For the complete implementation, refer to the [official script engine example](https://github.com/elastic/elasticsearch/blob/main/plugins/examples/script-expert-scoring/src/main/java/org/elasticsearch/example/expertscript/ExpertScriptPlugin.java).**

### Usage example

This example shows how to use your custom script engine in a search query:

```json
POST /_search
{
  "query": {
    "function_score": {
      "query": {
        "match": {
          "body": "foo"
        }
      },
      "functions": [
        {
          "script_score": {
            "script": {
                "source": "pure_df",
                "lang" : "expert_scripts",
                "params": {
                    "field": "body",
                    "term": "foo"
                }
            }
          }
        }
      ]
    }
  }
}

```


