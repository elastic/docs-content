---
navigation_title: "Using Cohere with {{es}}"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/cohere-es.html
applies_to:
  stack:
  serverless:
---



# Using Cohere with Elasticsearch [cohere-es]


The instructions in this tutorial shows you how to compute embeddings with Cohere using the {{infer}} API and store them for efficient vector or hybrid search in {{es}}. This tutorial will use the Python {{es}} client to perform the operations.

You’ll learn how to:

* create an {{infer}} endpoint for text embedding using the Cohere service,
* create the necessary index mapping for the {{es}} index,
* build an {{infer}} pipeline to ingest documents into the index together with the embeddings,
* perform hybrid search on the data,
* rerank search results by using Cohere’s rerank model,
* design a RAG system with Cohere’s Chat API.

The tutorial uses the [SciFact](https://huggingface.co/datasets/mteb/scifact) data set.

Refer to [Cohere’s tutorial](https://docs.cohere.com/docs/elasticsearch-and-cohere) for an example using a different data set.

You can also review the [Colab notebook version of this tutorial](https://colab.research.google.com/github/elastic/elasticsearch-labs/blob/main/notebooks/integrations/cohere/cohere-elasticsearch.ipynb).


## Requirements [cohere-es-req]

* A paid [Cohere account](https://cohere.com/) is required to use the {{infer-cap}} API with the Cohere service as the Cohere free trial API usage is limited,
* an [Elastic Cloud](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md) account,
* Python 3.7 or higher.


## Install required packages [cohere-es-packages]

Install {{es}} and Cohere:

```py
!pip install elasticsearch
!pip install cohere
```

Import the required packages:

```py
from elasticsearch import Elasticsearch, helpers
import cohere
import json
import requests
```


## Create the {{es}} client [cohere-es-client]

To create your {{es}} client, you need:

* [your Cloud ID](https://www.elastic.co/search-labs/tutorials/install-elasticsearch/elastic-cloud#finding-your-cloud-id),
* [an encoded API key](https://www.elastic.co/search-labs/tutorials/install-elasticsearch/elastic-cloud#creating-an-api-key).

```py
ELASTICSEARCH_ENDPOINT = "elastic_endpoint"
ELASTIC_API_KEY = "elastic_api_key"

client = Elasticsearch(
  cloud_id=ELASTICSEARCH_ENDPOINT,
  api_key=ELASTIC_API_KEY
)

# Confirm the client has connected
print(client.info())
```


## Create the {{infer}} endpoint [cohere-es-infer-endpoint]

[Create the {{infer}} endpoint](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-inference-put) first. In this example, the {{infer}} endpoint uses Cohere’s `embed-english-v3.0` model and the `embedding_type` is set to `byte`.

```py
COHERE_API_KEY = "cohere_api_key"

client.inference.put_model(
    task_type="text_embedding",
    inference_id="cohere_embeddings",
    body={
        "service": "cohere",
        "service_settings": {
            "api_key": COHERE_API_KEY,
            "model_id": "embed-english-v3.0",
            "embedding_type": "byte"
        }
    },
)
```

You can find your API keys in your Cohere dashboard under the [API keys section](https://dashboard.cohere.com/api-keys).


## Create the index mapping [cohere-es-index-mapping]

Create the index mapping for the index that will contain the embeddings.

```py
client.indices.create(
    index="cohere-embeddings",
    settings={"index": {"default_pipeline": "cohere_embeddings"}},
    mappings={
        "properties": {
            "text_embedding": {
                "type": "dense_vector",
                "dims": 1024,
                "element_type": "byte",
            },
            "text": {"type": "text"},
            "id": {"type": "integer"},
            "title": {"type": "text"}
        }
    },
)
```


## Create the {{infer}} pipeline [cohere-es-infer-pipeline]

Now you have an {{infer}} endpoint and an index ready to store embeddings. The next step is to create an [ingest pipeline](../../../manage-data/ingest/transform-enrich/ingest-pipelines.md) with an [{{infer}} processor](elasticsearch://reference/ingestion-tools/enrich-processor/inference-processor.md) that will create the embeddings using the {{infer}} endpoint and stores them in the index.

```py
client.ingest.put_pipeline(
    id="cohere_embeddings",
    description="Ingest pipeline for Cohere inference.",
    processors=[
        {
            "inference": {
                "model_id": "cohere_embeddings",
                "input_output": {
                    "input_field": "text",
                    "output_field": "text_embedding",
                },
            }
        }
    ],
)
```


## Prepare data and insert documents [cohere-es-insert-documents]

This example uses the [SciFact](https://huggingface.co/datasets/mteb/scifact) data set that you can find on HuggingFace.

```py
url = 'https://huggingface.co/datasets/mteb/scifact/raw/main/corpus.jsonl'

# Fetch the JSONL data from the URL
response = requests.get(url)
response.raise_for_status()  # Ensure noticing bad responses

# Split the content by new lines and parse each line as JSON
data = [json.loads(line) for line in response.text.strip().split('\n') if line]
# Now data is a list of dictionaries

# Change `_id` key to `id` as `_id` is a reserved key in Elasticsearch.
for item in data:
    if '_id' in item:
        item['id'] = item.pop('_id')

# Prepare the documents to be indexed
documents = []
for line in data:
    data_dict = line
    documents.append({
        "_index": "cohere-embeddings",
        "_source": data_dict,
        }
      )

# Use the bulk endpoint to index
helpers.bulk(client, documents)

print("Data ingestion completed, text embeddings generated!")
```

Your index is populated with the SciFact data and text embeddings for the text field.


## Hybrid search [cohere-es-hybrid-search]

Let’s start querying the index!

The code below performs a hybrid search. The `kNN` query computes the relevance of search results based on vector similarity using the `text_embedding` field, the lexical search query uses BM25 retrieval to compute keyword similarity on the `title` and `text` fields.

```py
query = "What is biosimilarity?"

response = client.search(
    index="cohere-embeddings",
    size=100,
    knn={
        "field": "text_embedding",
        "query_vector_builder": {
            "text_embedding": {
                "model_id": "cohere_embeddings",
                "model_text": query,
            }
        },
        "k": 10,
        "num_candidates": 50,
    },
    query={
        "multi_match": {
            "query": query,
            "fields": ["text", "title"]
        }
    }
)

raw_documents = response["hits"]["hits"]

# Display the first 10 results
for document in raw_documents[0:10]:
  print(f'Title: {document["_source"]["title"]}\nText: {document["_source"]["text"]}\n')

# Format the documents for ranking
documents = []
for hit in response["hits"]["hits"]:
    documents.append(hit["_source"]["text"])
```


### Rerank search results [cohere-es-rerank-results]

To combine the results more effectively, use [Cohere’s Rerank v3](https://docs.cohere.com/docs/rerank-2) model through the {{infer}} API to provide a more precise semantic reranking of the results.

Create an {{infer}} endpoint with your Cohere API key and the used model name as the `model_id` (`rerank-english-v3.0` in this example).

```py
client.inference.put_model(
    task_type="rerank",
    inference_id="cohere_rerank",
    body={
        "service": "cohere",
        "service_settings":{
            "api_key": COHERE_API_KEY,
            "model_id": "rerank-english-v3.0"
           },
        "task_settings": {
            "top_n": 10,
        },
    }
)
```

Rerank the results using the new {{infer}} endpoint.

```py
# Pass the query and the search results to the service
response = client.inference.rerank(
    inference_id="cohere_rerank",
    body={
        "query": query,
        "input": documents,
        "task_settings": {
            "return_documents": False
            }
        }
)

# Reconstruct the input documents based on the index provided in the rereank response
ranked_documents = []
for document in response.body["rerank"]:
  ranked_documents.append({
      "title": raw_documents[int(document["index"])]["_source"]["title"],
      "text": raw_documents[int(document["index"])]["_source"]["text"]
  })

# Print the top 10 results
for document in ranked_documents[0:10]:
  print(f"Title: {document['title']}\nText: {document['text']}\n")
```

The response is a list of documents in descending order of relevance. Each document has a corresponding index that reflects the order of the documents when they were sent to the {{infer}} endpoint.


## Retrieval Augmented Generation (RAG) with Cohere and {{es}} [cohere-es-rag]

[RAG](https://docs.cohere.com/docs/retrieval-augmented-generation-rag) is a method for generating text using additional information fetched from an external data source. With the ranked results, you can build a RAG system on the top of what you previously created by using [Cohere’s Chat API](https://docs.cohere.com/docs/chat-api).

Pass in the retrieved documents and the query to receive a grounded response using Cohere’s newest generative model [Command R+](https://docs.cohere.com/docs/command-r-plus).

Then pass in the query and the documents to the Chat API, and print out the response.

```py
response = co.chat(message=query, documents=ranked_documents, model='command-r-plus')

source_documents = []
for citation in response.citations:
    for document_id in citation.document_ids:
        if document_id not in source_documents:
            source_documents.append(document_id)

print(f"Query: {query}")
print(f"Response: {response.text}")
print("Sources:")
for document in response.documents:
    if document['id'] in source_documents:
        print(f"{document['title']}: {document['text']}")
```

The response will look similar to this:

```console-result
Query: What is biosimilarity?
Response: Biosimilarity is based on the comparability concept, which has been used successfully for several decades to ensure close similarity of a biological product before and after a manufacturing change. Over the last 10 years, experience with biosimilars has shown that even complex biotechnology-derived proteins can be copied successfully.
Sources:
Interchangeability of Biosimilars: A European Perspective: (...)
```
%  NOTCONSOLE
