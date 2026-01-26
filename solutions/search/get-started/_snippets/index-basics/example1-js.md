% WARNING: This snippet is auto-generated. Do not edit directly.

% See https://github.com/leemthompo/python-console-converter/blob/main/README.md

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
