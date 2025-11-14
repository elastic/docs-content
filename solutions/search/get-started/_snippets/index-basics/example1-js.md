```js
const { Client } = require("@elastic/elasticsearch");

const client = new Client({
  nodes: [process.env["ELASTICSEARCH_URL"]],
  auth: {
    apiKey: process.env["ELASTIC_API_KEY"],
  },
});

async function run() {
  const response = await client.indices.create({
    index: "books",
  });
  console.log(response);
}

run();
```
