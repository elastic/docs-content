---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-knn-search.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
products:
  - id: elasticsearch
---

# Tune approximate kNN search [tune-knn-search]

{{es}} supports [approximate k-nearest neighbor search](../../../solutions/search/vector/knn.md#approximate-knn) for efficiently finding the *k* nearest vectors to a query vector. Since approximate kNN search works differently from other queries, there are special considerations around its performance.

Many of these recommendations help improve search speed. With approximate kNN, the indexing algorithm runs searches under the hood to create the vector index structures. So these same recommendations also help with indexing speed.


## Reduce vector memory foot-print [_reduce_vector_memory_foot_print]

The default [`element_type`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-element-type) is `float`. But this can be automatically quantized during index time through [`quantization`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization). Quantization will reduce the required memory by 4x, 8x, or as much as 32x, but it will also reduce the precision of the vectors and increase disk usage for the field (by up to 25%, 12.5%, or 3.125%, respectively). Increased disk usage is a result of {{es}} storing both the quantized and the unquantized vectors. For example, when int8 quantizing 40GB of floating point vectors an extra 10GB of data will be stored for the quantized vectors. The total disk usage amounts to 50GB, but the memory usage for fast search will be reduced to 10GB.

For `float` vectors with `dim` greater than or equal to `384`, using a [`quantized`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization) index is highly recommended.


## Reduce vector dimensionality [_reduce_vector_dimensionality]

The speed of kNN search scales linearly with the number of vector dimensions, because each similarity computation considers each element in the two vectors. Whenever possible, it’s better to use vectors with a lower dimension. Some embedding models come in different "sizes", with both lower and higher dimensional options available. You could also experiment with dimensionality reduction techniques like PCA. When experimenting with different approaches, it’s important to measure the impact on relevance to ensure the search quality is still acceptable.


## Exclude vector fields from `_source` [_exclude_vector_fields_from_source]

{{es}} stores the original JSON document that was passed at index time in the [`_source` field](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md). By default, each hit in the search results contains the full document `_source`. When the documents contain high-dimensional `dense_vector` fields, the `_source` can be quite large and expensive to load. This could significantly slow down the speed of kNN search.

::::{note}
[reindex](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex), [update](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-update), and [update by query](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-update-by-query) operations generally require the `_source` field. Disabling `_source` for a field might result in unexpected behavior for these operations. For example, reindex might not actually contain the `dense_vector` field in the new index.
::::


You can disable storing `dense_vector` fields in the `_source` through the [`excludes`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md#include-exclude) mapping parameter. This prevents loading and returning large vectors during search, and also cuts down on the index size. Vectors that have been omitted from `_source` can still be used in kNN search, since it relies on separate data structures to perform the search. Before using the [`excludes`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md#include-exclude) parameter, make sure to review the downsides of omitting fields from `_source`.

Another option is to use  [synthetic `_source`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-source-field.md#synthetic-source).


## Ensure data nodes have enough memory [_ensure_data_nodes_have_enough_memory]

{{es}} uses either the Hierarchical Navigable Small World ([HNSW](https://arxiv.org/abs/1603.09320)) algorithm or the Disk Better Binary Quantization ([DiskBBQ](https://www.elastic.co/search-labs/blog/diskbbq-elasticsearch-introduction)) algorithm for approximate kNN search. 

HNSW is a graph-based algorithm which only works efficiently when most vector data is held in memory. You should ensure that data nodes have at least enough RAM to hold the vector data and index structures.

DiskBBQ is a clustering algorithm which can scale effeciently often on less memory than HNSW.  Where HNSW typically performs poorly without sufficient memory to fit the entire structure in RAM, DiskBBQ scales linearly when using less available memory than the total index size. You can start with enough RAM to hold the vector data and index structures but, in most cases, you should be able to reduce your RAM allocation and still maintain good performance. In testing, as little as 1-5% of the index structure size (centroids and quantized vector data) loaded in off-heap RAM is necessary for reasonable performance for each set of queries that accesses largely overlapping clusters.  

To check the size of the vector data, you can use the [Analyze index disk usage](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-disk-usage) API.

Here are estimates for different element types and quantization levels:

| `element_type` | `quantization` | Required RAM |
| --- | --- | --- |
| `float` | none | `num_vectors * num_dimensions * 4` | 
| `float` | `int8` | `num_vectors * (num_dimensions + 4)` |
| `float` | `int4` | `num_vectors * (num_dimensions/2 + 4)` |
| `float` | `bbq` |  `num_vectors * (num_dimensions/8 + 14)` |
| `bfloat16` | none | `num_vectors * num_dimensions * 2` |
| `bfloat16` | `int8` | `num_vectors * (num_dimensions + 4)` |
| `bfloat16` | `int4` | `num_vectors * (num_dimensions/2 + 4)` |
| `bfloat16` | `bbq` |  `num_vectors * (num_dimensions/8 + 14)` |
| `byte` | none |  `num_vectors * num_dimensions` |
| `bit` | none | `num_vectors * (num_dimensions/8)` |

If you're using HNSW, the graph must also be in memory. To estimate the required bytes, use the following formula below. The default value for the HNSW `m` parameter is `16`.

```{math}
\begin{align*}
estimated\ bytes &= num\_vectors \times 4 \times m \\
&= num\_vectors \times 4 \times 16
\end{align*}
```

The following is an example of an estimate with the HNSW indexed `element_type: float` with no quantization, `m` set to `16`, and `1,000,000` vectors of `1024` dimensions:

```{math}
\begin{align*}
estimated\ bytes &= (1,000,000 \times 4 \times 16) + (1,000,000 \times 4 \times 1024) \\
&= 64,000,000 + 4,096,000,000 \\
&= 4,160,000,000 \\
&= 3.87GB
\end{align*}
```

If you're using DiskBBQ, a fraction of the clusters and centroids need to be in memory.  When doing this estimation, it makes more sense to include both the index structure and the quantized vectors together as the structures are dependent. To estimate the total bytes, first compute the number of clusters, then compute the cost of the centroids plus the cost of the quantized vectors within the clusters to get the total estimated bytes.  The default value for the number of `vectors_per_cluster` is `384`.

```{math}
\begin{align*}
num\_clusters=\frac{num\_vectors}{vectors\_per\_cluster}=\frac{num\_vectors}{384}
\end{align*}
```

```{math}
\begin{align*}
estimated\ centroid\ bytes &= num\_clusters \times num\_dimensions \times 4 \\
& + num\_clusters \times (num\_dimensions + 14)
\end{align*}
```

```{math}
\begin{align*}
estimated\ quantized\ vector\ bytes = num\_vectors \times ((num\_dimensions/8 + 14 + 2) \times 2)
\end{align*}
```

Note that the required RAM is for the filesystem cache, which is separate from the Java heap.

The data nodes should also leave a buffer for other ways that RAM is needed. For example your index might also include text fields and numerics, which also benefit from using filesystem cache. It’s recommended to run benchmarks with your specific dataset to ensure there’s a sufficient amount of memory to give good search performance. You can find [here](https://elasticsearch-benchmarks.elastic.co/#tracks/so_vector) and [here](https://elasticsearch-benchmarks.elastic.co/#tracks/dense_vector) some examples of datasets and configurations that we use for our nightly benchmarks.


<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {
    --eui-page-bg: #FFFFFF;
    --eui-body-bg: #F6F9FC;
    --eui-panel-bg: #FFFFFF;
    --eui-highlight-bg: #ECF1F9;
    --eui-text: #1D2A3E;
    --eui-text-heading: #111C2C;
    --eui-text-subdued: #516381;
    --eui-text-ink: #07101F;
    --eui-link: #1750BA;
    --eui-primary: #0B64DD;
    --eui-primary-light: #BFDBFF;
    --eui-accent: #BC1E70;
    --eui-accent-secondary: #008B87;
    --eui-success: #008A5E;
    --eui-warning: #FACB3D;
    --eui-danger: #C61E25;
    --eui-border: #E3E8F2;
    --eui-border-strong: #CAD3E2;
    --eui-radius: 4px;
    --eui-shadow: 0 2px 4px rgba(0,0,0,0.05), 0 6px 12px rgba(0,0,0,0.05);
    --eui-font: 'Inter', BlinkMacSystemFont, Helvetica, Arial, sans-serif;
    --eui-mono: 'Roboto Mono', Menlo, Courier, monospace;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: var(--eui-font);
    background: var(--eui-body-bg);
    color: var(--eui-text);
    font-size: 1rem;
    line-height: 1.5;
    min-height: 100vh;
    -webkit-font-smoothing: antialiased;
  }

  .container {
    max-width: 800px;
    margin: 0 auto;
    padding: 32px 24px;
  }

  header {
    margin-bottom: 24px;
  }

  header h1 {
    font-size: 1.714rem;
    font-weight: 700;
    color: var(--eui-text-heading);
    letter-spacing: -0.01em;
    margin-bottom: 4px;
    line-height: 1.25;
  }

  header p {
    color: var(--eui-text-subdued);
    font-size: 0.875rem;
  }

  .card {
    background: var(--eui-panel-bg);
    border: 1px solid var(--eui-border);
    border-radius: var(--eui-radius);
    padding: 24px;
    margin-bottom: 16px;
    box-shadow: var(--eui-shadow);
  }

  .card-title {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--eui-text-subdued);
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--eui-border);
  }

  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; }

  @media (max-width: 640px) {
    .grid-2, .grid-3 { grid-template-columns: 1fr; }
  }

  .field { display: flex; flex-direction: column; gap: 4px; }

  .field label {
    font-size: 0.857rem;
    font-weight: 600;
    color: var(--eui-text);
  }

  .field input, .field select {
    background: var(--eui-page-bg);
    border: 1px solid var(--eui-border-strong);
    border-radius: var(--eui-radius);
    padding: 8px 12px;
    font-size: 0.875rem;
    color: var(--eui-text);
    outline: none;
    transition: border-color 0.15s, box-shadow 0.15s;
    font-family: var(--eui-font);
    line-height: 1.5;
  }

  .field input:focus, .field select:focus {
    border-color: var(--eui-primary);
    box-shadow: 0 0 0 1px var(--eui-primary);
  }

  .field input::placeholder { color: #A2B1C9; }

  .field select option { background: var(--eui-page-bg); color: var(--eui-text); }

  .field .hint {
    font-size: 0.75rem;
    color: var(--eui-text-subdued);
  }

  .results-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }

  @media (max-width: 640px) {
    .results-grid { grid-template-columns: 1fr; }
  }

  .result-block {
    background: var(--eui-body-bg);
    border-radius: var(--eui-radius);
    padding: 16px 20px;
    border: 1px solid var(--eui-border);
  }

  .result-block.highlight {
    border-color: var(--eui-primary-light);
    background: #F0F6FF;
  }

  .result-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--eui-text-subdued);
    margin-bottom: 4px;
  }

  .result-value {
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    color: var(--eui-text-heading);
  }

  .result-value .unit {
    font-size: 0.857rem;
    font-weight: 500;
    color: var(--eui-text-subdued);
    margin-left: 2px;
  }

  .result-sub {
    font-size: 0.75rem;
    color: var(--eui-text-subdued);
    margin-top: 2px;
    font-variant-numeric: tabular-nums;
  }

  .breakdown {
    margin-top: 20px;
  }

  .breakdown-title {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--eui-text-subdued);
    margin-bottom: 8px;
  }

  .breakdown-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid var(--eui-border);
    font-size: 0.857rem;
  }

  .breakdown-row:last-child { border-bottom: none; }

  .breakdown-row .label { color: var(--eui-text-subdued); }
  .breakdown-row .value { font-weight: 600; color: var(--eui-text); font-variant-numeric: tabular-nums; }

  .bar-chart {
    margin-top: 12px;
  }

  .bar-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 6px;
  }

  .bar-label {
    font-size: 0.75rem;
    color: var(--eui-text-subdued);
    width: 160px;
    min-width: 160px;
    text-align: right;
  }

  .bar-track {
    flex: 1;
    height: 16px;
    background: var(--eui-highlight-bg);
    border-radius: var(--eui-radius);
    overflow: hidden;
  }

  .bar-fill {
    height: 100%;
    border-radius: var(--eui-radius);
    transition: width 0.4s ease;
    min-width: 2px;
  }

  .bar-fill.disk-raw { background: var(--eui-primary); }
  .bar-fill.disk-quant { background: var(--eui-accent-secondary); }
  .bar-fill.disk-index { background: var(--eui-warning); }
  .bar-fill.ram-vec { background: var(--eui-primary); }
  .bar-fill.ram-index { background: var(--eui-accent-secondary); }

  .bar-amount {
    font-size: 0.75rem;
    color: var(--eui-text-subdued);
    min-width: 70px;
    font-variant-numeric: tabular-nums;
  }

  .legend {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    margin-top: 8px;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 0.75rem;
    color: var(--eui-text-subdued);
  }

  .legend-dot {
    width: 8px;
    height: 8px;
    border-radius: 2px;
  }

  .note-box {
    background: #E6F9F7;
    border: 1px solid #B3ECE8;
    border-radius: var(--eui-radius);
    padding: 12px 16px;
    font-size: 0.857rem;
    color: var(--eui-text);
    line-height: 1.5;
    margin-top: 12px;
  }

  .note-box strong { color: var(--eui-accent-secondary); font-weight: 600; }

  .warn-box {
    background: #FFF0F5;
    border: 1px solid #F5C2D8;
    border-radius: var(--eui-radius);
    padding: 12px 16px;
    font-size: 0.857rem;
    color: var(--eui-text);
    line-height: 1.5;
    margin-top: 12px;
    display: none;
  }

  .warn-box strong { color: var(--eui-danger); font-weight: 600; }
  .warn-box.visible { display: block; }

  .advanced-toggle summary {
    font-size: 0.857rem;
    color: var(--eui-link);
    cursor: pointer;
    user-select: none;
    font-weight: 500;
  }

  .advanced-toggle summary:hover { text-decoration: underline; }

  .formula-ref {
    margin-top: 16px;
    padding-top: 12px;
    border-top: 1px solid var(--eui-border);
  }

  .formula-ref summary {
    font-size: 0.857rem;
    color: var(--eui-link);
    cursor: pointer;
    user-select: none;
    font-weight: 500;
  }

  .formula-ref summary:hover { text-decoration: underline; }

  .formula-ref .formulas {
    margin-top: 10px;
    padding: 12px 16px;
    font-size: 0.8125rem;
    color: var(--eui-text);
    background: var(--eui-body-bg);
    border: 1px solid var(--eui-border);
    border-radius: var(--eui-radius);
    font-family: var(--eui-mono);
    line-height: 1.7;
    white-space: pre-wrap;
  }

  footer {
    text-align: center;
    padding: 24px;
    font-size: 0.75rem;
    color: var(--eui-text-subdued);
  }

  footer a { color: var(--eui-link); text-decoration: none; }
  footer a:hover { text-decoration: underline; }
