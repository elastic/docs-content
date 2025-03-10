---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-scripting-engine.html
---

# Advanced scripts using script engines [modules-scripting-engine]

A `ScriptEngine` is a backend for implementing a scripting language. It may also be used to write scripts that need to use advanced internals of scripting. For example, a script that wants to use term frequencies while scoring.

The plugin [documentation](elasticsearch://extend/index.md) has more information on how to write a plugin so that Elasticsearch will properly load it. To register the `ScriptEngine`, your plugin should implement the `ScriptPlugin` interface and override the `getScriptEngine(Settings settings)` method.

The following is an example of a custom `ScriptEngine` which uses the language name `expert_scripts`. It implements a single script called `pure_df` which may be used as a search script to override each document’s score as the document frequency of a provided term.

```java
private static class MyExpertScriptEngine implements ScriptEngine {
    @Override
    public String getType() {
        return "expert_scripts";
    }

    @Override
    public <T> T compile(
        String scriptName,
        String scriptSource,
        ScriptContext<T> context,
        Map<String, String> params
    ) {
        if (context.equals(ScoreScript.CONTEXT) == false) {
            throw new IllegalArgumentException(getType()
                    + " scripts cannot be used for context ["
                    + context.name + "]");
        }
        // we use the script "source" as the script identifier
        if ("pure_df".equals(scriptSource)) {
            ScoreScript.Factory factory = new PureDfFactory();
            return context.factoryClazz.cast(factory);
        }
        throw new IllegalArgumentException("Unknown script name "
                + scriptSource);
    }

    @Override
    public void close() {
        // optionally close resources
    }

    @Override
    public Set<ScriptContext<?>> getSupportedContexts() {
        return Set.of(ScoreScript.CONTEXT);
    }

    private static class PureDfFactory implements ScoreScript.Factory,
                                                  ScriptFactory {
        @Override
        public boolean isResultDeterministic() {
            // PureDfLeafFactory only uses deterministic APIs, this
            // implies the results are cacheable.
            return true;
        }

        @Override
        public LeafFactory newFactory(
            Map<String, Object> params,
            SearchLookup lookup
        ) {
            return new PureDfLeafFactory(params, lookup);
        }
    }

    private static class PureDfLeafFactory implements LeafFactory {
        private final Map<String, Object> params;
        private final SearchLookup lookup;
        private final String field;
        private final String term;

        private PureDfLeafFactory(
                    Map<String, Object> params, SearchLookup lookup) {
            if (params.containsKey("field") == false) {
                throw new IllegalArgumentException(
                        "Missing parameter [field]");
            }
            if (params.containsKey("term") == false) {
                throw new IllegalArgumentException(
                        "Missing parameter [term]");
            }
            this.params = params;
            this.lookup = lookup;
            field = params.get("field").toString();
            term = params.get("term").toString();
        }

        @Override
        public boolean needs_score() {
            return false;  // Return true if the script needs the score
        }

        @Override
        public boolean needs_termStats() {
            return false; // Return true if the script needs term statistics via get_termStats()
        }

        @Override
        public ScoreScript newInstance(DocReader docReader)
                throws IOException {
            DocValuesDocReader dvReader = DocValuesDocReader) docReader);             PostingsEnum postings = dvReader.getLeafReaderContext()                     .reader().postings(new Term(field, term;
            if (postings == null) {
                /*
                 * the field and/or term don't exist in this segment,
                 * so always return 0
                 */
                return new ScoreScript(params, lookup, docReader) {
                    @Override
                    public double execute(
                        ExplanationHolder explanation
                    ) {
                        if(explanation != null) {
                            explanation.set("An example optional custom description to explain details for this script's execution; we'll provide a default one if you leave this out.");
                        }
                        return 0.0d;
                    }
                };
            }
            return new ScoreScript(params, lookup, docReader) {
                int currentDocid = -1;
                @Override
                public void setDocument(int docid) {
                    /*
                     * advance has undefined behavior calling with
                     * a docid <= its current docid
                     */
                    if (postings.docID() < docid) {
                        try {
                            postings.advance(docid);
                        } catch (IOException e) {
                            throw new UncheckedIOException(e);
                        }
                    }
                    currentDocid = docid;
                }
                @Override
                public double execute(ExplanationHolder explanation) {
                    if(explanation != null) {
                        explanation.set("An example optional custom description to explain details for this script's execution; we'll provide a default one if you leave this out.");
                    }
                    if (postings.docID() != currentDocid) {
                        /*
                         * advance moved past the current doc, so this
                         * doc has no occurrences of the term
                         */
                        return 0.0d;
                    }
                    try {
                        return postings.freq();
                    } catch (IOException e) {
                        throw new UncheckedIOException(e);
                    }
                }
            };
        }
    }
}
```

You can execute the script by specifying its `lang` as `expert_scripts`, and the name of the script as the script source:

```console
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
%  TEST[skip:we don’t have an expert script plugin installed to test this]

