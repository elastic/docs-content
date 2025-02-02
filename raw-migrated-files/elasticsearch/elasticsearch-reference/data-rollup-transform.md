# Roll up or transform your data [data-rollup-transform]

{{es}} offers the following methods for manipulating your data:

* [Rolling up your historical data](../../../manage-data/lifecycle/rollup.md)

    ::::{admonition} Deprecated in 8.11.0.
    :class: warning

    Rollups will be removed in a future version. Use [downsampling](../../../manage-data/data-store/index-types/downsampling-time-series-data-stream.md) instead.
    ::::


    The {{stack}} {rollup-features} provide a means to summarize and store historical data so that it can still be used for analysis, but at a fraction of the storage cost of raw data.

* [Transforming your data](../../../explore-analyze/transforms.md)

    {{transforms-cap}} enable you to convert existing {{es}} indices into summarized indices, which provide opportunities for new insights and analytics.