</style>

<div class="container">
  <header>
    <h1>Elasticsearch Vector Sizing Calculator</h1>
    <p>Estimate disk and off-heap RAM requirements for dense_vector fields</p>
  </header>

  <!-- Inputs -->
  <div class="card">
    <div class="card-title">Configuration</div>
    <div class="grid-3">
      <div class="field">
        <label for="numVectors">Number of vectors</label>
        <input type="text" id="numVectors" placeholder="e.g. 10000000" inputmode="numeric">
      </div>
      <div class="field">
        <label for="numDimensions">Dimensions</label>
        <input type="number" id="numDimensions" placeholder="e.g. 768" min="1" max="65536">
      </div>
      <div class="field">
        <label for="elementType">Element type</label>
        <select id="elementType">
          <option value="float">float (4 bytes/dim)</option>
          <option value="bfloat16">bfloat16 (2 bytes/dim)</option>
          <option value="byte">byte (1 byte/dim)</option>
          <option value="bit">bit (1 bit/dim)</option>
        </select>
      </div>
    </div>

    <div class="grid-3" style="margin-top: 16px;">
      <div class="field">
        <label for="indexType">Index structure</label>
        <select id="indexType">
          <option value="hnsw">HNSW</option>
          <option value="flat">Flat (brute-force)</option>
          <option value="disk_bbq">DiskBBQ</option>
        </select>
      </div>
      <div class="field" id="quantField">
        <label for="quantization">Quantization</label>
        <select id="quantization">
          <option value="none">None</option>
          <option value="int8">int8</option>
          <option value="int4">int4</option>
          <option value="bbq">BBQ</option>
        </select>
      </div>
      <div class="field" id="numReplicasField">
        <label for="numReplicas">Number of replicas</label>
        <input type="number" id="numReplicas" value="1" min="0">
        <span class="hint">Total copies = 1 primary + replicas</span>
      </div>
    </div>

    <div id="hnswAdvanced" class="advanced-toggle" style="display:none; margin-top: 16px;">
      <details>
        <summary>Advanced HNSW parameters</summary>
        <div class="grid-3" style="margin-top: 12px;">
          <div class="field">
            <label for="hnswM">m (connections per node)</label>
            <input type="number" id="hnswM" value="16" min="2" max="512">
            <span class="hint">Default: 16</span>
          </div>
          <div class="field">
            <label for="efConstruction">ef_construction</label>
            <input type="number" id="efConstruction" value="100" min="1">
            <span class="hint">Default: 100 — build-time quality, no sizing impact</span>
          </div>
        </div>
      </details>
    </div>

    <div id="bbqAdvanced" class="advanced-toggle" style="display:none; margin-top: 16px;">
      <details>
        <summary>Advanced DiskBBQ parameters</summary>
        <div class="grid-3" style="margin-top: 12px;">
          <div class="field">
            <label for="bbqVpc">Vectors per cluster</label>
            <input type="number" id="bbqVpc" value="384" min="1">
            <span class="hint">Default: 384</span>
          </div>
        </div>
      </details>
    </div>

    <div id="warnInvalidCombo" class="warn-box">
      <strong>Invalid combination.</strong> <span id="warnMsg"></span>
    </div>

    <div id="noteRecommendation" class="note-box" style="display:none;"></div>
  </div>

  <!-- Results -->
  <div id="resultsArea">
    <div class="card">
      <div class="card-title">Estimated Requirements (per replica)</div>
      <div class="results-grid">
        <div class="result-block highlight">
          <div class="result-label">Total Disk</div>
          <div class="result-value" id="totalDisk">—</div>
          <div class="result-sub" id="totalDiskBytes"></div>
        </div>
        <div class="result-block highlight">
          <div class="result-label">Off-Heap RAM</div>
          <div class="result-value" id="totalRam">—</div>
          <div class="result-sub" id="totalRamBytes"></div>
        </div>
      </div>

      <!-- Disk Breakdown -->
      <div class="breakdown">
        <div class="breakdown-title">Disk Breakdown</div>
        <div id="diskBreakdown"></div>
        <div class="bar-chart" id="diskChart"></div>
      </div>

      <!-- RAM Breakdown -->
      <div class="breakdown" style="margin-top: 24px;">
        <div class="breakdown-title">Off-Heap RAM Breakdown</div>
        <div id="ramBreakdown"></div>
        <div class="bar-chart" id="ramChart"></div>
      </div>
    </div>

    <!-- With replicas -->
    <div class="card" id="clusterCard" style="display:none;">
      <div class="card-title">Cluster-Wide Totals</div>
      <div class="results-grid">
        <div class="result-block">
          <div class="result-label">Total Disk (all copies)</div>
          <div class="result-value" id="clusterDisk">—</div>
          <div class="result-sub" id="clusterDiskSub"></div>
        </div>
        <div class="result-block">
          <div class="result-label">Total Off-Heap RAM (all copies)</div>
          <div class="result-value" id="clusterRam">—</div>
          <div class="result-sub" id="clusterRamSub"></div>
        </div>
      </div>
    </div>

    <!-- Formulas -->
    <div class="card">
      <div class="formula-ref">
        <details>
          <summary>Show formulas used</summary>
          <div class="formulas" id="formulaText"></div>
        </details>
      </div>
    </div>
  </div>
</div>

<script>
(function() {
  const $ = (id) => document.getElementById(id);

  const inputs = ['numVectors', 'numDimensions', 'elementType', 'indexType', 'quantization', 'hnswM', 'efConstruction', 'bbqVpc', 'numReplicas'];
  inputs.forEach(id => {
    const el = $(id);
    el.addEventListener('input', recalculate);
    el.addEventListener('change', recalculate);
  });

  // Format the vector count input with thousands separators on blur
  const vecInput = $('numVectors');
  vecInput.addEventListener('blur', function() {
    const val = parseVectorCount(this.value);
    if (!isNaN(val) && val > 0) {
      this.value = val.toLocaleString('en-US');
    }
  });

  function parseVectorCount(str) {
    if (!str) return NaN;
    str = str.trim().replace(/,/g, '');
    const multipliers = { k: 1e3, K: 1e3, m: 1e6, M: 1e6, b: 1e9, B: 1e9 };
    const match = str.match(/^(\d+\.?\d*)\s*([kKmMbB])?$/);
    if (!match) return parseInt(str, 10);
    const num = parseFloat(match[1]);
    const mult = match[2] ? multipliers[match[2]] : 1;
    return Math.round(num * mult);
  }

  function formatBytes(bytes) {
    if (bytes === 0) return { value: '0', unit: 'bytes' };
    const units = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB'];
    let idx = 0;
    let val = bytes;
    while (val >= 1024 && idx < units.length - 1) {
      val /= 1024;
      idx++;
    }
    return { value: val < 10 ? val.toFixed(2) : val < 100 ? val.toFixed(1) : val.toFixed(0), unit: units[idx] };
  }

  function formatBytesStr(bytes) {
    const f = formatBytes(bytes);
    return f.value + ' ' + f.unit;
  }

  function formatExactBytes(bytes) {
    return bytes.toLocaleString('en-US') + ' bytes';
  }

  function updateVisibility() {
    const idx = $('indexType').value;
    const elType = $('elementType').value;
    const quantSel = $('quantization');

    // Show/hide advanced parameter sections
    $('hnswAdvanced').style.display = idx === 'hnsw' ? 'block' : 'none';
    $('bbqAdvanced').style.display = idx === 'disk_bbq' ? 'block' : 'none';

    // Quantization options based on index type and element type
    const prev = quantSel.value;
    quantSel.innerHTML = '';

    if (idx === 'disk_bbq') {
      quantSel.innerHTML = '<option value="bbq">BBQ (built-in)</option>';
      quantSel.disabled = true;
    } else {
      quantSel.disabled = false;
      const opts = [{ v: 'none', l: 'None' }];
      if (elType === 'float' || elType === 'bfloat16') {
        opts.push({ v: 'int8', l: 'int8' });
        opts.push({ v: 'int4', l: 'int4' });
        opts.push({ v: 'bbq', l: 'BBQ' });
      }
      opts.forEach(o => {
        const opt = document.createElement('option');
        opt.value = o.v;
        opt.textContent = o.l;
        if (o.v === prev) opt.selected = true;
        quantSel.appendChild(opt);
      });
    }
  }

  function recalculate() {
    updateVisibility();

    const V = parseVectorCount($('numVectors').value);
    const D = parseInt($('numDimensions').value, 10);
    const elType = $('elementType').value;
    const idxType = $('indexType').value;
    const quant = $('quantization').value;
    const m = parseInt($('hnswM').value, 10) || 16;
    const vpc = parseInt($('bbqVpc').value, 10) || 384;
    const replicas = parseInt($('numReplicas').value, 10) || 0;

    // Validation
    const warn = $('warnInvalidCombo');
    const warnMsg = $('warnMsg');
    warn.classList.remove('visible');

    if (isNaN(V) || isNaN(D) || V <= 0 || D <= 0) {
      $('totalDisk').textContent = '—';
      $('totalRam').textContent = '—';
      $('totalDiskBytes').textContent = '';
      $('totalRamBytes').textContent = '';
      $('diskBreakdown').innerHTML = '';
      $('ramBreakdown').innerHTML = '';
      $('diskChart').innerHTML = '';
      $('ramChart').innerHTML = '';
      $('clusterCard').style.display = 'none';
      $('formulaText').textContent = '';
      return;
    }

    if ((elType === 'byte' || elType === 'bit') && quant !== 'none' && idxType !== 'disk_bbq') {
      warn.classList.add('visible');
      warnMsg.textContent = `Quantization is not applicable to ${elType} element type.`;
    }

    // Recommendation note
    const noteEl = $('noteRecommendation');
    if (elType === 'float' && D >= 384 && quant === 'none' && idxType !== 'disk_bbq') {
      noteEl.style.display = 'block';
      noteEl.innerHTML = '<strong>Recommendation:</strong> For float vectors with dimensions >= 384, Elastic strongly recommends using a quantized index to reduce memory footprint.';
    } else {
      noteEl.style.display = 'none';
    }

    // --- Compute sizes (per replica = one full copy of all vectors) ---
    const formulas = [];

    // 1. Raw vector bytes per vector
    let rawBytesPerVec;
    switch (elType) {
      case 'float': rawBytesPerVec = D * 4; break;
      case 'bfloat16': rawBytesPerVec = D * 2; break;
      case 'byte': rawBytesPerVec = D; break;
      case 'bit': rawBytesPerVec = Math.ceil(D / 8); break;
    }
    const rawVectorDisk = V * rawBytesPerVec;
    formulas.push(`Raw vectors on disk = ${V.toLocaleString()} × ${rawBytesPerVec} = ${formatBytesStr(rawVectorDisk)}`);

    // 2. Quantized vector bytes (additional on disk)
    let quantDisk = 0;
    let quantLabel = '';
    if (idxType !== 'disk_bbq') {
      switch (quant) {
        case 'int8':
          quantDisk = V * (D + 4);
          quantLabel = 'int8 quantized vectors';
          formulas.push(`int8 quantized = V × (D + 4) = ${formatBytesStr(quantDisk)}`);
          break;
        case 'int4':
          quantDisk = V * (Math.ceil(D / 2) + 4);
          quantLabel = 'int4 quantized vectors';
          formulas.push(`int4 quantized = V × (D/2 + 4) = ${formatBytesStr(quantDisk)}`);
          break;
        case 'bbq':
          quantDisk = V * (Math.ceil(D / 8) + 14);
          quantLabel = 'BBQ quantized vectors';
          formulas.push(`BBQ quantized = V × (D/8 + 14) = ${formatBytesStr(quantDisk)}`);
          break;
        default:
          break;
      }
    }

    // 3. Index structure bytes on disk
    let indexDisk = 0;
    let indexLabel = '';
    let diskBBQCentroidDisk = 0;
    let diskBBQClusterDisk = 0;

    if (idxType === 'hnsw') {
      indexDisk = V * 4 * m;
      indexLabel = 'HNSW graph';
      formulas.push(`HNSW graph = V × 4 × m = ${V.toLocaleString()} × 4 × ${m} = ${formatBytesStr(indexDisk)}`);
    } else if (idxType === 'disk_bbq') {
      const numClusters = Math.ceil(V / vpc);
      diskBBQCentroidDisk = numClusters * D * 4 + numClusters * (D + 14);
      diskBBQClusterDisk = V * ((Math.ceil(D / 8) + 14 + 2) * 2);
      indexDisk = diskBBQCentroidDisk + diskBBQClusterDisk;
      indexLabel = 'DiskBBQ structures';
      formulas.push(`DiskBBQ clusters = ceil(V / ${vpc}) = ${numClusters.toLocaleString()}`);
      formulas.push(`Centroid bytes = clusters × D × 4 + clusters × (D + 14) = ${formatBytesStr(diskBBQCentroidDisk)}`);
      formulas.push(`Quantized cluster vectors = V × ((D/8 + 14 + 2) × 2) = ${formatBytesStr(diskBBQClusterDisk)}`);
    }

    const totalDisk = rawVectorDisk + quantDisk + indexDisk;
    formulas.push(`Total disk (per replica) = raw + quantized + index = ${formatBytesStr(totalDisk)}`);

    // 4. Off-heap RAM
    let ramVectors = 0;
    let ramVecLabel = '';
    let ramIndex = 0;
    let ramIdxLabel = '';

    if (idxType === 'hnsw' || idxType === 'flat') {
      switch (quant) {
        case 'none':
          ramVectors = rawVectorDisk;
          ramVecLabel = 'Raw vectors in RAM';
          formulas.push(`Vector RAM = raw vector size = ${formatBytesStr(ramVectors)}`);
          break;
        case 'int8':
          ramVectors = V * (D + 4);
          ramVecLabel = 'int8 vectors in RAM';
          formulas.push(`Vector RAM (int8) = V × (D + 4) = ${formatBytesStr(ramVectors)}`);
          break;
        case 'int4':
          ramVectors = V * (Math.ceil(D / 2) + 4);
          ramVecLabel = 'int4 vectors in RAM';
          formulas.push(`Vector RAM (int4) = V × (D/2 + 4) = ${formatBytesStr(ramVectors)}`);
          break;
        case 'bbq':
          ramVectors = V * (Math.ceil(D / 8) + 14);
          ramVecLabel = 'BBQ vectors in RAM';
          formulas.push(`Vector RAM (BBQ) = V × (D/8 + 14) = ${formatBytesStr(ramVectors)}`);
          break;
      }

      if (idxType === 'hnsw') {
        ramIndex = V * 4 * m;
        ramIdxLabel = 'HNSW graph in RAM';
        formulas.push(`HNSW graph RAM = V × 4 × ${m} = ${formatBytesStr(ramIndex)}`);
      }
    } else if (idxType === 'disk_bbq') {
      const fullStructure = diskBBQCentroidDisk + diskBBQClusterDisk;
      ramVectors = Math.ceil(fullStructure * 0.05);
      ramVecLabel = 'DiskBBQ structures (~5% in RAM)';
      formulas.push(`DiskBBQ RAM ≈ 5% × (centroids + quantized) = 5% × ${formatBytesStr(fullStructure)} = ${formatBytesStr(ramVectors)}`);
      formulas.push(`  Note: 1–5% of index structure in RAM is typically sufficient for DiskBBQ`);
    }

    const totalRam = ramVectors + ramIndex;
    formulas.push(`Total off-heap RAM (per replica) = ${formatBytesStr(totalRam)}`);

    // --- Render results ---

    // Totals
    const diskFmt = formatBytes(totalDisk);
    $('totalDisk').innerHTML = `${diskFmt.value}<span class="unit">${diskFmt.unit}</span>`;
    $('totalDiskBytes').textContent = formatExactBytes(totalDisk);

    const ramFmt = formatBytes(totalRam);
    $('totalRam').innerHTML = `${ramFmt.value}<span class="unit">${ramFmt.unit}</span>`;
    $('totalRamBytes').textContent = formatExactBytes(totalRam);

    // Disk breakdown
    const diskItems = [
      { label: 'Raw vectors', value: rawVectorDisk, cls: 'disk-raw' },
    ];
    if (quantDisk > 0) diskItems.push({ label: quantLabel, value: quantDisk, cls: 'disk-quant' });
    if (indexDisk > 0) diskItems.push({ label: indexLabel, value: indexDisk, cls: 'disk-index' });

    $('diskBreakdown').innerHTML = diskItems.map(i =>
      `<div class="breakdown-row"><span class="label">${i.label}</span><span class="value">${formatBytesStr(i.value)}</span></div>`
    ).join('');

    // Disk bar chart
    const maxDisk = Math.max(...diskItems.map(i => i.value), 1);
    $('diskChart').innerHTML = diskItems.map(i => {
      const pct = Math.max((i.value / totalDisk) * 100, 0.5);
      return `<div class="bar-row">
        <span class="bar-label">${i.label}</span>
        <div class="bar-track"><div class="bar-fill ${i.cls}" style="width:${pct}%"></div></div>
        <span class="bar-amount">${formatBytesStr(i.value)}</span>
      </div>`;
    }).join('') + `<div class="legend">
      <div class="legend-item"><div class="legend-dot" style="background:var(--eui-primary)"></div>Raw vectors</div>
      ${quantDisk > 0 ? '<div class="legend-item"><div class="legend-dot" style="background:var(--eui-accent-secondary)"></div>Quantized</div>' : ''}
      ${indexDisk > 0 ? '<div class="legend-item"><div class="legend-dot" style="background:var(--eui-warning)"></div>Index structure</div>' : ''}
    </div>`;

    // RAM breakdown
    const ramItems = [];
    if (ramVectors > 0) ramItems.push({ label: ramVecLabel, value: ramVectors, cls: 'ram-vec' });
    if (ramIndex > 0) ramItems.push({ label: ramIdxLabel, value: ramIndex, cls: 'ram-index' });

    $('ramBreakdown').innerHTML = ramItems.map(i =>
      `<div class="breakdown-row"><span class="label">${i.label}</span><span class="value">${formatBytesStr(i.value)}</span></div>`
    ).join('');

    // RAM bar chart
    $('ramChart').innerHTML = ramItems.map(i => {
      const pct = Math.max((i.value / totalRam) * 100, 0.5);
      return `<div class="bar-row">
        <span class="bar-label">${i.label}</span>
        <div class="bar-track"><div class="bar-fill ${i.cls}" style="width:${pct}%"></div></div>
        <span class="bar-amount">${formatBytesStr(i.value)}</span>
      </div>`;
    }).join('') + (ramItems.length > 1 ? `<div class="legend">
      <div class="legend-item"><div class="legend-dot" style="background:var(--eui-primary)"></div>Vector data</div>
      <div class="legend-item"><div class="legend-dot" style="background:var(--eui-accent-secondary)"></div>Index structure</div>
    </div>` : '');

    // Cluster-wide totals: 1 primary + N replicas
    const totalCopies = 1 + replicas;

    if (replicas > 0) {
      $('clusterCard').style.display = 'block';
      const clDisk = totalDisk * totalCopies;
      const clRam = totalRam * totalCopies;
      const cdFmt = formatBytes(clDisk);
      const crFmt = formatBytes(clRam);
      $('clusterDisk').innerHTML = `${cdFmt.value}<span class="unit">${cdFmt.unit}</span>`;
      $('clusterDiskSub').textContent = `1 primary + ${replicas} replica(s) = ${totalCopies} total copies`;
      $('clusterRam').innerHTML = `${crFmt.value}<span class="unit">${crFmt.unit}</span>`;
      $('clusterRamSub').textContent = `Spread across data nodes holding these replicas`;
      formulas.push(`\nCluster total disk = per-replica × ${totalCopies} copies = ${formatBytesStr(clDisk)}`);
      formulas.push(`Cluster total RAM = per-replica × ${totalCopies} copies = ${formatBytesStr(clRam)}`);
    } else {
      $('clusterCard').style.display = 'none';
    }

    // Formulas
    $('formulaText').textContent = formulas.join('\n');
  }

  // Initial
  recalculate();
})();
</script>



## Warm up the filesystem cache [dense-vector-preloading]

If the machine running {{es}} is restarted, the filesystem cache will be empty, so it will take some time before the operating system loads hot regions of the index into memory so that search operations are fast. You can explicitly tell the operating system which files should be loaded into memory eagerly depending on the file extension using the [`index.store.preload`](elasticsearch://reference/elasticsearch/index-settings/preloading-data-into-file-system-cache.md) setting.

::::{warning}
Loading data into the filesystem cache eagerly on too many indices or too many files will make search *slower* if the filesystem cache is not large enough to hold all the data. Use with caution.
::::

The following file extensions are used for the approximate kNN search: Each extension is broken down by the quantization types.

* {applies_to}`stack: ga 9.3+` `cenivf` for DiskBBQ to store centroids
* {applies_to}`stack: ga 9.3+` `clivf` for DiskBBQ to store clusters of quantized vectors
* `vex` for the HNSW graph
* `vec` for all non-quantized vector values. This includes all element types: `float`, `byte`, and `bit`.
* `veq` for quantized vectors indexed with [`quantization`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization): `int4` or `int8`
* `veb` for binary vectors indexed with [`quantization`](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#dense-vector-quantization): `bbq`
* `vem`, `vemf`, `vemq`, and `vemb` for metadata, usually small and not a concern for preloading

Generally, if you are using a quantized index, you should only preload the relevant quantized values and index structures such as the HNSW graph. Preloading the raw vectors is not necessary and might be counterproductive, because paging in the raw vectors might cause the OS to evict important index structures from the cache.

You can gather additional detail about the specific files by using the [stats endpoint](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-stats), which displays information about the index and fields.

For example, for DiskBBQ, the response might look like this:

```console
GET my_index/_stats?filter_path=indices.my_index.primaries.dense_vector

{
    "indices": {
        "my_index": {
            "primaries": {
                "dense_vector": {
                    "value_count": 3,
                    "off_heap": {
                        "total_size_bytes": 249,
                        "total_veb_size_bytes": 0,
                        "total_vec_size_bytes": 36,
                        "total_veq_size_bytes": 0,
                        "total_vex_size_bytes": 0,
                        "total_cenivf_size_bytes": 111,
                        "total_clivf_size_bytes": 102,
                        "fielddata": {
                            "my_vector": {
                                "cenivf_size_bytes": 111,
                                "clivf_size_bytes": 102,
                                "vec_size_bytes": 36
                            }
                        }
                    }
                }
            }
        }
    }
}
```


## Reduce the number of index segments [_reduce_the_number_of_index_segments]

{{es}} shards are composed of segments, which are internal storage elements in the index. For approximate kNN search, {{es}} stores the vector values of each segment as a separate HNSW graph, so kNN search must check each segment. The recent parallelization of kNN search made it much faster to search across multiple segments, but still kNN search can be up to several times faster if there are fewer segments. By default, {{es}} periodically merges smaller segments into larger ones through a background [merge process](elasticsearch://reference/elasticsearch/index-settings/merge.md). If this isn’t sufficient, you can take explicit steps to reduce the number of index segments.


### Increase maximum segment size [_increase_maximum_segment_size]

{{es}} provides many tunable settings for controlling the merge process. One important setting is `index.merge.policy.max_merged_segment`. This controls the maximum size of the segments that are created during the merge process. By increasing the value, you can reduce the number of segments in the index. The default value is `5GB`, but that might be too small for larger dimensional vectors. Consider increasing this value to `10GB` or `20GB` can help reduce the number of segments.


### Create large segments during bulk indexing [_create_large_segments_during_bulk_indexing]

A common pattern is to first perform an initial bulk upload, then make an index available for searches. Instead of force merging, you can adjust the index settings to encourage {{es}} to create larger initial segments:

* Ensure there are no searches during the bulk upload and disable [`index.refresh_interval`](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-refresh-interval-setting) by setting it to `-1`. This prevents refresh operations and avoids creating extra segments.
* Give {{es}} a large indexing buffer so it can accept more documents before flushing. By default, the [`indices.memory.index_buffer_size`](elasticsearch://reference/elasticsearch/configuration-reference/indexing-buffer-settings.md) is set to 10% of the heap size. With a substantial heap size like 32GB, this is often enough. To allow the full indexing buffer to be used, you should also increase the limit [`index.translog.flush_threshold_size`](elasticsearch://reference/elasticsearch/index-settings/translog.md).


## Avoid heavy indexing during searches [_avoid_heavy_indexing_during_searches]

Actively indexing documents can have a negative impact on approximate kNN search performance, since indexing threads steal compute resources from search. When indexing and searching at the same time, {{es}} also refreshes frequently, which creates several small segments. This also hurts search performance, since approximate kNN search is slower when there are more segments.

When possible, it’s best to avoid heavy indexing during approximate kNN search. If you need to reindex all the data, perhaps because the vector embedding model changed, then it’s better to reindex the new documents into a separate index rather than update them in-place. This helps avoid the slowdown mentioned above, and prevents expensive merge operations due to frequent document updates.


## Avoid page cache thrashing by using modest readahead values on Linux [_avoid_page_cache_thrashing_by_using_modest_readahead_values_on_linux_2]

Search can cause a lot of randomized read I/O. When the underlying block device has a high readahead value, there may be a lot of unnecessary read I/O done, especially when files are accessed using memory mapping (see [storage types](elasticsearch://reference/elasticsearch/index-settings/store.md#file-system)).

Most Linux distributions use a sensible readahead value of `128KiB` for a single plain device, however, when using software raid, LVM or dm-crypt the resulting block device (backing {{es}} [path.data](../../deploy/self-managed/important-settings-configuration.md#path-settings)) may end up having a very large readahead value (in the range of several MiB). This usually results in severe page (filesystem) cache thrashing adversely affecting search (or [update](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-document)) performance.

You can check the current value in `KiB` using `lsblk -o NAME,RA,MOUNTPOINT,TYPE,SIZE`. Consult the documentation of your distribution on how to alter this value (for example with a `udev` rule to persist across reboots, or via [blockdev --setra](https://man7.org/linux/man-pages/man8/blockdev.8.html) as a transient setting). We recommend a value of `128KiB` for readahead.

::::{warning}
`blockdev` expects values in 512 byte sectors whereas `lsblk` reports values in `KiB`. As an example, to temporarily set readahead to `128KiB` for `/dev/nvme0n1`, specify `blockdev --setra 256 /dev/nvme0n1`.
::::


## Use on-disk rescoring when the vector data does not fit in RAM
```{applies_to}
stack: preview 9.3
serverless: unavailable
```
If you use quantized indices and your nodes don't have enough off-heap RAM to store all vector data in memory, then you might experience high query latencies. Vector data includes the HNSW graph, quantized vectors, and raw float vectors.

In these scenarios, on-disk rescoring can significantly reduce query latency. Enable it by setting the `on_disk_rescore: true` option on your vector indices. Your data must be re-indexed or force-merged to use the new setting in subsequent searches.
